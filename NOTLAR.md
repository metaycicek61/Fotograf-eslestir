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
- [x] Tarama alanı oranı düzeltildi: kutu artık referansla aynı oranda (önce sabit SCAN_LEFT .25, RIGHT .97, TOP .20, BOTTOM .795; artık otomatik, aşağıya bak), mumlar gerilmiyor. Yakalama 2x çözünürlükte.
- [ ] Tek kare yerine birkaç kareye bakıp tutarlı sonuç alma
- [ ] Düşük skorda "eşleşme yok" eşiği
- [ ] Test: referansı ekranda açıp kendi kendine taratma, sonra gerçek Binance grafiği
- [ ] Uzun formasyonlar (40–60 mum) bul, sonra 1x çalışması (bkz. "Karar 31 Ekim 04:49")
- [ ] Başka telefonda test (renk eşikleri ayarlanabilir olabilir)
- [ ] Koyu temalı Binance ekranıyla test (renk eşikleri koyu zeminde bozulabilir)
- [ ] Renk kalibrasyonu: kamera ilk karede grafiğin kırmızı/yeşil tonlarına bakıp HSV eşiklerini kendisi ayarlasın (farklı telefon kamerası ve ekran parlaklığı için)
- [ ] Odak kontrolü: dokunarak odaklama ya da bulanıklık uyarısı (yakın mesafede odak kaçabiliyor)

### SIRALI YOL HARİTASI (kullanıcı kararı, 30 Ekim 06:13)
Adımlar bu sırayla yapılacak; bir adım bitmeden sonrakine geçilmez.

**ADIM 1: Kaliteli çekim ve tüm mumları tam tanıma**
- [ ] Kullanıcıya daha net bilgi: ne yapması gerektiğini tek cümleyle söyleyen uyarılar
- [ ] Bulanıklık kontrolü: bulanık görüntüye "iyi" denmesin, "netleşmesini bekle" desin
- [x] Yeşil tarama alanı büyütüldü (30 Ekim 06:25): aynı en-boy oranında (502x277) kamera alanına sığan en büyük kutu, kenarlarda %3 pay. Ölçü telefona göre otomatik hesaplanır (updateScanBox). iPhone'da yaklaşık genişlik %72 -> %94, yükseklik %60 -> %79 (~1,7 kat alan). Sebep: grafiğin üstü/altı kutudan taşıyor, sadece ~28 mum giriyordu.
- [ ] Kütüphanedeki mum sayısına göre çekim: kutuda kütüphane formasyonları kadar mum görünsün
- [ ] Birkaç kareye bak (3-5), hepsinde aynı okunan mumları al
- [ ] Kutunun kenarında yarım kalan mumları alma

**ADIM 2: Fotoğrafı kütüphane biçimine getirme (sitenin kendi betiği)**
- [ ] Tüm mumlar okununca site, Claude'un elle yaptığı gibi temiz çizim üretsin (beyaz zemin, kırmızı/yeşil, fitil mum renginde)
- [ ] Kontrol ekranı: temiz çizim numaralı gösterilsin, kullanıcı onaylasın
- [ ] Karşılaştırma bu temiz çizim üzerinden yapılsın (amaç kameradan çekilen görüntüyü karşılaştırmaya hazırlamak; kütüphaneye ekleme değil)

**ADIM 3: Karşılaştırmada zaman ve mum etkisini çözme**
- Aşağıdaki "Aşama takibi" maddeleri (hayalet çizim en son)

### Aşama takibi (asıl hedef: zamanla oluşacak formasyonu yakalamak)
Kütüphanedeki formasyonların sağı kesildi; kesilen kısım formasyonun devamı. Canlı grafiğin sağ başı "şu an". Formasyon zamanla oluşur, canlı grafik formasyonun ortasında olabilir. Akan zaman engel değil, doğrulama.
- [ ] 1. Aşama karşılaştırması: canlı grafiğin son mumlarını formasyonun farklı aşamalarıyla karşılaştır (ilk 12, 15, 18 ... sonuna kadar mum)
- [ ] 2. Sonuçta aşamayı göster: "Fo1'e benziyor, aşama 15/21, %82"
- [ ] 3. Her yeni mum oluştuğunda tekrar tara: formasyon oluşuyorsa aşama ilerler ve skor yükselir; oluşmuyorsa skor düşer, uyarı verir
- [ ] 4. (EN SON) Hayalet çizim: kalan mumlar ve kesilen devam kısmı sağa yarı saydam çizilsin (Ghost Pattern Finder fikri)
- [ ] Kaçırılan formasyon (1 Kasım, kullanıcı fikri, değerlendirildi): Tara en sağdaki pencere uymazsa pencereyi sola kaydırarak arasın; formasyonun sağında kalan mum sayısı formasyonun mum sayısının %50'sinden AZ ise eşleşmeyi göstersin ve uyarsın ("⚠️ Formasyon N mum önce tamamlandı, hareket başlamış olabilir; işlem kararı senin"). %50 ve üstü: çok geç, gösterme. Dikkat: (1) çok pencere = şans eseri eşleşme riski → eşik en sağ pencere %80, kaydırılmışlar %85; (2) sağda oluşmuş mumlar tahminle uyumlu mu kontrol (çelişirse uyar); (3) daha çok mum gerekir (1x önerisi buna göre); (4) tahminde gerçekleşen ve kalan hareket ("beklenen ▼%58, olan ▼%20, kalan ~▼%38").

## Bilinen riskler
- Rengi belirsiz mumlar (kahverengi/zeytin doji): F1 #2, F2 #4 ve #17, F3 #2, #20, #28 kontrol edilecek.
- Referanslar localStorage'da base64: çok görselde kota dolabilir.
- Referans önbellek anahtarı index|uzunluk, silince karışabilir.

## Yedekleme ve güvenlik (yapılacaklar)
- [ ] Ayda bir yedek al: depo sayfası > yeşil Code düğmesi > Download ZIP > iCloud'a kaydet
- [ ] Önemli dosyaların (Okuyucu.html, NOTLAR.md, araclar/formasyon_betik.py) kopyasını iCloud'da da tut
- [ ] GitHub hesabında iki adımlı doğrulamayı aç
- [ ] Depo herkese açık (public) kalsın: GitHub Pages ücretsiz planda yalnızca public depolarda çalışır
- [ ] Ziyaretçi erişimi (1 Kasım): site ve depo herkese açık. Ziyaretçi siteyi kullanabilir, kodu / NOTLAR.md'yi / formasyonlar/ klasörünü okuyabilir ve "📚 Hazır Kütüphane"yi yükleyip kullanabilir; telefondaki kişisel kütüphaneyi göremez, depoyu değiştiremez. Karar verilecek: (a) depoyu private yapmak (Pages için ücretli plan gerekir), (b) notları ayrı private depoya taşımak, (c) hazır kütüphaneyi siteden kaldırıp sadece kişisel kullanım. Formasyon Hazırla ile hazırlanan formasyonlar hiçbir zaman depoya/siteye yüklenmeyecek (telif).
- [ ] Kişisel kütüphanenin korunması (1 Kasım, ileride): Safari, 7 gün girilmeyen sitenin verilerini silebilir. (1) Siteyi Ana Ekrana Ekle (uygulama gibi açılır, silme kuralı uygulanmaz). (2) Formasyon Hazırla'ya dışa aktar / içe aktar düğmesi: kütüphane tek dosya (mum verisi + kanallar + temiz çizim) olarak iCloud/Dosyalar'a; telefon değişince geri yükleme, kontrol için Claude'a gönderme. Dosya depoya/siteye girmez.

## Maliyet notu
- GitHub Free süresiz ücretsiz; çalışmalar bir ay sonra silinmez. Ödeme gerekmiyor.
- Site adresi (metaycicek61.github.io/Fotograf-eslestir) ücretsiz. Kendi domain istenirse .com yaklaşık 10-11 dolar/yıl (Cloudflare), bağlamak ücretsiz.

