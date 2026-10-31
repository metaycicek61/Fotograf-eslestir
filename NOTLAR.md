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
