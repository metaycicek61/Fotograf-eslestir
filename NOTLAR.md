# Formasyon Okuyucu AI - Proje Notları

Site: metaycicek61.github.io/Fotograf-eslestir/Okuyucu.html (canlı dosya: Okuyucu.html; tek dosyalık HTML/JS, kamerayla mum formasyonu okuma)

## Uygulama özeti
- Kamera, ekrandaki yeşil "SON HAREKET" kutusunu okur.
- Kırmızı/yeşil renk maskesiyle mumları bulur, referans formasyonlarla karşılaştırır.
- Skor: %95 şekil + %5 AI (CLIP). AI şu an %97-98 sabit verdiği için neredeyse hiç ayırt etmiyor.

## Önemli ayarlar (kodda)
- TARGET_W=502, TARGET_H=277
- SCAN_LEFT=.49, SCAN_RIGHT=.93, SCAN_TOP=.025, SCAN_BOTTOM=.975
- SHAPE_WEIGHT=.95, AI_WEIGHT=.05

## Kararlar
- Kamera girdisi: Binance grafiğinin telefonla çekilmiş fotoğrafı. Sistemin başlangıcı bu.
- Referans görselleri bu biçime uygun olmalı: beyaz fon, başlık/çerçeve/ızgara yok, fitil mum renginde.
- Hazır formasyon görselleri (siyah fitilli, çerçeveli) Binance fotoğrafıyla uyuşmuyordu. Sorun kameradan değil, formasyon görsellerindendi.
- Formasyonlar `araclar/formasyon_betik.py` ile standartlaştırılır. Sonra sağdan N mum beyaza çevrilir (--cut N).
- Mum kalınlığı şimdilik değiştirilmiyor (Binance'e yaklaştırma ileride karar verilecek).

## Betik kullanımı
python3 formasyon_betik.py girdi.png cikti_klasoru --cut 6

Çıktılar: *_temiz.png, *_numarali.png, *_rapor.json (+ --cut ile *_sagN_beyaz.png)
Rapor: mum sayısı, yeşil/kırmızı, rengi belirsiz mumlar. Referansı siteye koymadan önce raporu kontrol et.
Betik, mumlar arasına en az 2 piksel boşluk bırakır (uygulama yan yana değen mumları tek sayıyor).

## Kütüphane
1. Liquidity Sweep + Bullish Reversal (26 mum)
2. Bullish Order Block Retest (32 mum)
3. Break of Structure - BOS (30 mum)
Sağdan kesilen mumlar: F1 son 5 (22-26, kalan 21), F2 son 8 (25-32, kalan 24), F3 son 5 (26-30, kalan 25). Dosyalar: formasyonlar/kesilmis/

## Yapılacaklar
- [x] Sağdan kesilecek mum sayıları belirlendi, kesilmiş dosyalar hazır
- [ ] Kesilmiş referansları siteye ekle (eski referansları sil)
- [x] Koda iki düzeltme yapıldı (Okuyucu.html): candleFromBody (fitil uzatma, boşluk toleransı), imageToCanvas kenar temizliği. Kamerayla test bekliyor.
- [x] Mum sayısı uyuşmazlığı düzeltildi: kamera referanstan az mum görürse referansın son k mumuyla da karşılaştırılır (bestShapeMatch / referenceTail).
- [x] Sahte kutular: gövde yüksekliği tuvalin %55'inden büyükse elenir; kenara değen ve %35'ten uzun gövdeler elenir.
- [x] Canlı kullanıcı ipuçları eklendi (#hint): mum okunamıyor / az mum / çok mum / taşıyor / iyi görüntü; tarama sonrası güçlü-orta-zayıf eşleşme ve yakın skor uyarısı.
- [ ] AI skorunu düzelt (ölçekle ya da kapat)
- [x] Tarama alanı oranı düzeltildi: kutu artık referansla aynı oranda (SCAN_LEFT .25, RIGHT .97, TOP .20, BOTTOM .795), mumlar gerilmiyor. Yakalama 2x çözünürlükte.
- [ ] Tek kare yerine birkaç kareye bakıp tutarlı sonuç alma
- [ ] Düşük skorda "eşleşme yok" eşiği
- [ ] Test: referansı ekranda açıp kendi kendine taratma, sonra gerçek Binance grafiği
- [ ] Başka telefonda test (renk eşikleri ayarlanabilir olabilir)
- [ ] Koyu temalı Binance ekranıyla test (renk eşikleri koyu zeminde bozulabilir)
- [ ] Renk kalibrasyonu: kamera ilk karede grafiğin kırmızı/yeşil tonlarına bakıp HSV eşiklerini kendisi ayarlasın (farklı telefon kamerası ve ekran parlaklığı için)
- [ ] Odak kontrolü: dokunarak odaklama ya da bulanıklık uyarısı (yakın mesafede odak kaçabiliyor)

## Bilinen riskler
- Rengi belirsiz mumlar (kahverengi/zeytin doji): F1 #2, F2 #4 ve #17, F3 #2, #20, #28 kontrol edilecek.
- Referanslar localStorage'da base64: çok görselde kota dolabilir.
- Referans önbellek anahtarı index|uzunluk, silince karışabilir.

## Yedekleme ve güvenlik (yapılacaklar)
- [ ] Ayda bir yedek al: depo sayfası > yeşil Code düğmesi > Download ZIP > iCloud'a kaydet
- [ ] Önemli dosyaların (Okuyucu.html, NOTLAR.md, araclar/formasyon_betik.py) kopyasını iCloud'da da tut
- [ ] GitHub hesabında iki adımlı doğrulamayı aç
- [ ] Depo herkese açık (public) kalsın: GitHub Pages ücretsiz planda yalnızca public depolarda çalışır

## Maliyet notu
- GitHub Free süresiz ücretsiz; çalışmalar bir ay sonra silinmez. Ödeme gerekmiyor.
- Site adresi (metaycicek61.github.io/Fotograf-eslestir) ücretsiz. Kendi domain istenirse .com yaklaşık 10-11 dolar/yıl (Cloudflare), bağlamak ücretsiz.

## Geri dönme
- Her değişiklik ayrı commit olarak kayıtlı. Bir şey bozulursa eski sürüme dönülebilir (depoda Commits sayfasından ya da Claude'dan istenerek).