## Geri dönme
- Her değişiklik ayrı commit olarak kayıtlı. Bir şey bozulursa eski sürüme dönülebilir (depoda Commits sayfasından ya da Claude'dan istenerek).

## Test sonuçları (iPhone, 29 Ekim, fo2 kendi kendine test, başka telefon ekranında)
- Formasyonun tamamı kutuda (25 mum algılandı): fo2 %99 (Formasyon %99, AI %100). Doğru.
- Kısmi görünüm (13 mum algılandı, grafik yakın): Fo1 %76, fo2 %60. YANLIŞ birinci. Sebep: sadece son ~13 mum görününce Fo1 ve fo2'nin sonu (yatay taban + büyük yeşil mum) birbirine benziyor.
- Karar: kutuda en az 18 mum görünmeli (FULL_VIEW_MIN=18). Daha azsa canlı uyarı "Formasyonun tamamı görünmüyor, uzaklaş" der.
- Binance gerçek ekran testlerinde sorunlar: bulanıklık, MA çizgileri ve filigran sahte kutu üretiyor. Binance'te gösterge ve ızgara kapatılmalı.

## Mum sayısı ölçütleri (VIEW_RULES, Okuyucu.html)
Gözlem (iPhone, yakın ve paralel çekim): 17 mum ve üstü iyi, 25 mum civarı en iyi sonuç.
Eşikler kütüphaneden otomatik hesaplanır, yeni formasyon eklenince kendiliğinden güncellenir:
- iyi başlangıç = en kısa referansın %95'i (şu an 21 mum -> 20). İlk değer %80 (17) idi, test sonuçlarına göre 20'ye çekildi
- çok iyi = en uzun referansın %95'i (şu an 25 mum -> 24)
- çok fazla = en uzun referansın %125'i
- Ayar: VIEW_RULES içindeki goodRatio / bestRatio / manyRatio / minGoodFloor
- Kütüphane okunamazsa varsayılanlar: 20 / 24 / 31
Uyarı şeridi: 20'nin altı "formasyonun tamamı görünmüyor", 20-23 "iyi", 24 ve üstü "çok iyi".

## Mesafe gözlemi (iPhone, 06:41)
- Orta mesafe, grafik kutunun ortasında: 24 mum, "çok iyi görüntü". En dengeli çekim bu.
- Yakın mesafe: 15 mum, görüntü bulanık, formasyonun tamamı kutuya girmiyor. Uyarı şeridi bu durumda "formasyonun tamamı görünmüyor" demeli.
- Hata düzeltildi: uyarı şeridi önceki karelerin ortalamasına bakıp geriden geliyordu (sensör 15, şerit 18 yazıyordu). Artık son 3 kareye bakıyor ve metinde o anki mum sayısını gösteriyor.

## Mum sayısı - skor tablosu (fo2 kendi kendine test, iPhone)
| Algılanan mum | Sonuç |
|---|---|
| 13 | YANLIŞ birinci (Fo1 %76, fo2 %60) |
| 18 | doğru ama zayıf (fo2 %70, Fo1 %63, fark 7 puan) |
| 20 | doğru, fark geniş (fo2 %93, Fo1 %51) |
| 23 (orta mesafe) | fo2 %92, FO3 %38, fark 54 puan |
| 25 (çok yakın, tam) | fo2 %99 |
Sonuç: güvenilir okuma için en az 20 mum görünmeli. En iyi çekim: orta mesafe, ekrana paralel, grafik kutunun ortasında.

## Binance fotoğraf testi (30 Ekim, PARTIUSDT, açık tema)
- Sorun: üstteki kırmızı fiyat yazısı (0.05808 -2.02%) harf harf kırmızı mum sayılıyor, üstelik altındaki gerçek mumlarla birleşip boylarını bozuyordu. Kesikli fiyat çizgisi de aynı türden gürültü.
- Mobilde MA/fiyat çizgisi kapatılamadı, bu yüzden kodda süzme eklendi (removeAlignedNoise): üst ve alt hizası aynı (±2 px), fitilsiz, küçük parçalar 4 ve daha fazlaysa elenir. Birleştirmede dikey boşluk sınırı eklendi (uzaktaki parçalar tek mum olmuyor).
- Sonuç (aynı fotoğraf): 36 mumdan 30'a; sahte mumların çoğu gitti, gerçek mumlar korundu. Eksi işaretleri ve parantez gibi 2-3 parça hâlâ kalabiliyor: en iyisi fiyat yazısını kutunun dışında tutmak.
- Kütüphanedeki 3 referansın mum sayıları değişmedi (21 / 24 / 25).

## İlgisiz grafik testi (30 Ekim 04:24, iPhone, kütüphanede olmayan Binance grafiği)
- Sonuç: fo2 %33 (Formasyon %30, AI %98), FO3 %32, Fo1 %23. Algılanan 27, karşılaştırılan 23 mum.
- Bilgisayardaki aynı koşullu deneme de %29-35 verdi; telefon ve bilgisayar tutarlı.
- İlgisiz grafiklerde görülen en yüksek skor: %55. Doğru eşleşmeler (20+ mum): %92-99.
- Eşik önerisi: %70 altı "eşleşme yok". AI yine %97-99 sabit, ayırt etmiyor.
- Uyarı tutarsızlığı düzeltildi: 27 mum (çok iyi) görürken "taşıyor, uzaklaş" diyordu. Artık taşma, tek fitil değil kenarda kesilen mum gövdeleriyle ölçülüyor. Mum sayısı yeterliyse "uzaklaş" yerine "uzaklaşmana gerek yok, grafiği kutunun ortasına getir (üst/alt kenar)" diyor. Sayı azsa eskisi gibi uzaklaş der.

## Sağdan tarama (30 Ekim 04:30, kullanıcının ana kuralı)
- Kural: tarama her zaman EN SAĞDAKİ (en son) mumdan başlar, sola doğru referansın mum sayısı kadar mum alınır (F1: 21, F2: 24, F3: 25). Algılama hatası için boyut ±2 esner.
- Önceden pencere 7 mum sola kayabiliyordu (grafiğin ortasında benzer bir parça bulup yüksek skor verebiliyordu). Kaldırıldı (queryWindows).
- Test (bilgisayar, aynı fotoğraflar): referanslar kendileriyle yine %100. İlgisiz grafiklerin en yüksek skoru %55'ten %33'e düştü; doğru ile ilgisiz arasındaki fark büyüdü.
- Not: F1 ile F2 birbirine benziyor (çapraz skor %73-76).

## Yol haritası (30 Ekim)
- İlk adım ve öncelik: Binance fotoğraflarından TEMİZ ÖLÇÜM (mum sayısı ve şekli doğru okunsun).
- Farklı coinlerde test yapılacak; sonuçlar aşağıdaki tabloya yazılacak, eşik ve ayarlar bu verilere göre güncellenecek.
- İleride: daha net kamera (yeni telefon), daha iyi ekran parlaklığı, daha büyük mumlar (grafiği büyüterek). Bunlar gelince eşikler yeniden ölçülecek.
- Eşleşme yok eşiği (%70 önerisi) farklı coin testleri bitince kesinleşecek.

## Coin test tablosu
| Tarih | Coin | Algılanan mum | 1. sonuç | 2. sonuç | Görüntü notu |
|---|---|---|---|---|---|
| 30 Ekim | PARTIUSDT (ilgisiz) | 27 | fo2 %33 | FO3 %32 | eski kod (sağdan tarama öncesi) |

## Zincir testi: Binance fotoğrafı -> referans -> kamera (30 Ekim 04:57)
- formasyon_betik.py telefonla çekilmiş fotoğrafta ÇALIŞMIYOR: ~34 mumluk grafikte 45 mum buldu, ızgara çizgilerini fitil sandı (fitiller tüm yüksekliğe uzadı). Betik temiz dijital görseller için yazılmış. İleride fotoğraf modu eklenmeli.
- Bunun yerine referans, uygulamanın kendi okuma koduyla (detectCandles) üretildi: fotoğraftan 31 mum okundu, en sağdaki 25 mum temiz çizildi -> formasyonlar/test/BINANCE_TEST_temiz.png (okununca 25 mum, 13 yeşil 12 kırmızı).
- Bilgisayar sonuçları: grafiğin tamamı görününce %99 (diğer formasyonlar %32-48). Kutu grafiğin üstünü/altını kesince %47-71'e düşüyor. Ders: mumların tam boyu kutuda görünmeli.
- Zayıf nokta: bulanık fotoğrafta ince fitiller ile gövde karışıyor (doji'lerin fitili gövde sanılıyor).
- Sıradaki: kullanıcı bu referansı uygulamaya yükleyip aynı Binance ekranını canlı tarayacak.

## Canlı zincir testi sonucu (05:04) ve fitil/gövde düzeltmesi
- Telefonda BINANCE_TEST referansı BİRİNCİ çıktı ama %40 (FO3 %34). Doğru sıralama, düşük skor.
- Sebep 1: Kamera önizlemesinde kutular mumlardan çok uzundu: bulanık görüntüde fitil ile gövde tek parça okunuyor, mum gövdesi fitil boyunda sanılıyordu.
- Sebep 2: Grafik canlı (kısa zaman dilimi); fotoğraf 04:57, tarama 05:04. Yeni mumlar oluştuğu için sağ baş kaydı. Test için 4 saatlik/günlük grafik kullanılmalı.
- Düzeltme (splitWick): her parça satır satır taranıyor; en geniş satırın %60'ından geniş satırlar gövde, inceler fitil sayılıyor. Uzun fitilli doji'ler de artık kaybolmuyor.
- Bilgisayar sonucu: 3 referans kendileriyle yine %100; fotoğraf kendi referansıyla %99; kutu kesik çekimde %71 -> %79.

## Fotoğraftan referans üretme (önemli karar, 30 Ekim)
- Zincir testinin 2. adımında eski betik (formasyon_betik.py) kullanılmadı, çünkü telefonla çekilmiş fotoğrafta çalışmadı.
- Bunun yerine uygulamanın kendi okuma kodu (detectCandles) kullanıldı: fotoğraf okundu, en sağdaki 25 mum kütüphane biçiminde temiz çizildi (beyaz zemin, kırmızı/yeşil mum, fitil mum renginde).
- Amaç aynı: fotoğrafı kütüphane formasyonlarıyla aynı biçime getirmek. Yani bu yöntem fiilen FOTOĞRAF İÇİN YENİ BİR BETİK gibi çalıştı.
- Faydası: kamera ve referans aynı okuma kodundan geçtiği için iki taraf aynı dili konuşuyor.

## Karar (30 Ekim 06:23)
- Büyük tarama alanı: daha net çekim, tüm mumlar tek görüntüde; başka telefonda da en geniş alan kullanılır.
- Fotoğrafı kütüphane biçimine getirmek orijinal okumayı bozmaz.
- Karşılaştırma (zaman ve mum etkisi) en son ele alınacak.

## Not: BINANCE_TEST referansı
- formasyonlar/test/BINANCE_TEST_temiz.png sadece zincir testi için üretildi. Kütüphane formasyonu DEĞİL, kütüphaneye eklenmeyecek.
- Uygulamaya test için yüklendi; sonuç zaman aşımı (grafik akmaya devam etti) yüzünden tutarsız çıktı. Uygulamadan silinebilir.

## GEÇİCİ test bölümü (30 Ekim 06:45) — testler bitince KALDIRILACAK
- Okuyucu.html'de "🧪 Çekilen Resim (geçici test)" kartı ve "Test Görüntüsü Kaydet" düğmesi.
- Üç görüntü üretir: 1) kameranın tam karesi, 2) yeşil alanın taradığı kısım (502x277), 3) okunan mumların numaralı çizimi. Ayrıca okunan mum sayısı, kamera çözünürlüğü ve alan oranı yazılır.
- Amaç: sitenin gördüğü görüntüyü telefonun kendi kamerasıyla çekilen fotoğrafla karşılaştırmak (sorun sitede mi, sahnede mi) ve bulanıklık eşiğini gerçek görüntülerle ayarlamak.
- Kaldırmak için: HTML'deki "GEÇİCİ TEST BÖLÜMÜ" yorumu ile işaretli kart ve JS'deki "GEÇİCİ TEST BÖLÜMÜ" bloğu silinir.

## 30 Ekim gece testi (PARTIUSDT 15m) — özet
- Telefon fotoğrafı keskin, okuyucunun karesi bulanık. Gerçekte ~33 mum, okuyucu 23 buldu (önceki testte 25).
- 19. bölgede birkaç küçük mum tek kutuya birleşti (en büyük hata). 6–18 arası yapı iyi okunuyor. Eşleştirme yüzdesine dokunulmayacak.
- Sebep: bulanıklık mumlar arasındaki boşluğu siliyor. Çözüm: keskin girdi + akıllı ayırma.

## 31 Ekim: yeni büyük ekran, 1x/2x karşılaştırma, fotoğraf modu
- Artık daha büyük ve net bir ekran kullanılıyor. Binance'te MA/EMA ve VOL kapalı.
- Telefonun kendi kamerasıyla 2x çekim 1x'ten çok daha iyi: mumlar büyük, aralar açık (~36-38 mum ekranda).
- Okuyucu.html'e eklendi:
  - Canlı kamerada 1x/2x düğmeleri (yalnızca tarayıcı zoom desteği verirse görünür; desteklenmiyorsa not çıkar).
  - "📸 Fotoğraf Çek / Seç ve Oku": iPhone kamerası ya da galeriden fotoğraf. Grafik alanı otomatik bulunur (kırmızı/yeşil piksel içeren en uzun dikey bölge), sağda boşluk bırakılır, yeşil kutuya yerleştirilir; aynı okuma kodu çalışır. Test bölümü 3 görüntüyü otomatik üretir.
- Geçici test bölümü kullanıcı isteğiyle KORUNUYOR.
- Bilgisayar sonucu (aynı fotoğraflar, fotoğraf modu): 2x fotoğraf 41 mum, VOL kapalı 2x fotoğraf 34 mum. Büyük mumlar doğru ayrılıyor.
- Kalan hatalar (sıradaki iş = ayırma düzeltmesi): (1) gövdesi neredeyse olmayan çok küçük doji'ler ("+" / "T") kaçıyor; (2) yan yana iki yeşil mum bazen tek kutu oluyor. İkisi de en sağ (en önemli) bölgede görüldü.

