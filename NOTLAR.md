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

## 3 Kasım (s8) — Numaralar yeniden sırayla
- Sorun: Kesim ekranında ve Adım 3 temiz çizimde numaralar seyreliyordu (25,30,35… / 2,4,6…), aradakiler ancak büyütünce çıkıyordu.
- Kesim ekranı artık ilk açılışta her mum numarası okunacak kadar büyük açılıyor (en sağdan). "Sığdır" tüm görseli gösterir, o zaman numaralar yine seyrelir.
- Adım 3 ekran çözünürlüğünde çiziliyor; mum aralığı ≥ ~15 px, gerekirse yana kaydırılıyor (soldan başlar). Numaralar 1,2,3… iki sıra dönüşümlü. Mum yeri/sırası değişmez, yalnızca orantılı büyütme.
- s9 (kullanıcı düzeltmesi): kesim sayfası ve Adım 3 yine ORİJİNAL fotoğraf hâliyle, tamamı ekran genişliğinde açılır (otomatik büyütme geri alındı). Numaralar sıkışıkta seyrelir; ＋ / iki parmakla büyütünce sırayla görünür.
- s10: 👁 Orijinal düğmesi büyütmeyi sıfırlar, fotoğrafın tamamını orijinal hâliyle gösterir.
- s11 (kullanıcı onayı): numaralar alt şeritte 2–5 sıra üst üste; orijinal (tam) görünümde bile hepsi sırayla. Yazı 11 px, gerekirse 8 px'e kadar küçülür. Kesim sayfası ve Adım 3 aynı.
- s12: Adım 3 her yeni görsel/kesimde TEMİZ çizimle açılır; önceki '👁 Orijinal' seçimi taşınmıyordu (temizlik bozuldu sanılıyordu).
- s13 (okuma, kamera dahil ortak): BOŞLUK DOLDURMA (fillGaps). Küçük gövdeli mumlar (≈3×2 px, soluk fitil) 8 px alan sınırına takılıp atılıyordu → temiz çizimde boşluk. Mum aralığı düzenli olduğu için iki mum arasındaki beklenen boşlukta duran küçük dolu gövde (≥4 px, komşuların fiyat bandında) mum sayılır; sol uçta da bir mum aranır, sağ uçta aranmaz (fiyat ekseni etiketleri). Test: USDCHF QM 100→115 mum (kayıp 11'in hepsi + sağ taraftaki 4 küçük mum); kütüphanedeki 14 görsel ve 2 Binance test görselinde sayı değişmedi.
- s14: Telefonda aynı USDCHF görseli 107 mum okudu (bilgisayar tarayıcısında 115) — iPhone görüntüyü küçültürken küçük mumları daha soluk/ince bırakıyor. Boşluk doldurma genişletildi: beklenen boşlukta 3 px'lik ince doji (3×1), fitiliyle birleşmiş gövde ve komşusuna yapışmış mumun kendi sütunları da mum sayılıyor. Kaba küçültmede (iPhone benzetimi) 111→117. Kütüphane ve Binance test görsellerinde sayı değişmedi.
- s15 (kullanıcı: "temizlik mumları küçültüyor, boyunu kısaltıyor"): Adım 3 temizliği artık mumu YENİDEN ÇİZMİYOR. Her mumun pikselleri orijinalden AYNEN kopyalanıyor (gövde sütun genişliğinde, fitil orta sütunda, gövdeye bağlı olduğu kadar; 2 px boşluk serbest). Ok/yuvarlak/yazı/zikzak atılıyor; uzun yatay çizginin sütundan geçen ince kısmı alınmıyor; mumun üstünden çizgi geçen 1–4 px'lik kesikler mumun kendi rengiyle dolduruluyor. Mum sayısı ve boyutu okumayla aynı kalır.
- s16 (kullanıcı: "dalgalanma çok, sadece 2 kanal çizdi → başarısız"): Kanal bulma (findChannels) artık DALGALARI izliyor. Zikzak dönüş noktaları (formasyon yüksekliğinin %20'si kadar geri dönüş) bulunur; kanal sınırı bir dönüş noktasındaysa ucuz (en az 3 mum), başka yerde eski ölçüt (düz taban/konsolidasyon için). USDCHF QM (55 mum): 2 kanal → 6 kanal (Yatay 1–18, Yükselen 19–29, İnen 30–36, Yükselen 37–43, İnen 44–50, Yükselen 51–55), taşma 0. Kütüphane: LO_07, LO_08, LO_09, SH_01, LO_04 aynı yapı; LO_06'da retest dalgası ayrı kanal oldu (İnen→Yükselen→İnen→Yükselen); LO_05'te ilk iniş ikiye bölündü. Aynı yöntem Tara karşılaştırmasında da kullanılıyor.
- s17 (kullanıcı: "son alan karışık; mesafeli olsun, iniş/çıkış eğilmeden, son mumlara bitişik olmadan"): (1) Aynı yöne giden ardışık kanallar (İnen+İnen, Yükselen+Yükselen) tek düz kanalda birleşir — hem kanal bulmada hem Adım 4 önerisinde; kırık/eğik çizgi yok. (2) Kanal çizgileri gövdeden değil en tepedeki/en dipteki mumun FİTİL ucundan + %20 pay. (3) Kanal genişliği en az formasyon yüksekliğinin %15'i. Kütüphane: Kahve Fincanı'nda iki yükselen kanal tek kanal oldu; LO_05 yeniden 3 kanal.

## ⭐ ASIL HEDEF (3 Kasım, kullanıcı) — karşılaştırmanın amacı
- Hedef bölgesi SON MUMUN (kesim mumunun) yönüne ve ZAMAN AKIŞINA bağlıdır; kesimden başlayan akış takip edilir.
- Son mum hangi yöne gidiyorsa (ör. kırmızı → aşağı) kanal o yönde %20 uzar; bu uzantı = beklenen hedef bölgesi.
- Karşılaştırmada (Tara) beklenen hedef bu yöndedir. Kodlama ayrıntıları kullanıcıyla netleştirilecek (uzunluk ve eğim).
- s18 ⭐ HEDEF KANALI (Adım 4): kesim mumundan başlar, yönü SON 3 MUM belirler (kesim "hareket başı + 2 mum" olduğu için; kullanıcı: "son mumlar gidilecek yönü tayin edecek şekilde kesiyorum"). Boyu formasyonun %20'si kadar mum (55 mum → 11). Eğimi formasyonda bu yöne giden en son kanalın eğimi (yoksa son 3 mumun eğimi, kanalların ortalama dikliğinin 1,5 katıyla sınırlı). Genişliği son kanal kadar. Yeşil (yukarı) / kırmızı (aşağı) taralı alan + "🎯 Hedef". Kaydedilen formasyona hazir.hedef olarak giriyor. Sıradaki iş: Tara karşılaştırmasında bu hedefi kullanmak.
- s19 (kullanıcı: "son seçilen mumlara göre yön tayini; kanallar son mum yönüne göre %20 uzasın; karşılaştırmada bu yöne göre seçim"): DENEME A. Tara karşılaştırmasında hedefi kaydedilmiş formasyonlar için grafiğin (kamera/fotoğraf) SON 3 MUMUNUN yönü, formasyonun hedef yönüyle aynı olmalı; ters ise formasyon ELENİR ("❌ Yön ters"). Uyuyorsa sonuçta "🎯 Hedef: ▲/▼ • sonraki N mum" yazar. Yön ölçütü kesimdeki ve kameradaki son 3 mum için aynı fonksiyon (sonYon). Kütüphane kartı/büyük görünümde hedef alanı da çizilir. Hedef yalnızca s18+ ile kaydedilen formasyonlarda var (eskiler yeniden kaydedilmeli). Site kesim önerisi değişmedi (hareket başı + 2), kullanıcı kararsız kalırsa alternatif.
- SONRAKİ DENEME B: sitenin kesim önerisine göre aynı test.
- s20: Adım 3 tuvali kutu genişliğine tam oturuyor. Kutu gizliyken genişlik ölçülemiyor (330 varsayılıyordu); telefonda kutu daha dar olduğu için sağdaki son mumlar (49–55) ekran dışında kalıyor, kesim bozulmuş gibi görünüyordu. Kesimin kendisi doğruydu.
- s21 (kullanıcı: "hedef çok uzun, formasyonla alakasız; kesimdeki son mumun uzunluğu kadar"): hedef alanı boyunca toplam iniş/çıkış = kesim mumunun boyu (fitil ucundan fitil ucuna). Yön yine son 3 mum, boy yine formasyonun %20'si kadar mum.
- s22 (kullanıcı: "son 2 mum belirlesin"): hedef alanının kalınlığı = son 2 mumun kapladığı yükseklik (en üst fitil ucu → en alt fitil ucu); son kanalın genişliği artık kullanılmıyor. Hedef: yön son 3 mum, eğim kesim mumu boyu, kalınlık son 2 mum, uzunluk formasyonun %20'si.
- s23 (kullanıcı): Formasyon Hazırla'da görsel seçilince ÖNCE yön sorulur (LO ▲ long / SH ▼ short; hazır kütüphanede dosya adından). Seçilen yön üstte görünür ve Adım 5'teki yön kutusuna yazılır. Kesimden sonra (Adım 3 ve 4) son 3 mumun yönü seçimle karşılaştırılır: uyuyorsa '✅ Yön uyumlu', çelişiyorsa '⚠️ Çelişki … kesimi kontrol et ya da yönü değiştir' uyarısı; yön kutusu değişince uyarı yenilenir. Engellemez, devam edilebilir.
- s24: Uyarı testi başarılı (LO seçip 55'te kesince '⚠️ Çelişki' çıktı). Adım 4'te art arda iki İnen kanal görüldü: birleştirme okuma koordinatlarına göre yapılıyordu, ekrandaki (orijinal koordinatlı) kanallar farklı yön verebiliyordu. Artık ikisine göre de birleştiriliyor.
- Kullanıcı (3 Kasım): taban/fiyat aralığı ayrıntısı şimdilik gereksiz; öncelik BİTMİŞ formasyonların eşleştirilmesi. Taban kanalı ayırma önerisi rafa kaldırıldı.

## Yol haritası (3 Kasım, kullanıcı)
1. Diğer formasyonları kütüphaneye ekle (yön sorusu → kesim → kanallar + hedef → kaydet); hata çıkarsa düzelt.
2. Hepsi hatasız yüklenince: Binance'ten çekilen orijinal resmi kütüphaneye ekle, sitenin onu bulup karşılaştırmasını dene.
3. Bu eşleşme oranı = ilk analiz yeteneği sonucu.

## Kontrol edilecek (3 Kasım) — temizlik: koyu kırmızı zikzak çizgisi
- BTC/USD 1h QM (TradingFinder, Head and Shoulders) görselinde orijinaldeki KOYU KIRMIZI zikzak çizgisi mum rengine benzediği için temizlikte tamamen silinmedi; ilk tepenin yanında ve dipte ince kahverengi çizgi parçaları kaldı. Çizim benzerliği ~%85.
- Olası çözüm: koyu/kahverengi kırmızı (düşük parlaklık) pikselleri mum kırmızısından ayırmak; mum sütununun dışındaki çapraz ince çizgileri almamak.
- Not 2 (aynı sorun): BTC/USDT 5m QM (TFlab/TradingFinder, Binance) — tepenin solunda koyu kırmızı zikzak parçası kaldı; yoğun 5 dk grafikte birkaç minik mum silik. Çizim benzerliği ~%88.
- Not 3 (aynı sorun, YEŞİL): WTI 1h QM (TFlab, LO) — yeşil zikzak parçaları ilk düşüşün üstünde ve 21 Şubat tepkisinin yanında kaldı. ~%85.
- ETKİ: kalıntılar yalnızca kütüphane GÖRÜNTÜSÜNDE (piksel kopya). Karşılaştırma mum verisinden yeniden çizilen temiz görüntüyle yapılır → kalıntı girmez. Tek risk: zikzak mumun üstünden/altından geçerse fitil uzun ölçülür → kanal (fitil ucuna göre) biraz genişler, %20 kuralı az gevşer.
- ÇÖZÜM (tüm formasyonlar yüklendikten sonra tek seferde): mum renginde (kırmızı VE yeşil) çizilmiş çapraz ince çizgileri hem okumada hem temizlikte ayıkla. Düzeltmeden sonra formasyonlar yeniden kaydedilmeli.
- 5 formasyon yüklendi. Çizim benzerlik oranları: GBPUSD QMR (LO) ~%90, USDCHF QM (SH) ~%92, BTC/USD 1h QM (SH) ~%85, BTC/USDT 5m QM (SH) ~%88, WTI 1h QM (LO) ~%85 → ortalama ~%88.
- s25 ZİKZAK AYIKLAMA (yalnızca temizlik; okuma/kamera DEĞİŞMEDİ). Yedek: dal `yedek-s24-dal` (geri dönüş için).
  Kural: mum pikseli, mumun kendi renginin zemine doğru tonları üstünde olmalı (renk uzaklığı < 48); zikzak/gösterge çizgileri (koyu kırmızı, saf yeşil) farklı tonda → alınmaz. Gövde satırlarında yalnızca gövde genişliği (+1 px). Fitil dik olmalı (aynı sütunda üst/alt komşu). İnce gövdeli mumlar için görselin genel mum rengi de kabul.
  Kontrol 1 (görsel, 5 formasyon): BTC 1s/5dk koyu kırmızı ve WTI yeşil zikzak parçaları büyük ölçüde gitti; gövdeler bozulmadı (ilk denemede küçük gövde ve doji kayboluyordu, düzeltildi; eşik 32/24 gövdeleri boşaltıyordu, 48 seçildi).
  Kontrol 2 (tam akış, 5 formasyon + 7 kütüphane + 2 Binance testi): mum sayısı, kanallar, hedef yönü 14/14 AYNI; kütüphane ve Binance temiz görselinde piksel farkı %0, Binance fotoğrafında %-2 (görsel olarak aynı); zikzaklı görsellerde %-0,1…-4,6 (silinen = zikzak).

## ▶️ KALDIĞIMIZ YER (3 Kasım 05:00) — buradan devam
- Site sürümü: 3Kas-s25. Geri dönüş yedeği: dal `yedek-s24-dal` (zikzak düzeltmesinden önceki hâl).
- Kütüphanede 5 formasyon var (GBPUSD QMR LO, USDCHF QM SH, BTC/USD 1s QM SH, BTC/USDT 5dk QM SH, WTI 1s QM LO); çizim benzerliği ort. ~%88.
- SIRADAKİ ADIMLAR:
  1. s25 temizliğini telefonda kontrol et (BTC ve WTI'de zikzak parçaları gitti mi).
  2. Beğenilirse 5 formasyonu yeniden kaydet (kartlardaki temiz görüntü kayıt anından geliyor).
  3. Binance'ten çekilen orijinal resmi kütüphaneye ekle → sitenin bulup karşılaştırmasını dene → eşleşme oranı = ilk analiz sonucu.
- Bekleyen / sonraya: kesim önerisi kullanıcının kesiminden 1–2 mum erken (öneri olduğu gibi kalacak); hedef alanının yüksekliği gerçekleşen hareketten kısa (ileride devam mumlarıyla ölçülecek); dip/taban kanalı = profesyonel aşama.
- s26: sürüm sayfanın en üstünde (başlığın altında, sarı) ve Formasyon Hazırla başlığında görünüyor — telefonda eski sürüm açılıp açılmadığı kolay kontrol edilsin. Kod değişikliği yok.

## s26 yeniden yükleme — bulunan hatalar (3 Kasım 06:43)
1. MUM BİRLEŞMESİ (asıl sorun, BTC/USDT 5dk): görselde ~153 mum var, site 97 okudu. Okuma görseli 502 px genişliğe küçültüyor; 153 mum için mum aralığı ~3 px → yan yana mumlar tek kutu oluyor (kesim ekranında 84, 87–90 kutuları 2 mumu kapsıyor). Diğer görseller (~100 mum) sorunsuz. Okuma kodu kamera ile ortak → çözüm kullanıcı kararı bekliyor (seçenekler: kütüphanede ~100 mumdan sık görselleri kırpmak / okuma çözünürlüğünü artırmak).
2. Kutular gövdeden büyük (WTI kesim ekranı): bazı kutular fitili de kapsıyor, bir doji (+) kutusuz. Aynı düşük çözünürlük etkisi; kanallar fitil ucuna göre çizildiği için eşleştirmeye etkisi küçük.
3. BTC 5dk temiz çizimde tepenin solunda koyu kırmızı zikzak parçası hâlâ var (s25 açık tonlu kenar piksellerini tam ayıklamıyor; mum birleşmesiyle de ilişkili olabilir).
4. Adım 4 numara şeridinde kanal sınırı numaraları normal numaraların üstüne biniyor ("1920", "4041", "2323"). Yalnızca görüntü.
- s27 NET TEMİZLİK (yalnızca temizlik; okuma/kamera/kanallar DEĞİŞMEDİ). Yedek: dal `yedek-s26-dal`.
  Mumun yeri ve boyu orijinal piksellerden (gövde, gövde genişliğinin %60'ı dolu satırlar boyunca; çizgi kesikleri atlanır), rengi grafiğin tam mum rengiyle DÜZ boyanır: gövde dolu dikdörtgen, fitil tek renk çizgi. Renkli kutu altındaki soluk mumlar net çıkar. Rengi grafiğin mum renginden çok farklı "mum" (zikzak/gösterge çizgisi) çizilmez. Okumada birleşmiş yan yana gövdeler boş sütundan ayrı çizilir.
  Kontrol 1 (görsel): GBPUSD pembe kutu altı mumlar net; BTC 1s/WTI zikzak parçaları gitti; USDCHF, Binance fotoğrafı, LO_09, SH_01 orijinalle aynı ve net.
  Kontrol 2 (tam akış, 14 görsel): mum sayısı, kanallar, hedef 14/14 AYNI.
  Kalan (okuma kaynaklı, temizlik değil): BTC 1s'te zikzak üstünde sahte bir kırmızı "mum" okunuyor (temizlikte çizilmiyor ama veride var; yanındaki küçük yeşil mum yerine geçmiş); BTC 5dk birleşme → kırpma kararı.
- s28 (kullanıcı: "kanallar tepe/dipte kesişiyor ve uzuyor; görselde kesişme olmasın; %20 pay yeter, uzama payı genişletiyor"). Yedek: dal `yedek-s27-dal`.
  Kanal çizgileri yalnızca kendi mumları üzerinde (±0,45 mum; eskiden ±0,6 → komşu kanalla kesişiyordu). Hedef alanı son kanal çizgisinin bittiği yerden başlar. "En az %15 genişlik" kuralı kaldırıldı: kanal = en uç fitiller + %20 pay (hem görüntü hem karşılaştırma).
  Kontrol: 4 formasyonda kanal bölümleri aynı; yalnızca BTC 1s 44–48 kanalı daraldı (49→35, %15 kuralı yalnız orada devredeydi). Kendi grafiğiyle eşleşme 55/55, 55/55, 61/61, 63/63; aynı grafiğin başka bölümleri 0 geçiş (eleme seçici).

## ▶️ YARIN (4 Kasım) — buradan başla
1. Sayfayı ?v=28 ile aç, başlık altında "sürüm 3Kas-s28" olduğunu doğrula.
2. Kütüphaneyi sil, 5 formasyonu yeniden yükle (BTC 5dk'yı 10:00–16:00 arası kırp). Her biri için çizim benzerlik skorunu değerlendir (önceki ort. ~%88).
3. Hata çıkarsa düzelt (her değişiklikten önce yedek dalı, 2 kez kontrol).
4. Binance denemesi: Binance'ten çekilen resimle karşılaştırma → eşleşme oranı = ilk analiz sonucu.
- Bekleyen (en sona): siteye giriş koruması. Kullanıcı PIN değiştirmede Gmail onayı istiyor. Seçenekler: (1) PIN + Firebase e-posta onayı, (2) Cloudflare Access — her girişte Gmail'e kod, PIN gereksiz, gerçek koruma (önerilen). Kütüphane + Binance testi bittikten sonra karar verilecek. Eski not: Seçenekler: basit PIN ekranı (kolay, ama depo herkese açıksa kod okunabilir; kütüphane zaten yalnızca telefonda) / gerçek koruma için Cloudflare Access vb. Kullanıcının kararı bekleniyor.
- Açık küçük hata: Adım 4 numara şeridinde sınır numaraları üst üste biniyor.

- s29 (kanalları iniş+yatay diye bölme + çizgi kırpma) denendi; kullanıcı beğenmedi: "s28 daha sade ve görsel, karşılaştırma için avantajlı; s29 karmaşık". Bölme GERİ ALINDI.
- s30 (kullanıcı: "s28'e dön, yalnızca kanal çizgileri üst üste kesişmesin diye boylarını kısalt"). Yedek: dal `yedek-s28-dal` (s28'in tam hâli).
  Kanal bölümleri, eğimler, %20 pay, taşma hesabı, karşılaştırma s28 ile AYNI. Tek fark çizim: kanal çizgisi kendi mumlarının en üst/en alt fitilinden %20 paydan ileri gitmez, dik kanalda o sınırda kesilir (kanalUc/kanalCizgi; Adım 4 ve kütüphane kartı). Eski kayıtlar (yUst/yAlt yok) kırpılmadan çizilir → formasyonlar yeniden kaydedilmeli.
- s30 telefonda onaylandı (3 Kasım 21:14): "şimdilik süper, karşılaştırma yapınca daha net değerlendirilecek". Kanal çizimi bu hâliyle kalıyor.
- SIRADAKİ: kalan formasyonları s30 ile yeniden kaydet → Binance resmiyle karşılaştırma → eşleşme oranı = ilk analiz sonucu.
- s31 (kullanıcı: "aynı paralelde uzanan üst/alt kanal çizgileri aynı boyda olmalı"; seçenekler: ikisi uzun / ikisi kısa / ORTALAMA → ortalama seçildi). Yedek: dal `yedek-s30-dal`.
  Her kanalda üst ve alt çizginin s30 kırpma uçları hesaplanır, ortalaması alınır; iki çizgi de bu ortak aralıkta çizilir. Kanallar, %20, karşılaştırma DEĞİŞMEDİ (yalnız çizim).

## 📋 YAPILACAKLAR — sıra (3 Kasım 21:34, kullanıcı)
1. Kamera testi + Binance testi (karşılaştırma ve eşleşme oranı).
2. ⏭️ BU TESTLERDEN SONRA İLK KONTROL: kütüphane görsellerinde MUM BİRLEŞMESİ. (Kullanıcı 21:35: "kütüphane için şimdilik büyük sorun değil" — düşük öncelik.)
   - Neden (bulundu): site resmi 502 px'e küçültüyor; sık mumlu görsellerde (~110+ mum) gövde 2 px, boşluk 0–1 px. Ayırma kodu (splitWideBodies) yalnızca gövde ≥3 px (merdiven bölme ≥4 px) iken çalışıyor → devreye girmiyor. Örnek: kesim ekranında 83, 84, 88, 90, 93 kutuları 2 mum.
   - Kullanıcı kararı: Binance/kamera okuması ve karşılaştırması yeterliyse, kütüphane görselleri için KAMERA OKUMASI DEĞİŞTİRİLMEYECEK (kütüphane düzenlemesi bir kez yapılır, kamera okuması sürekli kullanılır). O zaman çözüm kütüphane tarafında: görseli ~80–90 muma kırpmak.
   - Kamera da yetersiz kalırsa: sık mumda daha yüksek çözünürlükte okuma düşünülür (yedek + 2 kez kontrol, kullanıcının orijinal görseliyle test).
3. Bekleyen (en sona): siteye giriş koruması (PIN + Gmail onayı / Cloudflare Access).
- s32 BINANCE TELEFON FOTOĞRAFI — TEMİZLİKTE YEŞİL MUMLAR SİLİNİYORDU (3 Kasım 21:53, kullanıcı: "sorun nerede başladı, bul"). Yedek: dal `yedek-s31-dal`.
  Sorun okumada (Adım 2) DEĞİL, temizlikte (Adım 3, hzTemizOrj) başladı: s25/s27 zikzak ayıklaması gövdenin en koyu tonunu (Bb) grafiğin genel mum rengiyle karşılaştırıyordu. Fotoğraftaki moire çizgileri yeşil gövdelerin en koyu pikselini (0,50,8) genel yeşilden (23,93,67) 70+ uzaklaştırdı → tüm yeşil mumlar "zikzak" sanılıp çizilmedi. Kırmızılar koyu bordo çıktı ama kaldı.
  Düzeltme: mum ancak gövdenin ORTANCA rengi de genel renkten uzaksa atılır. Kontrol: kullanıcının fotoğrafında tüm mumlar geri geldi; BINANCE_TEST foto/temiz + 7 kütüphane görselinde temiz çizim piksel farkı 0 (değişiklik yok). Okuma, kanallar, kamera DEĞİŞMEDİ.
  Not: kanallar (Adım 4) zaten okuma verisinden hesaplanıyordu, yalnız arka plandaki temiz görüntü eksikti. "⚠️ Çelişki" uyarısı kesim 42'den (sağ kenardaki yarım mum, son mumlar ▼) geliyordu; site önerisi kesim 18.
- Kullanıcı (3 Kasım 22:03): kütüphaneye bazen formasyonları TELEFONLA ÇEKİP yükleyecek; ayrıca EKRAN GÖRÜNTÜSÜ testi de yapılacak → temizlik/okuma her iki kaynakla (telefon fotoğrafı + ekran görüntüsü) test edilmeli.
- s33: Eşleşme kartında yazılar fotoğrafın ALTINDA (yanda ekrandan taşıyordu). Yalnız görünüm. Yedek: `yedek-s32-dal`.
## İLK BİNANCE TESTİ (3 Kasım 22:10) — sonuç %84
- Kullanıcı Binance BTC fotoğrafını (36 mum) kütüphaneye ekledi, aynı grafiği kamerayla (2x) taradı: kamera 35 mum, en iyi eşleşme LO QM %84 (kanal profili), şekil aynı: Yükselen → İnen → Yükselen → Yatay. Kullanıcı: "aynı grafik, 95 üstü olmamalı mı?"
- Ölçüm (sitenin kendi koduyla): aynı fotoğraf ↔ kendisi %100; aynı grafiğin başka açıdan fotoğrafı %89; baştan/sondan 1 mum eksik %88–89; kamera (bulanık, 35 mum) %84.
- Neden: (1) %20 kanal testi ÇALIŞMADI — kamera 35 < formasyon 36 mum → "az mum", skor kanal profiline düştü. Formasyon ekranın tamamı olduğu için kamera (kenar payı) hiçbir zaman tüm mumları göremiyor. (2) Kanal profili karşılaştırması 1 mumluk kaymaya ve açı farkına hassas (her biri ~%10 düşürüyor).
- Önerilen (kullanıcı onayı bekliyor): A) kamera formasyonun en az ~%85'ini görüyorsa %20 testi sağdan hizalanarak çalışsın (eksik baş mumlar atlanır); B) kanal profili ±1 mum kaymayı tolere etsin. Sonra aynı grafik 95+ beklenir; FARKLI grafiklerin skorunun yükselmediği de kontrol edilecek.
- s34 SOLDAN EKSİLTME (kullanıcı onayı 22:34; "sağ taraf akış için gerekli, kesilmez; eşit görüntü için soldan mum düşülür"). Yedek: `yedek-s33-dal`.
  kanal20Kontrol: kamera formasyondan az mum görürse (en fazla formasyonun %15'i eksik) kameranın mumları formasyonun SON mumlarıyla sağdan hizalanır (son mum = kesim mumu); görülemeyen baş mumlar atlanır, her mum kendi %20 kanalında kontrol edilir. Temiz çizim formasyonun yerleşimiyle yapılır (hzCleanDraw(list,nTop,off)). %15'ten fazla eksikse yine "az mum". Sonuçta "(soldan N mum düşüldü)" yazar. Fotoğraf, bezik/kütüphane hazırlama, kamera okuması DEĞİŞMEDİ.
  Kontrol (Binance BTC fotoğrafı = formasyon, 36 mum): aynı %100; başka açı %98; 1 eksik %100 (önce "az mum"); başka açı 1 eksik %98; 3 eksik %100; 6 eksik → az mum; ilk fotoğraf (farklı an) %79. FARKLI grafikler (LO_04, LO_09, SH_01): %48–56 → %80 eşiğinin altında, elenir (seçicilik korunuyor).
- ⏸ Kullanıcı ara verdi; s34 telefonda sonra denenecek (aynı Binance grafiği kamerayla Tara → beklenen 95+).

## ✅ BİNANCE TESTİ 2 (4 Kasım 02:58) — s34 başarılı
- Formasyon: Binance BTC iPhone fotoğrafı (2x), 41 mum, LO QM 11-04 02:42.
- Sitede 2x tarama: 26 mum → "az mum" (%73). Neden: site kamerası video (16:9) açıyor, iPhone fotoğrafı 3:4 → sitenin 2x'i yatayda fotoğrafın ~%70'ini görüyor. iPhone 2x ≠ site 2x.
- Sitenin önerisiyle 1x (formasyon 41 > 33): 2 deneme → %97 (45 mum algılandı, %20 kanal 40/41, hareket %96) ve %90 (60 mum, 40/41, hareket %79). Hedef ▼ aşağı, son mumların yönü uyuyor. İlk analiz sonucu: aynı grafik %90–97.
- Fark: 60 mumlu karede (grafik dışı alan, tarih/gösterge yazıları kadraja girmiş) mumlar küçülüyor → hareket uyumu düşüyor. Kadraj grafiği doldurursa sonuç daha iyi.
- Karar: kamera 3:4 değişikliği ŞİMDİLİK YAPILMADI (sitenin 1x önerisi sorunu karşılıyor). Not: 33 eşiği sitenin kendi kamerasına göre; iPhone fotoğrafıyla hazırlanan formasyonlarda site önerisine uyulmalı.
- s35 (kullanıcı: "kullanıcı çektiği kareyi görmek istiyor; Tara'dan sonra kamera canlıya dönüyor"). Yedek: `yedek-s34-dal`.
  Sonuç kartında "📷 Taranan kare": Tara'nın okuduğu kare (yeşil alan, tam çözünürlük) kalıcı gösterilir. Karşılaştırmaya giren mumlar renkli kutulu, dışarıda kalanlar gri kesikli, pencere başı mavi dikey çizgi. Dokununca büyük görünümde açılır (iki parmakla büyütme). Okuma/karşılaştırma DEĞİŞMEDİ.
- s36 (kullanıcı: "Tara'ya basınca kare kamera ekranında kalsın; Tara düğmesi DEVAM olsun, basınca canlıya geçsin"). Yedek: `yedek-s35-dal`.
  Tara sonrası kare kamera alanında okunan kutularla DONUK kalır, düğme "▶️ Devam" olur; basınca canlı görüntü ve sensör devam eder, düğme yine "🧠 Tara". 1x/2x seçimi ve fotoğraf modundan çıkış da canlıya döndürür. Okuma Tara anındaki karede yapılır (değişmedi); donukken yalnız canlı sensör durur, kamera akışı ve kare tamponu çalışır. Sonuç kartındaki "📷 Taranan kare" (s35) de kalıyor.
- s36 telefonda TEST EDİLDİ (4 Kasım 03:11): donuk kare + "▶️ Devam" + sonuç kartındaki "📷 Taranan kare" (53 mum, son 41 karşılaştırıldı) çalışıyor.
- s37: iPhone'da sayfa kaydırılınca (adres çubuğu → resize) donuk karedeki mum kutuları siliniyordu; artık yeniden çiziliyor. Yedek: `yedek-s36-dal`.
## ⭐ İLK HEDEF GERÇEKLEŞMESİ (4 Kasım 03:11)
- Formasyon LO QM 11-04 02:42 (41 mum), hedef ▼ aşağı, sonraki 8 mum. 03:11'de (15 dk grafik, ~2 yeni mum) büyük kırmızı düşüş mumu geldi → hedef yönü TUTTU.
- Aynı anda skor %82'ye düştü (39/41, hareket %61; önce %90–97): yeni mumlar sağa eklendiği için son 41 mumluk pencere formasyondan 2 mum kaydı. Bu beklenen davranış: site formasyonun ŞİMDİ bitip bitmediğini ölçüyor; formasyon geçtikçe skor düşer.
- Fotoğraf Oku testi (4 Kasım 03:20): 1x 38 mum → LO %68 (soldan 3 düşüldü, hareket %43); 2x 37 mum → LO elendi, en üstte SH 21:15 %46. Neden: grafik 02:42'den sonra 4–5 mum ilerledi (hedef ▼ gerçekleşti), pencere kaydı. Okuma sağlıklı (moire'ye rağmen mumlar ayrı).
- s38: fotoğraf modunda kaydırınca (iPhone resize) mum kutuları siliniyordu, canlı sensör olmadığı için geri gelmiyordu → artık son çizilen kutular yeniden çiziliyor. Yedek: `yedek-s37-dal`.
- s39 (kullanıcı: "Tara doğrudan Fotoğraf Oku gibi iPhone kamerasına bağlansın, çerçeve yine olsun"; öncelik: canlı veride en net mum okuma). Yedek: `yedek-s38-dal`.
  Tara → iPhone'un kendi kamerası açılır (capture=environment, galeri yok; tam 3:4 sensör, iPhone odağı) → fotoğraf kamera alanında yeşil çerçeveyle gösterilir, mumlar kutulanır → otomatik karşılaştırma → düğme "▶️ Devam" → basınca canlı kameraya dönülür. Canlı görüntü nişan almak için kalır. Fotoğraf Oku (galeri seçeneğiyle) aynen duruyor; ikisi aynı işleyişi (fotoIsle) kullanır. Okuma/karşılaştırma DEĞİŞMEDİ.
  Not: Safari'de sitenin çerçevesi iPhone'un kendi kamera ekranının İÇİNE çizilemez; çerçeve çekimden sonra sitede görünür.
  Test (tarayıcı): Tara fotoğrafı → 36 mum, sonuç kartı + Taranan kare, düğme Devam, hata yok.
  Sonra: 1x/2x çekim önerisi eşiği (33) sitenin dar video kamerasına göreydi; iPhone kamerasıyla yeniden ölçülmeli.
