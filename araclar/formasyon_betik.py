#!/usr/bin/env python3
"""
Formasyon Okuyucu AI - formasyon görseli standartlaştırma betiği

Ne yapar (mumların yeri, boyu, sırası DEĞİŞMEZ, boyut aynı kalır):
  1. Başlık bandı, dış çerçeve ve arka plan süslerini (ızgara, order block alanı) beyaza çevirir.
  2. Siyah fitilleri ve siyah mum kenarlarını mumun kendi rengine (kırmızı/yeşil) boyar.
  3. Doji gibi soluk renkli mumları en yakın renge (kırmızı/yeşil) çevirir.
  4. Mumları soldan sağa numaralar, kontrol raporu ve numaralı önizleme üretir.
  5. İstenirse sağdan N mumu beyaza çevirir (--cut N).

Kullanım:
  python3 formasyon_betik.py girdi.png cikti_klasoru [--cut N]
"""
import sys, json, argparse, os, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

RED = (224, 43, 59)
GREEN = (8, 156, 88)


def hsv_arrays(a):
    f = a.astype(float) / 255.0
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx = f.max(2)
    mn = f.min(2)
    d = mx - mn
    with np.errstate(all="ignore"):
        hr = 60 * (((g - b) / d) % 6)
        hg = 60 * (((b - r) / d) + 2)
        hb = 60 * (((r - g) / d) + 4)
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb))
    h = np.where(d != 0, h, 0)
    h = np.where(h < 0, h + 360, h)
    s = np.where(mx == 0, 0, d / np.maximum(mx, 1e-9))
    return h, s, mx


def header_bottom(a):
    """Başlık bandının bittiği satırı bulur (pastel yeşil bant)."""
    h, w = a.shape[:2]
    xs = [w // 4, w // 2, 3 * w // 4]
    last = 0
    for y in range(0, 70):
        ok = 0
        for x in xs:
            r, g, b = a[y, x]
            if g > r + 12 and g > b + 8 and r > 150:  # pastel yeşil
                ok += 1
        if ok >= 2:
            last = y
    return last + 2


def normalize(path, cut=0):
    img = Image.open(path).convert("RGB")
    a = np.array(img).astype(int)
    H, W = a.shape[:2]
    hb = header_bottom(a)
    hue, sat, val = hsv_arrays(a)

    # 1) gövde pikselleri: yeterince doygun ve koyu/orta tonlu (pastel zeminleri dışlar)
    body = (sat > 0.35) & (val > 0.25)
    body[:hb] = False
    border = 6
    body[:border] = False
    body[-border:] = False
    body[:, :border] = False
    body[:, -border:] = False

    # renk sınıfı: yeşil (90-180) / kırmızı-turuncu-zeytin (diğer)
    is_green = (hue >= 55) & (hue <= 180)  # zeytin (60-90) yeşile gider
    green_mask = body & is_green
    red_mask = body & ~is_green

    # gövde bileşenleri (tür ayırmadan: soluk dojiler renk karışımı olabilir)
    allmask = green_mask | red_mask
    allmask = ndimage.binary_closing(allmask, structure=np.ones((3, 3)))
    lab, n = ndimage.label(allmask, structure=np.ones((3, 3)))
    comps = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        comp = (lab == i)
        area = int(comp.sum())
        w = sl[1].stop - sl[1].start
        if area < 10 or w < 3:
            continue
        comps.append({"i": i, "sl": sl, "comp": comp, "w": w})

    # tipik gövde genişliği
    ws = [c["w"] for c in comps if c["w"] >= 8]
    medw = float(np.median(ws)) if ws else 10.0

    pieces = []
    for c in comps:
        sl, comp, w = c["sl"], c["comp"], c["w"]
        x0, x1 = sl[1].start, sl[1].stop - 1
        n_parts = max(1, int(round(w / medw))) if w > 1.5 * medw else 1
        cuts = [x0]
        colcount = comp[:, x0:x1 + 1].sum(axis=0)
        for k in range(1, n_parts):
            target = x0 + k * w / n_parts
            lo = int(max(x0 + 1, target - 2)); hi = int(min(x1 - 1, target + 2))
            best = min(range(lo, hi + 1), key=lambda cx: colcount[cx - x0]) if hi >= lo else int(target)
            cuts.append(best)
        cuts.append(x1 + 1)
        for a0, a1 in zip(cuts[:-1], cuts[1:]):
            sub = comp[:, a0:a1]
            ys, xs = np.where(sub)
            if len(ys) < 10:
                continue
            gcount = int((green_mask[:, a0:a1] & sub).sum())
            rcount = int((red_mask[:, a0:a1] & sub).sum())
            pieces.append({
                "type": 2 if gcount > rcount else 1,
                "x0": a0 + int(xs.min()), "x1": a0 + int(xs.max()),
                "y0": int(ys.min()), "y1": int(ys.max()),
                "area": len(ys),
                "belirsiz": bool((((hue[:, a0:a1][sub] >= 12) & (hue[:, a0:a1][sub] <= 80)).mean()) > 0.3),
            })
    pieces.sort(key=lambda b: (b["x0"] + b["x1"]) / 2)
    candles = pieces
    for c in candles:
        c["cx"] = (c["x0"] + c["x1"]) / 2

    # yan yana değen gövdeler arasına en az 2 piksel boşluk bırak (algılama mumları ayırabilsin)
    MIN_GAP = 2
    for i in range(len(candles) - 1):
        l, r = candles[i], candles[i + 1]
        gap = r["x0"] - l["x1"] - 1
        if gap < MIN_GAP:
            need = MIN_GAP - gap
            take_l = (need + 1) // 2
            take_r = need - take_l
            if l["x1"] - take_l - l["x0"] >= 2:
                l["x1"] -= take_l
            if r["x1"] - (r["x0"] + take_r) >= 2:
                r["x0"] += take_r

    # 2) koyu pikseller (fitil + kenar): en yakın mumun rengine boyanır
    dark = (val < 0.55) & (sat < 0.6)
    dark[:hb] = False
    dark[:border] = False
    dark[-border:] = False
    dark[:, :border] = False
    dark[:, -border:] = False

    out = np.full(a.shape, 255, np.uint8)
    cxs = np.array([c["cx"] for c in candles])
    colors = {1: RED, 2: GREEN}

    ys, xs = np.where(dark)
    for y, x in zip(ys, xs):
        k = int(np.argmin(np.abs(cxs - x)))
        c = candles[k]
        half = (c["x1"] - c["x0"]) / 2
        if abs(x - c["cx"]) <= half + 1.5:
            c["wick_y0"] = min(c.get("wick_y0", y), y)
            c["wick_y1"] = max(c.get("wick_y1", y), y)

    for c in candles:
        c.setdefault("wick_y0", c["y0"])
        c.setdefault("wick_y1", c["y1"])
        c["top"] = min(c["y0"], c["wick_y0"])
        c["bottom"] = max(c["y1"], c["wick_y1"])
        col = colors[c["type"]]
        # kesintisiz fitil (2 piksel genişlik, mumun ortasında)
        wx = int(round(c["cx"]))
        out[c["top"]: c["bottom"] + 1, wx: wx + 2] = col
        # dolu gövde
        out[c["y0"]: c["y1"] + 1, c["x0"]: c["x1"] + 1] = col

    # 3) sağdan kesme
    cut_info = []
    if cut > 0:
        for c in candles[-cut:]:
            pad = 3
            out[max(0, c["top"] - pad): c["bottom"] + pad + 1,
                max(0, c["x0"] - pad): c["x1"] + pad + 1] = 255
            cut_info.append(candles.index(c) + 1)

    return Image.fromarray(out), candles, hb, cut_info


def numbered_preview(norm_img, candles):
    prev = norm_img.resize((norm_img.width * 2, norm_img.height * 2), Image.NEAREST)
    d = ImageDraw.Draw(prev)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
    except Exception:
        f = None
    for i, c in enumerate(candles, 1):
        x = int(c["cx"] * 2)
        y = max(10, int(c["top"] * 2) - 12)
        d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(30, 60, 255))
        d.text((x, y), str(i), fill="white", font=f, anchor="mm")
    return prev