## 31 Ekim 03:45 — Yeşil alan tam ekran + ayırma düzeltmesi
- Kamera alanı 1,2:1, yeşil alan kamera alanının tamamı (%3 pay). Karşılaştırma dikey ölçekten bağımsız olduğu için oran zorlanmıyor; okuma sıkıştırmasız (genişlik 502).
- Test (BTCUSDT 15m, büyük ekran, site test görüntüleri): kutular mumlara tam oturuyor; ekran görüntülerindeki kayma hareketten. 1x: 22 mumun hepsi doğru (yalnız küçük "T" kaçtı). 2x: 29 gerçek mumdan 25.
- 2x'te ekran piksel deseni (dikey çizgiler) belirgin; biraz uzaktan çekmek iyi. Çerçeve sık sık aşağı kayıyor: grafik alanın ortasında olmalı.
- Ayırma düzeltmesi (Okuyucu.html, "AYIRMA DÜZELTMESİ"):
  - splitWideBodies: ortanca gövde genişliğinin 1,6 katından geniş kutu bölünür (gövde kenarı sıçraması / seyrek sütun).
  - addDojis: mumlardan uzakta kalan dikey fitil izinde en dolu satır = "+" / "T" doji gövdesi.
  - mergeBodyCandidates: gövdenin üstünde/altında duran ince fitil parçası artık gövdeye eklenmiyor (gövdeler fitil boyunda uzuyordu).
  - Başka mumun gövde aralığındaki dar parça (fitil) ayrı mum sayılmıyor.
- Sonuç: 2x test 25 -> 28 (kalan tek eksik kenarda yarım doji), 1x test 22 -> 23 (hepsi doğru). Kütüphane referansları değişmedi (21/24/25).

## 31 Ekim 04:05 — Tek parmak kontrol çubuğu
- Sorun: Tara ve Test Kaydet düğmeleri aşağıdaydı; kaydırınca kamera yukarı çıkıyor, görüntü yakalanırken telefon sabit tutulamıyordu.
- Çözüm: kameranın hemen altına tek sıra kontrol çubuğu: [1x] [2x] [📸 Kaydet] [🧠 Tara]. Kaydırmadan erişilir.
- "📸 Kaydet" test görüntülerini kaydeder (sonuçlar aşağıdaki test kartında), düğmede kısa süre "✅ N mum" görünür.
- Testlerden ders: netlik mum boyutundan önemli. Keskin 2x çekim 35/35 doğru; bulanık yakın çekimde 26'dan 25 ve fitil gövde sanıldı. Sıradaki iş adayı: bulanıklık uyarısı.

## 31 Ekim 04:20 — Bulanıklıkta merdiven birleşmesi
- Sorun: el sarsıntısıyla bulanık karede ardışık aynı renk mumlar (örneğin 5 kırmızı düşüş mumu) çapraz olarak birbirine değip tek dev parça oluyordu; parça çok geniş olduğu için tamamen eleniyordu (5 mum birden kayıp).
- Çözüm: genişliği tuvalin %10–40'ı arasındaki parçalar atılmıyor, ortanca gövde genişliğine göre bölünüyor (splitWideBodies + medOverride).
- Sonuç: bulanık test 21 -> 25; diğer testler ve kütüphane referansları değişmedi.
- Denenip GERİ ALINAN: yeşil ton sınırını 178 -> 195 genişletmek (çok ince "T" camgöbeği görünüyor). Diğer testlerde hata artırdı.
- Gözlem: çerçeve sık sık sağ üste kayıyor; son mumun üstünde/sağında boşluk bırakmak gerekiyor.

## 31 Ekim 04:25 — Kayma kontrolü ve net kare seçimi
- Kullanıcı gözlemi: Tara/Kaydet'e basınca çekilen kare, önizlemeye göre hep aşağı yönde kayıyor; basınca beklemek gerekiyor.
- Kontrol (bilgisayar, sahte kamera deseni, iPhone ekran boyutu): önizleme ile kaydedilen kare arasında kod kaynaklı kayma YOK (merkez farkı ~%0,2).
- Sebep: düğmeler ekranın alt yarısında; basmak telefonu eğiyor, site tam o anki kareyi alıyordu (kayma + hareket bulanıklığı).
- Çözüm (captureBest): basınca 0,45 sn beklenir, sonra ~0,6 sn içinde 6 kare alınır, en net olan (gradyan enerjisi) kullanılır. Kaydet ve Tara ikisi de bunu kullanıyor. Test bilgisinde "Netlik" değeri yazıyor (bulanıklık eşiği ayarı için veri).

## 31 Ekim 04:32 — Dokunmadan ÖNCEKİ kareyi kullan
- 04:25 yöntemi (basınca 0,45 sn bekle, sonra çek) ters tepti: kullanıcı dokununca telefonu indiriyor, site grafiğin altını (VOL/MACD yazıları, -1,90%) çekti.
- Yeni yöntem: kamera açıkken son ~1 sn'nin kareleri sürekli tutuluyor (120 ms'de bir, 9 kare). Kaydet/Tara'ya parmak DEĞDİĞİ andan önceki karelerin en neti kullanılıyor. Sonuç anında; dokunuş ve sonrasındaki hareket etkilemiyor.
- Not: kırmızı "-1,90%" yazısı kırmızı mum sayıldı (12 sahte mum); yazıları alan dışında tutmak gerekiyor.

## 31 Ekim 04:42 — Anında önizleme
- Kaydet/Tara sonrası yakalanan kare, okunan mum kutularıyla kamera alanında 2 sn donuyor; sensör şeridinde "⏸ Yakalanan kare: N mum". Kaydırmadan kontrol için.
- 04:39 ilk deneme testi: keskin, 23 mumdan 22 doğru. Tek hata: ekrandaki fare imleci yeşil mum sayıldı -> çekimden önce imleci grafik dışına al. Çerçeve hâlâ biraz yukarıda (son mumlar üst kenara değiyor).

## Karar (31 Ekim 04:49): 1x çalışması
- Şimdilik 2x ana yöntem (25–35 mum için ideal; kütüphane formasyonları 21–25 mum).
- 1x ileride uzun formasyonlar (40–60 mum) için gerekecek. Sıra: ÖNCE uzun formasyonlar bulunacak, SONRA 1x çalışması yapılacak.
- 1x çalışmasında yapılacaklar: o mum sayısıyla 1x test, okuma doğruluğunu ölç, gerekirse ayırma kodunu küçük mumlara göre ayarla; gerekirse 1,5x düğmesi ekle.
- Bilinen sınır: 1x'te ~30 mum iyi (22/22), ~56 mumda kutular karışıyordu.

## KARAR (31 Ekim 05:08): Karşılaştırma büyük resimde, kanallarla
- Mum mum birebir eşleşme gerçekçi değil. Karşılaştırmada kanal içindeki küçük farklar yok sayılacak; formasyon büyük resimde yakalanacak: kanalların sırası, yönü/eğimi ve oranları (inen → yatay → yükselen gibi).
- Aranan formasyonlar Smart Money yapıları. Formasyonun ilk büyük kısmı (yaklaşık 2/3) büyük ölçüde tutmalı; kalan kısım hareket edilecek yönü gösterir.
- KESİM KURALI (kullanıcının yöntemi): mumlar, gerçek yukarı hareketin başladığı yerden 2 mum sonra kesildi. Amaç: formasyonun başladığından emin olmak ve harekete geçtiği anı yakalamak. Kesilen mumlar = hareket edeceğimiz alan (karşılaştırmaya girmez, sonuçta beklenen hareket olarak gösterilir). Mevcut kesimler (F1: 5, F2: 8, F3: 5) bu kurala göre yapılmış, AYNEN kalıyor.
- Kanal denemesi (tam formasyonlar, sitenin okuma koduyla, otomatik):
  - F1 Liquidity Sweep: İnen (1–10) → dik iniş/iğne (11–14) → Yükselen (15–26). Yatay taban yok.
  - F2 Order Block: İnen (1–10) → Yatay taban (11–23) → Yükselen (24–32). Kullanıcının elle çizimiyle birebir aynı.
  - F3 BOS: Yumuşak inen (1–16) → Yatay (17–24) → Yükselen (25–30).
- Sıradaki adımlar: (1) kanal bulmayı siteye ekle ve kamera görüntüsüne çiz; (2) karşılaştırmayı kanal dizisine geçir (eski mum mum karşılaştırma bir süre yanında kalsın); (3) sonuçta "aşama" ve kesilen kısmı beklenen hareket olarak göster (hayalet çizim en son).
- Not: son kısım geçmişte formasyonun nasıl tamamlandığını gösterir, her seferinde aynı yönü garanti etmez.

