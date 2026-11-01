# QM kütüphanesi — işlem kaydı

Orijinal görseller telif nedeniyle depoda YOK (yalnızca kullanıcının özel arşivinde). Burada sadece yöntem, betikler ve hata kayıtları var.

## Standart adımlar (her görsel için)
1. **Mum algılama** (`numara.py`): gövde renkleri (kırmızı/yeşil) sütun sütun taranır, her mum soldan sağa numaralanır.
2. **Eksik mum doldurma** (`fill.py`): mum aralığının medyanı alınır; iki mum arası 1,5 aralıktan büyükse aradaki ince doji mumlar renk taramasıyla eklenir.
3. **Fitil uçları** (`wick.py`): gövdeden yukarı/aşağı kesintisiz renkli piksel izlenir. Grafikteki yatay çizgiler (fiyat çizgisi, bölge sınırı) önce silinir; yoksa fitil sanılır.
4. **Kesim kararı**: kullanıcı numaralı görsel üzerinde verir (formasyon başlangıcı + kesim mumu, kesim mumu DAHİL).
5. **Temiz çizim** (`temiz.py`): formasyon mumları sitenin kütüphane biçiminde yeniden çizilir — 502×277, beyaz zemin, kenar payı 30/22 px, kırmızı #e02b3b / yeşil #089c58, fitil mum renginde. Mum sırası, rengi ve oranları korunur.
6. **Kanallar (%20)**: her kanalda en uç GÖVDELER esas alınır, paralel iki çizgi çizilir ve kanal genişliğinin %20'si kadar dışarı kaydırılır (kesikli çizgi). Kanallar görsele GİRMEZ (okuyucu çizgiyi mum sanır); `*_kanallar.json` dosyasında eğim / kesişim / üst-alt sınır olarak saklanır. Eşleştirmede %20 sınırını aşan mum → o formasyon elenir.
7. **Site kontrolü** (`siteraw.js`): temiz görsel, sitenin KENDİ okuma kodu (`imageToCanvas` → `referenceSequence`) ile okunur. Kamera görüntüsü de karşılaştırmadan önce aynı koddan geçer; böylece kütüphane ve kamera aynı işlemden geçmiş olur. Beklenen: okunan mum sayısı = formasyon mum sayısı, renk hatası 0, boy farkı < %3.

## 01 — QM SH Nora GBPUSD 1G (1 Kasım)
- Kesim: kullanıcı numarasıyla 8–58 (58 dahil). Devam (öngörülecek kısım): 59–103.
- **Hata 1 — gizli mum:** 55 ile 56 arasında aralık 10,5 px (medyan 5,5). Bakıldığında gövdesi tamamen grafiğin altında kalan bir kırmızı mum var (sadece 1 px'lik ucu görünüyor). Algılama bunu kaçırmıştı.
  - Düzeltme: mum eklendi (kırmızı, en alt seviyede, "kırpık" işaretli). Formasyon **51 → 52 mum**. Kullanıcının numaralandırmasında 56'dan sonraki numaralar 1 kayar; kesim aynı fiziksel mumda (eski 58 = yeni 59).
- **Hata 2 — kırpık dipler:** 55, gizli mum ve 56'nın dipleri grafiğin alt kenarında kesik; gerçek dip görünmüyor. Temiz çizimde düz dip olarak kaldı.
  - Düzeltme yok (veri yok). Kullanıcı aynı grafiği aşağısı görünecek şekilde çekerse güncellenecek.
- **Hata 3 — yanlış kütüphane dosyası:** Önce sitenin `drawCleanCandles` çıktısı (`*_site.png`) kütüphane dosyası olarak önerilmişti. Site bu dosyayı tekrar okuyunca 51 yerine **48 mum** buldu: 51 mumda gövdeler (~10 px) mum aralığından (8,8 px) geniş çiziliyor, yan yana mumlar birleşiyor.
  - Düzeltme: kütüphane dosyası `temiz.py` çıktısı (gövde ≤ aralığın %76'sı). Site karşılaştırmada kütüphane görselini zaten kendi okuma kodundan geçiriyor; `drawCleanCandles` sadece yapay zekâ benzerliği için ara çizim. (Kamera/mum sayım koduna dokunulmadı.)
- **Hata 4 — ilk algılamada fitiller:** İlk taramada bazı fitil uçları başlık/ızgara pikseline kadar uzamıştı (ör. 9. mum). `wick.py` ile kesintisiz tarama yapılarak düzeltildi.
- Son kontrol: site okuması 52/52 mum, renk hatası 0, en büyük boy farkı %0,4.
- Kanallar (gövde + %20): 8–26 yükselen, 26–42 inen, 42–47 yükselen (retest), 47–57 inen, 57–59 yükselen.