def report(candles, hb, name):
    g = sum(c["type"] == 2 for c in candles)
    r = sum(c["type"] == 1 for c in candles)
    return {
        "dosya": name,
        "mum_sayisi": len(candles),
        "yesil": g,
        "kirmizi": r,
        "baslik_alti_satir": hb,
        "mumlar": [
            {"no": i, "renk": "yesil" if c["type"] == 2 else "kirmizi",
             "x": round(c["cx"], 1), "ust": int(c["top"]), "alt": int(c["bottom"]),
             "govde_genislik": int(c["x1"] - c["x0"] + 1),
             "renk_belirsiz": c.get("belirsiz", False)}
            for i, c in enumerate(candles, 1)
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("girdi")
    ap.add_argument("cikti_klasoru")
    ap.add_argument("--cut", type=int, default=0, help="sağdan beyaza çevrilecek mum sayısı")
    a = ap.parse_args()
    os.makedirs(a.cikti_klasoru, exist_ok=True)
    base = os.path.splitext(os.path.basename(a.girdi))[0]

    norm, candles, hb, _ = normalize(a.girdi, 0)
    norm.save(os.path.join(a.cikti_klasoru, base + "_temiz.png"))
    numbered_preview(norm, candles).save(os.path.join(a.cikti_klasoru, base + "_numarali.png"))
    rep = report(candles, hb, base)
    if a.cut > 0:
        cutimg, _, _, cut_info = normalize(a.girdi, a.cut)
        cutimg.save(os.path.join(a.cikti_klasoru, "%s_sag%d_beyaz.png" % (base, a.cut)))
        rep["kesilen_mumlar"] = cut_info
    with open(os.path.join(a.cikti_klasoru, base + "_rapor.json"), "w", encoding="utf-8") as fh:
        json.dump(rep, fh, ensure_ascii=False, indent=2)
    print(base, "mum:", rep["mum_sayisi"], "yesil:", rep["yesil"], "kirmizi:", rep["kirmizi"])


if __name__ == "__main__":
    main()