## 31 Ekim 05:15 — Kanal tabanlı karşılaştırma eklendi (ilk sürüm)
- Okuyucu.html "KANAL TABANLI KARŞILAŞTIRMA": findChannels (mumları en uygun kanallara böler; kanal içi küçük farklar yok sayılır), channelProfile (kanal orta çizgisi 24 noktaya örneklenir + her noktanın yönü: inen/yatay/yükselen), channelMatch (canlı pencere en sağdan, referans mum sayısının %75–130'u arasında esner; en iyi uyan alınır).
- Skor = %60 kanal çizgisinin şekli + %40 kanal yönlerinin sırası. ANA SKOR artık kanal skoru; mum mum skor yanında gösteriliyor ("Kanal X% • Mum Y%"). Sonuç kartında grafiğin ve formasyonun kanal dizisi yazıyor.
- Bilgisayar testi (kesilmiş referanslar):
  - Kendisiyle %100. F2 tabanı 4 mum uzatılınca %92, düşüşü 3 mum kısaltılınca %87 (mum sayısı serbestliği çalışıyor).
  - İlgisiz BTC grafikleri: %28–53.
  - Zayıf nokta: kesilmiş F1 ile F3 birbirine benziyor (%76–82); ikisi de kesimden sonra "inen → yükselen" görünüyor. Ayrım için ileride kanal eğimi/derinliği ağırlığı artırılabilir.
- Sıradaki: kanalları kamera görüntüsüne/test görüntüsüne çizmek (drawChannels hazır), telefonda Tara ile test, eşik belirleme.

## ▶ KALDIĞIMIZ YER (31 Ekim 05:15) — sonraki oturumda buradan başla
**Bu gece tamamlananlar**
- Yeni büyük/net ekran + Binance'te MA/EMA ve VOL kapalı.
- Canlı kamerada 1x/2x (Safari gerçek zoom destekliyor, 1–10). 2x ana yöntem.
- Yeşil alan tam ekran (kamera alanı 1,2:1). Kamera altında tek sıra: [1x][2x][📸 Kaydet][🧠 Tara]; altında [Kamerayı Aç][Fotoğraf Oku].
- Okuma düzeltmeleri: birleşen mumları bölme, "+"/"T" doji bulma, fitilin gövdeye eklenmemesi, bulanıklıkta merdiven birleşmesini bölme.
- Çekim: dokunmadan ÖNCEKİ son 1 sn'nin en net karesi kullanılıyor; yakalanan kare 2 sn donuyor ("⏸ Yakalanan kare: N mum").
- Sonuç: keskin 2x çekimde 26/26 ve 24/24 doğru okuma.
- Kanal tabanlı karşılaştırma ilk sürümü yayında (ana skor), mum mum skor yanında.

**Kararlar**
- Karşılaştırma büyük resimde, kanallarla (inen/yatay/yükselen); küçük farklar yok sayılır.
- Kesim kuralı: yükselişin başlangıcı + 2 mum; kesilen kısım = hareket edeceğimiz alan. Mevcut kesimler aynen kalıyor.
- 1x çalışması: önce uzun (40–60 mum) formasyonlar bulunacak.
- Geçici test bölümü ve Fotoğraf Oku düğmesi kalıyor.

**Sıradaki adımlar**
1. Telefonda 2x'te 🧠 Tara testi: sonuç kartındaki "Kanal %", "Grafik: …" ve "Formasyon: …" satırlarını kontrol et (ilgisiz BTC grafiğinde düşük skor bekleniyor).
2. Kanalları kamera görüntüsüne ve test görüntüsüne çiz (drawChannels hazır, bağlanmadı).
3. F1 ile F3 ayrımını güçlendir (kesilmiş hâlleri benzer: %76–82).
4. "Eşleşme yok" eşiğini kanal skoruyla belirle.
5. Sonuçta aşama + kesilen kısmı beklenen hareket olarak göster; hayalet çizim en son.

**Çekim ipuçları**: 2x, grafik ortada, son mumun üstünde/sağında boşluk, fare imleci grafik dışında, ✅ görünce telefonu indir.

## KARAR (31 Ekim 06:45): Kanal dışına taşma sınırı — TÜM kanallar için
- Kanal içi serbest: mumlar çizgiye değebilir, ortada kalabilir, aşağı yukarı oynayabilir.
- SINIR: kanal dışına taşma. Gövde taşması en fazla %20 (kullanıcı kararı). Fitil taşması daha serbest (~%35 önerisi; Spring/likidite alımı fitil taşmasıdır). Kanal genişliğinin yarısından fazla taşma = kırılım (yeni kanal başlar).
- Uygulama için kanal çizgileri uç mumlara göre değil çoğunluğa göre çizilecek (şu an uç mumlara göre, taşma hep %0 çıkıyor). HENÜZ KODA EKLENMEDİ.
- Ölçülen kanal içi sapma (gövde ortası / kanal yarı genişliği): eski F1–F3 %17–19 (fazla temiz), gerçek BTC çekimleri %26–36.

## 31 Ekim 06:50 — 6 yeni formasyon taslağı (kütüphaneye EKLENMEDİ, onay bekliyor)
- W1 Wyckoff Birikim Spring'li (31/kesim 7), W2 Spring'siz (30/6), OB Retest (26/6), CHoCH Dönüşü (25/5), BOS Devamı (26/6), W1d Dağıtım UTAD'lı (31/7, W1'in aynası). Kesim kuralı: yükselişin başı + 2 mum.
- Çizimler sitenin kamerayla okuduğu gerçek grafiklerin mum istatistiklerine göre ayarlandı (kanallardan bağımsız):
  | ölçü | gerçek çekim | yeni çizim |
  | gövde/aralık medyan | %8,8 | %8,6 |
  | doji oranı | %19 | %13 |
  | fitil medyan / p90 | %1,4 / %6,5 | %1,9 / %6,3 |
  | trend içinde ters renkli mum | %33 | %33 |
  | gövde genişliği/aralık | 0,84 | 0,76 |
  Çizim düzeni sitenin temiz çizimiyle aynı (kenar payı 30/22 px, gövde ≤15 px).
- Okuyucu her çizimde mum sayısını doğru okuyor. Benzerlik uyarıları: CHoCH ↔ F1 %91, W2 ↔ eski F2 %91, BOS ↔ Dağıtım %79.
- Üretici: scratchpad yeni/uret.py (depoya alınmadı).

## 31 Ekim 06:58 — Hazır kütüphane + LO/SH etiketleri
- Depoda formasyonlar/kutuphane/: karşılaştırmada kullanılan KESİLMİŞ hâller (hareket alanı çıkarılmış) + liste.json. Tam hâller formasyonlar/kutuphane/tam/.
- Ad kuralı: yukarı yön = LO (yeşil ▲), aşağı yön = SH (kırmızı ▼). Sonuç kartında, eşleşme listesinde ve kütüphanede renkli etiket olarak görünüyor.
- Sitede "📚 Hazır Kütüphaneyi Yükle" düğmesi: liste.json'daki formasyonları ekler (aynı adlı olanı tekrar eklemez). Telefondaki eski referanslar silinmez; istenirse "Tüm Referansları Sil" sonra yükle.
- Kütüphane (9): LO 01 Liquidity Sweep, LO 02 OB Retest (eski), LO 03 BOS (eski), LO 04 Wyckoff Birikim Spring'li, LO 05 Wyckoff Birikim Spring'siz, LO 06 OB Retest, LO 07 CHoCH Dönüşü, LO 08 BOS Devamı, SH 01 Wyckoff Dağıtım UTAD'lı.
- Bilgisayar testi: LO 04 görseli Fotoğraf Oku ile tarandı -> 1. LO Wyckoff Birikim (Spring'li) %100, 2. %67.
- Açık konu: benzer çiftler (LO 05 ↔ LO 02 %91, LO 07 ↔ LO 01 %91) kullanıcı kararı bekliyor.

## 31 Ekim 07:20 — LO 09 Kahve Fincanı (Cup and Handle) eklendi
- Tanım (William O'Neil, How to Make Money in Stocks; StockCharts ChartSchool): önce yükseliş (devam formasyonu), U şeklinde yuvarlak dip (V değil), fincan derinliği önceki yükselişin ~1/3'ü (en fazla 1/2–2/3), sağ kenar sol tepeye yakın döner, kulp: kısa, hafif aşağı eğimli geri çekilme (fincan yükselişinin ~%30–50'sinden az), kırılım kulp direncinin üstü (hacim artışıyla).
- Çizim: 34 mum, kesim 5 (kulp kırılımı + 2 mum). Kanallar: Yükselen → İnen → Yükselen. En yakın: BOS Devamı %78.
- Kullanıcı notu: daha önce görüp denedi, işe yarıyor.

## Zaman dilimi (31 Ekim 07:20)
- Kütüphane çizimleri ŞEMATİK: belirli bir zaman dilimine bağlı değiller, mum sayısıyla tanımlı. SMC/Wyckoff ve Cup and Handle tanımları her zaman diliminde kullanılıyor (fraktal kabul).
- Ancak klasik tanımlar (O'Neil Cup and Handle: fincan 1–6 ay, kulp 1–4 hafta) GÜNLÜK/HAFTALIK grafiklerden geliyor; düşük zaman diliminde gürültü daha fazla, güvenilirliği bağımsız olarak kanıtlanmış değil.
- Kullanıcı tercihi: 15 dk. Bilimsel yaklaşım: her testte zaman dilimini kaydet (coin test tablosuna sütun), ileride 5/15/30 dk ve 1 sa için sonuçları karşılaştır.

## ▶ YARIN (1 Kasım) — SH (short) formasyonları
- Kullanıcı kararı: SH formasyonları LO'dan DAHA FAZLA olacak. Gerekçe (kullanıcı): düşenin çıkması uzun sürer; çıkanın düşüşü daha net ve sert olur; manipülasyon ve volatiliteden daha uzak bir yaklaşım.
- SH formasyonları AYNALANMAYACAK; kendi tanımlarıyla araştırılıp ayrı çizilecek (düşüşler daha hızlı/sert, tepeler daha geniş/dalgalı). Mevcut SH 01 (aynalama ile yapıldı) yeniden çizilecek.
- Araştırılacak/çizilecek aday liste: Wyckoff Dağıtım (UTAD'lı, UTAD'sız), düşüş Order Block Retest, düşüş CHoCH, düşüş BOS devamı, Ters Kahve Fincanı, İkili Tepe, Omuz-Baş-Omuz, likidite alımı (tepe üstü iğne) + düşüş.
- Kesim kuralı aynı: düşüşün başladığı yer + 2 mum; kesilen kısım = hareket alanı.
- Kullanıcıdan istenen: düşüş yaşanmış 2–3 Binance grafiğinden site test görüntüleri (2x, 15 dk), düşüş mumlarının istatistiğini ölçmek için.
- Sonra: kanal dışına taşma sınırını (%20 gövde) koda eklemek; sonuçta "yön özeti" (ilk 5 eşleşmede LO/SH sayısı).

## 31 Ekim 23:30 — Çekim önerisi: 1x mi 2x mi?
- Okuyucu.html: kamera düğmelerinin altında "📐 Çekim önerisi" kutusu. SADECE öneri; kamera, mum sayımı ve çekim işlemlerinde değişiklik YOK (kullanıcı kararı).
- Kural (kullanıcı): kütüphanedeki formasyon 33 mumdan fazlaysa 1x, değilse 2x önerilir. Önerilen zoom düğmesi yeşil çerçeveli olur; seçim kullanıcıda. Kutu kaç formasyonun 2x / 1x olduğunu ve Fotoğraf Oku için iPhone lensini yazar.
- 1x için düzeltmeler ileride yapılacak.
- Bilgisayar testi: mevcut 10 formasyon → 2x (en uzun 29 mum); 77 mumluk XAUUSD QM eklenince → 1x.
- Öncelik (kullanıcı): kütüphanedeki kesme işlemi ve kanal boylarını yerleştirmek. QM ortak 9 görsel (TradingView + ForexFactory) kırılım kontrolü sürüyor.
- Kullanıcı kararı (31 Ekim 23:53): QM hızlı / yavaş (normal) retest ayrımı ya KENDİLİĞİNDEN (kütüphanede ayrı formasyonlar, karşılaştırma ayırt eder) ya da KULLANICI SEÇİMİYLE (taramadan önce "Hepsi / Hızlı retest / Normal QM") yapılacak. Kodlama sonra; kamera ve mum sayımına dokunulmayacak.

## 1 Kasım 03:30 — QM kütüphanesi: 01 tamamlandı, işlem kaydı
- Yöntem ve hata kayıtları: araclar/qm_kutuphane/ISLEM_KAYDI.md (betikler aynı klasörde). Orijinal görseller depoda yok.
- 01 (Nora GBPUSD 1G, SH): 52 mum (gizli mum eklendi), kesim kullanıcı numarasıyla 58 dahil. Kanal yöntemi kesin: en uç gövdeler + kanal genişliğinin %20'si dışarı, paralel kesikli çizgi; kanallar json'da, görselde değil.
- Kütüphane dosyası site formatında (502×277); sitenin kendi okuma koduyla 52/52 doğrulandı.
- 02 düşük çözünürlük (~200 mum / 625 px): büyük orijinal bekliyor. Sırada 03.

## 1 Kasım 03:45 — Arayüz düzeltmeleri (kullanıcı isteği)
- 1x / 2x: yeşil çerçeve artık KULLANICININ SEÇİMİNİ gösteriyor (önceden hep öneriyi, 2x'i gösteriyordu). Düğmeler her zaman seçilebilir; seçim öneri kutusunda "Seçimin: 1x (öneri 2x)" olarak yazar ve Fotoğraf Oku için iPhone lensi buna göre söylenir. Kamera zoom'u yalnızca tarayıcı canlı zoom destekliyorsa uygulanır (önceki davranış aynı).
- "🖼️ Fotoğraf Oku" düğmesi "Referans Formasyon Ekle"nin yanına taşındı; "Kamerayı Aç" tek başına tam genişlikte.
- Kamera, mum okuma ve çekim kodunda değişiklik yok.

## 1 Kasım 04:20 — Formasyon Hazırla, Adım 1: numaralama
- Okuyucu.html'de yeni kart "🛠️ Formasyon Hazırla" (kütüphane kartının üstünde). Kamera / mum okuma / Tara koduna dokunulmadı; mevcut fonksiyonlar sadece çağrılıyor.
- Yol Fotoğraf Oku ile birebir aynı: findChartBox → buildStill → tam kare (kamera kutusu oranı) → captureScanRegion → detectCandles. Ortak tuvaller (stillCanvas, SCAN_OUT_H) işlem sonrası eski hâline döner.
- Numaralı görüntü gerçek boyutta, yatay kaydırılabilir, en sağdan açılır. Muma dokununca silinir (✕), tekrar dokununca geri gelir; "Silmeleri Geri Al" düğmesi. Bilgi satırı: okunan / silinen / kalan mum, 33 üstü ise 1x notu.
- Doğrulama (bilgisayar): Hazırla ile Fotoğraf Oku aynı mum sayısını veriyor — iPhone BTC fotoğrafı 50/50, site karesi 58/58, 01 temiz 52/52.
- Sıradaki: eksik (gizli) mum ekleme, sonra Adım 2 kesim yerleri.
- 04:30 düzeltme (kullanıcı geri bildirimi: okuma sonucu ve silme düğmesi görünmüyordu): bilgi satırı büyük ve kalın ("✅ Okunan: N mum"); görüntü sadece mumların olduğu yüksekliğe kırpılıyor; numaralar iki sıra (üst üste binmiyor); muma dokununca SARI seçilir, altında "🗑️ Seçili Mumu Sil" ve "↩️ Tüm Silmeleri Geri Al" düğmeleri; dokunma en yakın muma (mum aralığının %75'i içinde) gider.

## 1 Kasım 04:50 — Formasyon Hazırla: net gösterim, çoklu silme, Adım 2
- Kullanıcı geri bildirimi: görüntü bulanık, silme tek tek ve kullanışsız, sonraki adıma geçiş yok.
- NET GÖSTERİM: okuma yine Fotoğraf Oku yolundan (502 genişlik, kamerayla aynı) yapılıyor; ama numaralar ORİJİNAL görselin üstüne çiziliyor. Tarama koordinatları buildStill / tam kare / yeşil alan geometrisiyle orijinale geri çevriliyor (hzStillGeom + hz.map). Görüntü yüksekliği en fazla ~440 px, mum başına ~20 px, yatay kaydırma, en sağdan açılır.
- Mod düğmeleri: ✂️ 1. Sahte Mum / 🟢 2. Başlangıç / 🔴 2. Kesim.
- Sahte mum: çoklu seçim (sarı), "Aralık seç" kutusu (iki muma dokun → aradakilerin hepsi), "Seçilileri Sil (n)", "Seçimi Temizle", "Silmeleri Geri Al".
- Adım 2: başlangıç mumu yeşil numara, öncesi gri; kesim mumu kırmızı numara (DAHİL), sonrası sarı + kesikli kırmızı çizgi. Özet: "Formasyon: a → b (kesim dahil) = N mum → 1x/2x • Devam: M mum". Numaralar silinen mumlar çıkarıldıktan sonraki sırayla.
- "➡️ Adım 3: Kes ve Temiz Çiz" düğmesi görünür ama henüz pasif (sıradaki iş).
- Test (bilgisayar): BTC iPhone 50 mum, 01 temiz 52 mum; aralık silme, başlangıç/kesim seçimi çalışıyor; hata yok.

## 1 Kasım 05:10 — Formasyon Hazırla: Adım 1–3 (kullanıcı geri bildirimi sonrası)
- Kaydırma sabit: tuval bir kez oluşturuluyor, dokunuşta yeniden çiziliyor (görüntü sola kaymıyor). En sağdan açılıyor.
- Numaralar altta tek şeritte (iki sıra), mumdan şeride ince kılavuz çizgi; dokunulan SÜTUNDAKİ mum seçilir (tam mumun üstüne basmak gerekmez).
- 4 mod: ✂️ Sahte Mum (tek tek) / ↔️ Aralık Sil (iki mum: ilk ve son → aradakilerin hepsi) / 🟢 Başlangıç / 🔴 Kesim. Yönerge satırı her modda ne yapılacağını söylüyor.
- Adım 3 "Kes ve Temiz Çiz" çalışıyor: başlangıç–kesim arası (silinenler hariç) kütüphane biçiminde 502×277 çizilir (gövde = mum aralığının %72'si, birleşme olmasın); site kendi okuma koduyla tekrar okur ve "N/N ✓ birebir" yazar. Mum verisi (form) ve devam kısmı bellekte tutulur (kaydetme Adım 5).
- Test: BTC iPhone fotoğrafı 21→45 = 25 mum, tekrar okuma 25/25.
- Not: üstüne çizgi/yazı eklenmiş görseller (kırılım işaretli hâller) sahte mum üretir; Hazırla'ya ORİJİNAL görsel verilmeli.
- Sırada: Adım 4 (%20 kanallar), Adım 5 (kaydet).
- 05:05: Kullanıcı ekranında görüntü çok uzundu (dar görsellerde grafik ekranı kaplıyordu, numaralar en altta kalıyordu). Gösterimde yatay ve dikey ölçek ayrıldı: grafik yüksekliği en fazla ~300 px; okuma etkilenmez. Kullanıcı: "resim çektik, numara tamam".
- 05:15: Kullanıcı kesimi seçti ama başlangıcı seçmediği için Adım 3 düğmesi çıkmadı; sahte mum modunda sarı seçtiği mumlar kesim modunda da sarı görünüp karışıklık yarattı. Düzeltme: başlangıç İSTEĞE BAĞLI (seçilmezse ilk mum); kesim seçilince Adım 3 düğmesi çıkar. Sarı seçim yalnızca silme modlarında gösterilir; silinmemiş seçim varsa uyarı yazar.
- 05:25 Kesim ÖNERİSİ (kullanıcı isteği: site önersin, karar kullanıcıda): hareket adayı = gövdesi ≥ 1,8 × ortanca gövde ve sonraki 4 mumda aynı yönde net yol ≥ 4 × ortanca gövde. En güçlü 3 aday düğme olarak sunulur ("⭐ Kesim N — ▲/▼ M'de başlıyor"), kesim = hareket başı + 2. Kullanıcı birini seçer ya da 🔴 Kesim moduyla kendisi seçer.
- Adım 3 sonrası: "✅ Kesme bitti" + kesimin sağında mum varsa "⚠️ N mum formasyona girmedi, devam olarak saklandı" uyarısı; işlem durmaz.
- Bilinen sınır: çok sıkışık formasyonlarda (ör. 73 mum / 502 px) temiz çizim tekrar okununca birkaç mum eksik çıkabiliyor (73→70). 60 mum üstü formasyonlar zaten seçim ölçütü dışında.
- 05:35 Kullanıcı: "kesimin sağında 11 mum var diye bilgi verip ilerlemiyor". Sebep: Adım 4 düğmesi yoktu ve uyarı engel gibi görünüyordu. Düzeltme: uyarı mavi bilgi notu ("Sorun değil, devam et ↓") + "➡️ Adım 4: %20 Kanallar" düğmesi.
- Adım 4: kesilmiş temiz çizim sitenin kendi okumasıyla tekrar okunur; kanal bölümleri sitenin findChannels'ı ile önerilir (Tara'daki kanal karşılaştırmasıyla aynı mantık). Her kanalda gövde ortalarına doğru, en uç gövdelere paralel üst/alt sınır + kanal genişliğinin %20'si dışarı; kesikli çizgi (mavi yükselen, mor inen, turuncu yatay). Fitil taşmaları % olarak listelenir. Kanallar hz.clean.channels verisine yazılır (görsele değil). Test: Nora 01 → 4 kanal, taşma 0.
- Sırada: kanal sınırlarını kullanıcının düzeltebilmesi, Adım 5 Kaydet.
- 06:30 Kullanıcı: Kaydet düğmesi yok; kanal adımında sağdaki mumlar görünmüyor ve uyarı yok. Düzeltme: Adım 4 görüntüsü formasyon + devamı birlikte gösterir (devam sarı, kesikli kırmızı çizgi); kesim son mum değilse "⚠️ Kesim (a) son mum (b) değil: sağda N mum var → devam olarak kaydedilir". Kanal verisi yine yalnızca formasyondan hesaplanır.
- Adım 5 Kaydet: LO/SH seçimi + ad → telefondaki kişisel kütüphaneye (localStorage). Kayıt: temiz görsel (Tara bunu okur) + hazir:{mum, kanallar, devam, tarih}. Depoya/siteye girmez. Test: BTC fotoğrafı 31 mum, 3 kanal, devam 19 → kütüphanede görünüyor.
- Sırada: kanal sınırını kullanıcının düzeltmesi; Tara'da %20 eleme kuralı (hazir.kanallar kullanılarak).
- 06:35 Kullanıcı kararı: "Aralık Sil (iki mum)" kaldırıldı. Sahte mum yalnızca tek tek; sağ tarafı ayırmak için kesim yeterli. Modlar: ✂️ Sahte Mum / 🟢 Başlangıç / 🔴 Kesim.

## 1 Kasım 06:50 — Tara'da %20 kanal elemesi
- Yalnızca Formasyon Hazırla ile kaydedilmiş formasyonlarda (ref.hazir). Kamera / mum okuma koduna dokunulmadı.
- Yöntem: algılanan mumlardan en sağdaki N (formasyonun mum sayısı) alınır → kütüphane biçiminde yeniden çizilir (hzCleanDraw) → sitenin okumasıyla okunur → her gövde kendi kanalının %20 paylı sınırları içinde mi bakılır. İçeride kalan oran < %80 (KANAL20_ESIK) ise formasyon ELENİR (skor 0). Az mum varsa "az mum (a/N)" yazar, elemez.
- Sonuç ekranı: "✅ %20 kanal 29/31" ya da "❌ ELENDİ %20 kanal 10/31".
- Test (bilgisayar): iPhone BTC fotoğrafından iki formasyon kaydedildi (son 31 mum = aynı, ilk 31 mum = farklı).
  - Aynı fotoğrafla tarama: aynı 31/31 ✅ %100; farklı 12/31 ❌ elendi.
  - Aynı grafiğin SİTE KAMERA karesiyle tarama: aynı 29/31 ✅; farklı 10/31 ❌ elendi.
- Eşik (%80) ilk değer; gerçek testlerle ayarlanacak.

## 1 Kasım 07:10 — Karşılaştırma kanal içinde + tahmin (kullanıcı isteği)
- Kanal verisi olmayan formasyonlar (Hazır Kütüphane, eski referanslar) için kanallar Tara sırasında OTOMATİK hesaplanıyor (Adım 4 ile aynı yöntem, gövde + %20); sonuçta "(kanal otomatik)" yazar.
- Skor artık kanal içinde: pencere (en sağdan N mum) ve formasyon aynı biçimde yeniden çizilip okunur → içeride oranı (%20 paylı sınırlar) + hareket uyumu (ardışık gövde ortası yukarı/aşağı aynı mı). Kanal skoru = %60 içeride + %40 hareket; içeride < %80 → elenir (skor 0). Eski mum/kanal/AI skorları detayda bilgi olarak duruyor.
- Hepsi elenirse: "Eşleşme yok — tüm formasyonlar %20 kanal kuralıyla elendi" + en yakını.
- TAHMİN: Adım 5'te devam mumlarından hesaplanıp kaydedilir (hazir.tahmin): yön ▲/▼/◆, sonraki N mumda net hareket ve en çok yukarı/aşağı, formasyon boyuna göre %. Eşleşmede "🔮 Tahmin: ▼ düşüş • sonraki 8 mumda net %20 (en çok ▲%0 / ▼%58)". Devamı olmayan formasyonda "Tahmin yok".
- Test: BTC fotoğrafının %80'i (kırpık, 42 mum) tarandı; tam fotoğraftan kırpığın son mumunda kesilen 25 mumluk formasyon: 25/25 içeride, hareket %100, tahmin ▼ (gerçekte de sonrasında düşüş vardı). Hazır kütüphanedeki 10 formasyon bu grafikte elendi.
- Not: Hazır Kütüphane formasyonlarının devam kısmı yok (formasyonlar/kutuphane/tam/ içinde tam hâlleri var; ileride tahmin için kullanılabilir).

## Yapılacaklar — 1 Kasım 07:10 önerileri (Claude, kullanıcı listeye eklenmesini istedi)
- [ ] Kanal sınırını düzeltme: Adım 4'te site yanlış bölerse kullanıcı sınır mumunu seçip kanalı böler/birleştirir.
- [ ] Kütüphane yönetimi: kayıtlı formasyonu kanallı önizlemeyle görme, yeniden adlandırma, tek tek silme, Hazırla'da yeniden açıp düzenleme.
- [ ] (ÇOK SONRA) Test arşivi: her tarama DEĞİL, yalnızca benzerliği belli oranın üstünde olan ve yakın çıkan eşleşmeler arşivlenir; sonradan "gerçekleşti / gerçekleşmedi" işaretlenip başarı oranı ve eşikler (%80, %60/%40) ayarlanır.
- [ ] Hazır Kütüphane için tahmin: formasyonlar/kutuphane/tam/ içindeki tam hâllerden devam kısmını çıkarıp tahmin üret.
- [ ] Yapay zekâ (CLIP) modeli: ana skor artık kanal skoru; ~90 MB model ilk taramayı yavaşlatıyor. Kapat/aç seçeneği (kapalıyken Tara saniyeler içinde biter).
- [ ] Çizimli görsel uyarısı: Hazırla'da çok sayıda sahte mum silinirse "görselde çizim/yazı var gibi, orijinali kullan" uyarısı.
- [ ] Kütüphaneyi gözden geçirme ve deneme planı:
  1. Hazır Kütüphane (10) + QM (6) formasyonlarını Hazırla'dan geçir (kanallar + devam/tahmin).
  2. Kendi kendine test: her formasyonun kendi görseliyle tarama → kendisi %80+ ile geçmeli.
  3. Çapraz test: her formasyon diğerlerinin görseliyle → elenmeli; elenmeyen çiftler "benzer" (eski not: LO 05 ↔ LO 02 %91, LO 07 ↔ LO 01 %91) → birleştir ya da ayırt edici hâle getir.
  4. Gerçek Binance denemeleri (15 dk, farklı coinler, 1x/2x): sonuçları test günlüğüne yaz.
- 07:20 Kanal düzeltme Adım 4'e eklendi (kullanıcı: kaydetmeden önce kanal seçeneğinde sunulmalı): grafikte bir muma dokun → o mumdan yeni kanal başlar (BÖL; her kanal en az 2 mum); listede "⤴ öncekiyle birleştir"; "↺ Sitenin önerisine dön". Kanal türü (yükselen/inen/yatay) eğime göre yeniden hesaplanır; kayıt düzeltilmiş kanallarla yapılır. Test: böl 15→6+9, birleştir, kaydet çalışıyor.
- Kullanıcı görüşü: tüm grafikler Hazırla'dan yeniden yükleneceği için kütüphane yönetimindeki kanal düzenleme ihtiyacı büyük ölçüde ortadan kalkar; yeniden adlandırma / tek tek silme yeterli olabilir.

- ÖNCELİK (1 Kasım, kullanıcı): Smart Money (SMC) formasyon grafiklerini bulup Formasyon Hazırla ile kütüphaneye eklemek.

## 1 Kasım 07:30 — Yapay zekâ kapatıldı
- Tara'da CLIP modeli KAPALI (AI_ACIK=false). Skor zaten tamamen kanal skorundan geliyordu; model katkı vermeden ~90 MB indiriliyordu. Bilgisayar testi: Fotoğraf Oku + 10 formasyonluk tarama ~0,8 sn, model hiç çağrılmıyor. Gerekirse AI_ACIK=true.
- İleride (fikir): AI'ı Tara yerine kütüphanede kullanmak — kayıtta benzer formasyon uyarısı / gruplama.

## ▶ YARIN (2 Kasım) PLANI
1. Kütüphane sıfırdan: telefondaki eski referansları sil ("Tüm Referansları Sil"); tüm formasyonlar Formasyon Hazırla'dan eklenecek (numaralama → sahte mum → kesim önerisi/seçimi → kes → %20 kanallar + düzeltme → LO/SH adıyla kaydet).
   - Önce 6 QM görseli (QM_Ortak_6), sonra diğer SMC formasyonları (öncelik).
   - Hazır Kütüphane'deki 10 formasyon da istenirse Hazırla'dan geçirilir (kanal + devam/tahmin için tam hâlleri: formasyonlar/kutuphane/tam/).
2. Bol deneme:
   - Kendi kendine: her formasyon kendi görseliyle → kendisi geçmeli.
   - Çapraz: diğer formasyonların görselleriyle → elenmeli; elenmeyen benzer çiftleri not et.
   - Gerçek Binance (15 dk, farklı coinler, 1x/2x; Fotoğraf Oku ve canlı kamera).
3. Aksaklıkları tespit et: her sorunun ekran görüntüsü + hangi adımda olduğu.
4. En son: Yapılacaklar listesi ve NOTLAR bölümleri birlikte kontrol edilip güncellenecek (biten işler işaretlenecek, gereksizler çıkarılacak).

## 2 Kasım 02:45 — Hazırla: "📚 Hazır Kütüphaneden yükle"
- Kullanıcı sırası: 1) kütüphane çizimlerini bitir → 2) test → 3) sonuçlara göre karşılaştırma → 4) eksik/hataları not al → 5) devam planı.
- Hazırla'ya açılır liste eklendi: 10 hazır formasyonun TAM hâli (devamıyla, formasyonlar/kutuphane/tam/) yüklenir; kesim, kesik kütüphane görselinin mum sayısında ÖNERİLİR (kullanıcı değiştirebilir); ad ve LO/SH Adım 5'e otomatik yazılır. Kamera / mum okuma koduna dokunulmadı.
- Test (telefon boyutu, bilgisayar): 10/10 yüklendi, Adım 3 tekrar okuma hepsinde birebir.
  | Formasyon | Tam | Kesim | Devam |
  |---|---|---|---|
  | LO 01 Liquidity Sweep | 26 | 21 | 5 |
  | LO 02 OB Retest (eski) | 32 | 24 | 8 |
  | LO 03 BOS (eski) | 30 | 25 | 5 |
  | LO 04 Wyckoff Spring'li | 31 | 24 | 7 |
  | LO 05 Wyckoff Spring'siz | 30 | 24 | 6 |
  | LO 06 OB Retest | 26 | 20 | 6 |
  | LO 07 CHoCH | 25 | 20 | 5 |
  | LO 08 BOS Devam | 26 | 20 | 6 |
  | LO 09 Kahve Fincanı | 34 | 29 | 5 |
  | SH 01 Wyckoff Dağıtım | 31 | 24 | 7 |
- QM görselleri (6) özel arşivde; onlar "Görsel Seç" ile yüklenir.
- 02:45 Kullanıcı isteğiyle eski "📚 Hazır Kütüphaneyi Yükle" düğmesi GİZLENDİ (kesik görselleri Hazırla'dan geçirmeden ekliyordu). Kod duruyor; formasyonlar artık yalnızca Hazırla → Adım 5 Kaydet ile kütüphaneye girer.
- 02:50 Telif önlemi (kullanıcı onayı): kaynağı belgelenmemiş ilk 3 formasyon (F1 Liquidity Sweep, F2 OB Retest, F3 BOS = LO 01–03) depodan ve Hazırla listesinden KALDIRILDI (kutuphane, tam, temiz, numarali, kesilmis). Listede yalnızca bizim çizdiğimiz 7 formasyon kaldı (LO 04–09, SH 01). Not: git geçmişinde eski sürümler hâlâ duruyor.
- Kullanıcı şimdi telefonundaki 9 formasyonu (31 Ekim seçilen ortak set) Görsel Seç ile Hazırla'dan geçiriyor; sorun çıkarsa bildirecek.

## 2 Kasım 03:05 — Hazırla görüntüsü: orijinal oran + büyütme (kullanıcı isteği)
- Sorun (kullanıcı ekranı, QM 01 Nora GBPUSD): görüntü yatayda esnetiliyordu (mum başına 22 px), kutular mumların üstüne biniyordu, büyütme/küçültme yoktu → formasyon orijinal hâliyle görülemiyordu.
- Düzeltme (yalnızca gösterim; okuma/kamera koduna dokunulmadı):
  - Görsel ORİJİNAL ORANIYLA açılır (esnetme yok); yatayda görselin tamamı, dikeyde mumların olduğu bant.
  - 🔍－ / 🔍＋ / ⤢ Sığdır düğmeleri + iki parmakla büyütme (1x–12x); büyütmede parmakların altındaki nokta yerinde kalır.
  - 👁 Orijinal: mum kutuları ve kılavuz çizgileri gizlenir, yalnızca numara şeridi (ve seçili/silinen/başlangıç/kesim işaretleri) kalır. 🔢 İşaretler ile geri döner.
  - Sıkışıkken numaralar seyreltilir (her 2/5/10'da bir + ilk/son + işaretliler); büyütünce hepsi görünür.
- Test (iPhone boyutu): Nora QM görseli 103 mum, sığdır/büyüt/orijinal çalışıyor; 7 hazır formasyon Adım 3 birebir.

## 2 Kasım 03:20 — Mum okuma düzeltmesi: merdiven köprüsü (ortak okuma kodu)
- Kullanıcı bulgusu (QM 01 Nora, Hazırla): 18 ile 19 arasındaki uzun yeşil mum (HH'ye çıkış) okunmadı; temiz çizimde de yok.
- Sebep: merdiven gibi dizilen aynı renk iki uzun mum, aradaki 1 px boşluk bulanınca TEK satırla birleşiyor. splitWick o 1 satırı "gövde", iki uzun gövdeyi "fitil" sanıyor → yüksekliği 1 olan parça eleniyor → İKİ mum birden kayboluyordu. Görselin boyutuna göre ortaya çıkıyor (bende 1,33 kat ölçekte tekrarlandı).
- Düzeltme: splitBridge — bileşenin içinde neredeyse boş bir sütun varsa, iki yan dikeyde az örtüşüyorsa (merdiven) ve bileşen dar-uzunsa, o sütundan ayrılır. Yatay yazı / fiyat etiketi (ör. "GBPUSD 1.27580") bölünmez.
- detectCandles ortak: kamera, Fotoğraf Oku, Hazırla ve kütüphane okuması aynı düzeltmeyi alır.
- Test (eski ↔ yeni, mum kaybı = 0 her yerde): Nora görseli 14 farklı ölçek → yalnızca kaçan merdiven mumları eklendi (1,33x: 95→97, 0,8x: 97→99, 2,2x: 102→104); BINANCE_TEST foto 34=34, temiz 25=25; 7 hazır formasyon değişmedi, Adım 3 birebir.
- 03:30 Kullanıcı: "sonraki adıma geçmiyor". Durum: kesimin sağındaki ~60 mum Sahte Mum ile silinmişti, kesim seçilmemiş görünüyordu (Adım 3 düğmesi yok). Kesim modunda silinmiş (✕) bir muma dokunulunca site sessizce hiçbir şey yapmıyordu. Düzeltme: silinmiş muma dokunulursa en yakın silinmemiş mum seçilir; hzRender'da hata olursa ekranda kırmızı uyarı çıkar. Not: kesimin sağı DEVAM'dır (tahmin bundan hesaplanır), silinmemeli; sağ tarafı ayırmak için kesim yeterli.

## 2 Kasım 03:45 — Hazırla akışı sadeleşti (kullanıcı isteği)
- Kullanıcı: "kullanıcı için zor" — orijinal görselde sahte mum seçmek zor; sahte mum TEMİZ çizimde belli olur.
- Yeni sıra: 1) görsel yükle → 2) 🔴 Kesim (görsel açılınca varsayılan mod; tek dokunuş, sağ taraf otomatik ayrılır = devam, tahmin için saklanır) → 3) Kes ve Temiz Çiz → temiz çizimde sahte mumlara dokun (sarı) → "🗑️ Sil ve Yeniden Çiz" → "↩️ Silmeleri Geri Al" ile geri dönülebilir → 4) kanallar → 5) kaydet.
- Temiz çizimin altında numaralar var. Kesim/başlangıç mumu silinirse en yakın sağlam muma kayar.
- Mod düğmeleri sırası: 🔴 Kesim / 🟢 Başlangıç / ✂️ Sahte Mum (orijinal görselde silme isteğe bağlı olarak duruyor).
- Test: Nora görseli kesim 58, temizde 3 mum seç → 55 birebir, geri al → 58, Adım 4: 3 kanal.
- 03:50 Kullanıcı kararı: 🟢 Başlangıç düğmesi KALDIRILDI (formasyonlar zaten tam hâliyle yüklenecek; mum dizilişi yüklenince görünüyor). Formasyon = ilk mum → kesim. Kullanıcının işi: kesim → (varsa) temiz çizimde sahte mum düzeltme → kanal sapma kontrolü → kaydet.

## 2 Kasım 04:00 — QM_Ortak_6 kontrolü (görseller depoda YOK, yalnızca kullanıcı arşivi)
- Kullanıcının Hazırla'ya yüklediği Nora kopyası işaretli ("KESIM" yazılı) ve kırpıktı → 69 mum, temiz çizimde "fark var" (44→40), LL'ye inen mumlar kayıp. Arşivdeki orijinal Nora (01) ile aynı işlem: 103 mum, kesim 58 → 58/58 birebir.
- Her görsel sitenin okumasıyla okundu, tüm mumlar temiz çizildi, orijinalle göz kontrolü:
  | No | Görsel | Mum | Sonuç |
  |---|---|---|---|
  | 01 | Nora GBPUSD 1G | 103 | ✅ yapı birebir; sağ kenarda 1–2 sahte (fiyat etiketi) |
  | 02 | TFlab MT5 USDCHF 15dk | 88 | ✅ iyi; sağ eksende 1 sahte kırmızı çizgi |
  | 03 | TFlab BTCUSD 1s | 96 | ⚠️ kullanılabilir: zikzak çizimi mumların üstünde, sağ kenarda fiyat etiketlerinden sahte mumlar (devam kısmına düşüyor → tahmini bozabilir) |
  | 04 | TFlab BTCUSDT 5dk | 81 | ✅ iyi |
  | 05 | TFlab MT5 GBPUSD 5dk | 55 | ❌ UYGUN DEĞİL: orijinalde ~250 küçük mum, site 55 okuyor; Reverse QM yapısı kayboluyor (dün de "şüpheli" denmişti) |
  | 06 | TFlab WTI 1s | 80 | ✅ iyi |
- Karar önerisi: 01, 02, 04, 06 kütüphaneye; 03 dikkatle (sahteler silinir, devamdaki sahteler için ileride çözüm); 05 çıkarılır. Sıfırdan başlamaya gerek yok.
- Yeni eksik (not): Adım 3'te sahte mum yalnızca formasyonda silinebiliyor; kesimin sağındaki (devam) sahte mumlar silinemiyor → tahmine girer.

## 2 Kasım 04:05 — Hazırla okuması kamera kutusundan bağımsız
- Bulgu: aynı Nora orijinali kullanıcının telefonunda 69 mum, bilgisayarda 103 mum. Sebep: Hazırla (Fotoğraf Oku yolu) görseli sayfadaki kamera kutusunun o anki en/boy oranına göre yerleştiriyor; kutu farklı boyuttaysa (telefon düzeni, kamera kapalı/açık vb.) okuma değişiyor (test: kutu 358×150 → 59 mum, kırmızı mumlar kayboluyor). "KESIM" yazısı sitenin değil, eski işaretli kopyanındı — ama 69'un asıl sebebi buydu.
- Düzeltme: Hazırla sırasında kutu ölçüsü sabit 330×275 (CSS oranı 1,20) kabul ediliyor. Kutu 150–700 px her boyda: 103 mum, öneriler 46/68/32. Kamera ve Fotoğraf Oku okumasına dokunulmadı.
- AÇIK KONU (not): Fotoğraf Oku da aynı şekilde kutu boyutuna bağlı → aynı fotoğraf farklı cihaz düzenlerinde farklı okunabilir. Kamerayla tutarlılık için şimdilik bırakıldı; test aşamasında bakılacak.
- 04:15 Kullanıcı kararı: kamera için önemli olan SAĞ taraf (son mumlar) — kameraya dokunulmadı. Kütüphane için önemli olan SOL taraf (formasyon ilk mumdan başlar) → Hazırla artık kamera çerçevesini HİÇ kullanmıyor; görselin kendi oranı kullanılıyor (grafik okuma alanını tam doldurur, sola boşluk/kesik yok). Sonuç (6 QM): 01 103, 02 89, 03 95, 04 88, 05 51, 06 84 mum; çerçeve boyutu ne olursa olsun aynı. 04'te ortadaki uzun kırmızı mum (18:30) temiz çizimde eksik görünüyor — testte bakılacak.

## 2 Kasım 04:40 — Kütüphane için grafik sınırı (hzFindChartBox)
- Teşhis satırı (sürüm • görsel • grafik • dpr) eklendi. Telefonda: sürüm doğru, görsel 625×585, ama grafik "5,0 615×585" (görselin TAMAMI) → başlık ve eksen de okunuyor, 86 mum, sahteler. Bilgisayarda "5,186 616×361".
- Bulgular: (a) eski findChartBox satırda ≥2 renkli piksel arıyor ve görseli 600 px'e küçültüyordu → Nora HH'nin 1 px fitil ucu (y 159–185) KESİLİYORDU; (b) telefondaki görselde Fotoğraflar işaretlemesi ("hareket", "KESIM" yazıları) var → boş alanı köprüleyip başlıkla grafiği birleştiriyor olabilir (bilgisayarda renk doygunluğu artırılarak tekrarlanamadı).
- Yeni hzFindChartBox (yalnızca Hazırla): küçültme yok (1200 px'e kadar), çekirdek bant = satırda ≥ max(3, %1 genişlik) renkli piksel, en büyük kütleli bant; üst/alt yalnızca çekirdeğe BAĞLI piksellerle (fitiller, 2 satır kopukluk toleransı) uzatılır. Nora: grafik 5,159 617×388 (HH ucu dahil), 106 mum.
- Kullanıcıya: telefondaki görsel işaretli kopya; Fotoğraflar → Düzenle → Geri Al (Orijinale Dön) ya da zip'ten çıkan dosya.

## 2 Kasım 05:05 — Oturum sonu: asıl engel bulundu
- Telefonda Hazırla'ya yüklenen görseller "Kırılım" klasöründen geliyordu: dün kesim yeri işaretlenmiş kopyalar (sarı alan, yeşil "hareket", kırmızı "KESIM" yazıları). Bütün 69/86 mum, "fark var", başlık/eksen sahteleri bu yüzden. Ayrıca "Kırılım" ve "QM_Ortak_6" klasörleri telefonda Son Silinenler'de görünüyor (kullanıcı silmedi; Kurtar gerekebilir).
- Temiz orijinaller (01, 02, 03, 04, 06) kullanıcıya sohbetten yeniden gönderildi → "QM_Temiz" klasörüne kaydedip Dosyayı Seç ile yüklenecek.

## ▶ SONRAKİ OTURUM (2 Kasım devamı) PLANI
1. QM_Temiz'den 02 USDCHF ile başla: teşhis satırı "grafik 1,32 619×277", 88 mum beklenir → kesim → Adım 3 "✓ birebir" → sahte sil → Adım 4 kanallar → Kaydet (SH).
2. Sonra 01 Nora (beklenen ~106 mum, kesim Entry'den sonraki düşüşün 2. mumu), 04, 06, 03 (sahteleri dikkatle). 05 çıkarıldı.
3. Hazır kütüphaneden 7 formasyon (LO 04–09, SH 01) açılır listeden.
4. Test: kendi kendine (her formasyon kendi görseliyle geçmeli), çapraz (elenmeli), gerçek Binance (15 dk, 1x/2x).
5. Açık konular: Fotoğraf Oku hâlâ kamera çerçevesine bağlı (kullanıcı onayıyla düzeltilecek); devam kısmındaki sahte mumlar silinemiyor (tahmine karışır); üst sıradaki "✂️ Sahte Mum" düğmesi kalsın mı kararı; 04'te ortadaki uzun kırmızı mum temiz çizimde eksik görünüyor.

## 2 Kasım 06:10 — Kullanıcı ilk formasyonu kaydetti + 3 düzeltme
- Kullanıcı temiz 02 USDCHF ile Hazırla'yı baştan sona geçirdi: 53 mum, 4 kanal, devam 54 → kaydedildi (ad "QM 11-02 02:54", yön LO seçilmiş — 02 aslında SH, düzeltilecek).
- Sorun 1 "Sil ve Yeniden Çiz çalışmıyor": iPhone'da temiz çizime dokunuş için click yerine pointerup; seçilenler yönerge satırında yazıyor ("🟨 Seçili: 11, 21"); düğme seçim yokken soluk.
- Sorun 2 (bulunan): temiz çizim tekrar okununca bazı mumlar kayıp ("fark var", 02'de 53→49). Sebep gövde genişliği (aralığın %72'si). %50'ye indirildi: 02 53/53, Nora 58/58, 6 QM 30/45/60 mumluk dilimlerin çoğu birebir (02 45→41, 05 60→58 kaldı), 7 hazır formasyon birebir.
- Sorun 3 "kütüphanede kanallar görünmüyor": kanallar veri olarak kaydediliyordu; artık kütüphane kartında da kesikli çizgi olarak çiziliyor (yalnızca gösterim; kayıtlı görsel ve Tara değişmedi).
- 06:20 Kullanıcı: "seçtiğim alan, kesilen alan, kanal alanı birbirinden çok farklı; her seferinde fotoğraf değişiyor". Sebep: her adım farklı ölçekte (Adım 2 görselin tamamı, Adım 3 yalnızca formasyonu çerçeveye yayar, Adım 4 formasyon+devamı birlikte sığdırır). Düzeltme: Adım 3'te üstte ORİJİNAL fotoğrafın kesilen kısmı, temiz çizimle AYNI ölçek/hizada (ilk-son mum ortası ve formasyonun en üst/en alt noktası eşlenir), aralarında ince kılavuz çizgiler; seçilen sahte mum her iki görüntüde sarı. Test: 02 kesim 38 → 38/38, Nora 58/58; görsel karşılaştırmada QM tepesi, düşüş ve dönüş birebir.
- Not: Adım 4'te devam kısmında sahte mum (fiyat etiketi "---") görünüyor → devam sahtelerini silme hâlâ eksik.

## 2 Kasım 07:05 — KURAL: orijinal fotoğrafa kesimden başka dokunulmaz (kullanıcı)
- Kullanıcı: "Orijinal üstünde kesimden başka hiçbir oynama olmasın; numaralamadan sonra orijinal foto değişmesin; sadece kesilen alan atılıp büyütme/küçültme/daraltma olmadan kanallar yerleştirilsin." (Tarama/karşılaştırmaya henüz geçilmedi.)
- Uygulama (sürüm 2Kas-07:00):
  - Adım 3: orijinal fotoğraf, yalnızca kesimin sağı atılmış hâlde (ölçek değişmez); numaralar altta; sahte mum seçimi bu görüntüde (sarı sütun). Temiz çizim artık GÖSTERİLMİYOR, yalnızca arka planda (Tara verisi + "birebir" kontrolü).
  - Adım 4: kanallar orijinal fotoğrafın ÜSTÜNE, orijinal koordinatlarda çiziliyor (hzEnv aynı yöntem, mumlar orijinal koordinata çevrilerek). Kanal bölme dokunuşu da orijinal üzerinde.
  - Kaydet: hazir.orijinal (kırpık orijinal, ≤900 px JPEG) + hazir.kanallarOrj. Kütüphane kartı orijinal + kanalları gösteriyor. Tara için src (temiz çizim) ve hazir.kanallar değişmedi.
- Bu görünüm okuma eksiklerini ortaya çıkardı → ORTAK OKUMA düzeltmesi: removeAlignedNoise grafiğin her yerindeki aynı hizadaki küçük düz mumları "yazı" sanıp siliyordu (QM 02 yatay bölgede ~1/3 kayıp). Artık yalnızca YAN YANA dizili (≤ max(10, 4×genişlik) aralıklı) ≥4 parça yazı/kesikli çizgi sayılıyor; üst %10 şeritte (başlık) eski kural. Sonuç: 02 88→100, 04 80→92, 06 79→89 (06'da yeşil zikzak çizgisi parçaları sahte olarak gelebilir — Adım 3'te silinir); Nora, 03, Binance test, 7 hazır formasyon DEĞİŞMEDİ.
- Kalan: 02'de mavi zikzak çizgisinin geçtiği yerde 2–3 küçük mum hâlâ kaçıyor; devam kısmındaki sahteler silinemiyor; Fotoğraf Oku çerçeveye bağlı.

## 3 Kasım 02:15 — Formasyonu büyük açma (kanallarla) — sürüm 3Kas-02:15
- Kullanıcı: kütüphaneye eklenen formasyon kanal çizgileriyle büyük görülebilmeli; eşleşme sonrası kullanıcı eşleşen görüntüyü elle büyütüp gerçek ekranla gözle karşılaştırmalı.
- Eklendi: tam ekran görüntüleyici (openZoom). Kütüphane kartına dokununca, En Yakın Eşleşmeler'deki küçük resme dokununca ve "🔍 Formasyonu Büyük Aç (kanallarla)" düğmesiyle açılır. İki parmakla büyütme, kaydırma, çift dokunma 2x/sığdır, Sığdır ve ✕. Telefon yan çevrilince yeniden sığdırır.
- Kart çizimi refPreview(ref) fonksiyonuna taşındı (aynı çizim kartta, eşleşme listesinde ve büyük görünümde). Eşleşme listesindeki küçük resim artık kanallı orijinal. Kayıtlı görsel ve Tara DEĞİŞMEDİ.
- 02 USDCHF testi (sürüm 2Kas-07:00 kuralları) hâlâ bekliyor.

## 3 Kasım 02:20 — "Tüm Referansları Sil" güvenliği — sürüm 3Kas-02:20
- Kullanıcı: düğme daha küçük olsun, silmeden önce iki ayrı onay: 1) sağda "Emin misin?" 2) solda "Onaylıyor musun?".
- Uygulama: küçük gri düğme (ortada). Basınca "⚠️ N formasyonun tamamı silinecek" + SAĞDA "1) Emin misin?" + Vazgeç. Ona basınca sağdaki kaybolur, SOLDA "2) Onaylıyor musun?" çıkar; ancak buna basınca silinir. 8 sn işlem yapılmazsa onay kapanır. Tek formasyonun "Sil" düğmesi değişmedi.

## 3 Kasım 02:35 — KURAL DEĞİŞTİ: orijinal, dizilim bozulmadan TEMİZLENİR — sürüm 3Kas-02:35
- Kullanıcı (büyük görünümde ok/yuvarlak/zikzak duruyordu): "Orijinal mum dizimi ve sırası bozulmadan temizlenip kanallar eklensin."
- Yeni kural (2 Kasım kuralının yerine): orijinalle AYNI boyutta beyaz zemin; her mum orijinaldeki yerinde, aynı genişlik/yükseklikte, orijinalden örneklenen rengiyle yeniden çizilir (hzTemizOrj). Ok, yuvarlak, çizgi, yazı, eksen, araç çubuğu düşer. Ölçek/kayma/sıra değişmez; Adım 3'te sahte diye silinen mumlar girmez.
- Nerede: Adım 4 (kanallar temiz orijinal üstünde), kütüphane kartı, eşleşme listesi, büyük görünüm. Adım 3 sahte mum seçimi için ORİJİNALİ göstermeye devam ediyor.
- Kayıt: hazir.temizOrj (PNG) eklendi; hazir.orijinal da saklanıyor. Büyük görünümde "👁 Orijinal ⇄ 🧹 Temiz" düğmesi (yakınlaştırma korunur).
- Eski kayıtlarda temizOrj yok → orijinal gösterilir; temiz hâl için formasyonu Hazırla'dan yeniden geçirmek gerekir.
- Tara/eşleştirme DEĞİŞMEDİ (yine arka plandaki temiz çizimi okur).

## 3 Kasım 02:45 — Tek formasyon silme de iki onaylı — sürüm 3Kas-02:45
- Kullanıcı: tek silinen formasyonlarda da 2 kez onay.
- Kartta "Sil" → SAĞDA "1) Emin misin?" + Vazgeç → SOLDA "2) Onaylıyor musun?" → silinir. 8 sn dokunulmazsa kapanır. (confirm() kaldırıldı.)
- Kullanıcı eski "QM 11-02 23:02" kaydını sildi; temiz hâlle yeniden hazırlanacak.

## 3 Kasım 02:20 — Saat düzeltmesi — sürüm 3Kas-s4
- Kayıt adındaki saat UTC'ydi (3 saat geri: "QM 11-02 23:02" aslında 3 Kasım 02:02). Artık telefonun yerel saati kullanılıyor.
- Sürüm etiketleri saat değil, sıra numarası (3Kas-s4 = 3 Kasım'ın 4. sürümü). Önceki 02:35/02:45 etiketleri yanlışlıkla ileri saat yazılmıştı.

## 3 Kasım 02:25 — İlk temiz-orijinal testi (02 USDCHF) — sürüm 3Kas-s5
- Kullanıcı testi: 47 mum, Adım 4'te 3 kanal, taşma 0; araç çubuğu, QM yuvarlağı, oklar, zikzak temizlendi; mumlar yerinde.
- Düzeltildi: temiz çizimde fitiller telefonda görünmeyecek kadar inceydi (≥ W/300, ≤ aralığın %16'sı); Adım 3 numaraları üst üste biniyordu (adım 2'de hepsi aynı sıraya düşüyordu) → sıra numarası dönüşümlü, aralık en geniş numaraya göre.
- Açık: temiz görüntüde grafiğin altındaki geniş boş beyaz alan (orijinal yükseklik korunduğu için). Kırpılsın mı → kullanıcıya soruldu.

## 3 Kasım 02:27 — Adım 4 dik çizgiler kaldırıldı — sürüm 3Kas-s6
- Kullanıcı: kanal başlangıcını gösteren dik çizgiler gereksiz; diğer formasyonlarda olmayan bir fark "site hata mı" diye güven sorunu yaratır. Kaldırıldı; kanal başlangıcı yalnızca alttaki renkli numarayla gösteriliyor.
- İlke (kullanıcı): ekranda gereksiz/tutarsız görsel öğe olmasın; formasyonlar arasında görünüm aynı olsun.
- 02:28 Karar (kullanıcı): alttaki boş beyaz alan KIRPILMAYACAK. Hâlâ çizim aşamasındayız; diğer formasyonlarda olmayan değişiklik burada da olmasın; ayrıca 02'de aşağı yönlü devam var (boş alan devamın gideceği yer).

## 3 Kasım 02:35 — Adım 3 artık TEMİZ çizimi gösterir — sürüm 3Kas-s7
- Kullanıcı: "Kes ve Temiz Çiz"den sonra sadece kesti; yuvarlak ve oklar duruyordu. (Düğme adı ile ekran çelişiyordu.)
- Adım 3 görüntüsü temiz orijinal (hzTemizOrj, aynı boyut/yer); "👁 Orijinal ⇄ 🧹 Temiz" düğmesiyle orijinale bakılarak sahte mum kontrol edilir. Seçim/numaralar her iki görünümde aynı.
