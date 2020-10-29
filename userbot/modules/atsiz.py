# Copyright (C) 2020 Yusuf Usta.
#
# Licensed under the GPL-3.0 License;
# you may not use this file except in compliance with the License.
#

# Asena UserBot - Yusuf Usta


from random import choice
from userbot import CMD_HELP
from userbot.events import register
from userbot.cmdhelp import CmdHelp

# ================= CONSTANT =================
ATSIZ = ['Türklük ve Türkçülük ebedidir.', 'Yaşayıp yükselmek, ahlaklı ve iradesi sağlam milletlerin hakkıdır.', 'Bir milletin yürütücü kuvvetine “ülkü” denir.', 'Dil, bir milletin en değerli malıdır.', 'En büyük kahramanlığı yapsanız bile en küçük karşılığını beklemeyiniz.', 'Hakkımızı, atalar mirasını istiyoruz. Alacağız da.', 'İlim ve hakikat, siyasetin oyuncağı olamaz.', 'İstek ve inanç, her güçlüğü devirir.', 'Milletleri millet yapan, uğrunda ölecekleri yüksek ülkülere bağlanmış olmalarıdır.', 'Emperyalizm bir milletin başka milletleri hükmü altına alması demektir.', 'İlk düşüneceğimiz şey: Türkiye’de Türk Kültürü’nü hakim kılmak, yabancı tesirleri silkip atmaktır.', 'İnsan meziyet sahibi olmaya mecburdur.', 'Dün tembelliğinden bahsolunan bu millet, kendine göre en ağır vergileri ödeyen millettir.', 'Biz bin yıl sonrasına hitap ediyoruz.', 'Ahlak, millet yapısının temelidir. O olmadan hiç bir şey olmaz.', 'Barış, savaşın başka metotlarla devamı ve silahlı savaşa hazırlığın ayrı bir şeklidir.', 'Büyümek istemeyen bir millet küçülmeye mahkumdur.', 'Fedakarlık insanları da, milletleri de asilleştirir, kahramanlaştırır.', 'Bir millete, geçmişini unutturmak, onu yok etmenin ilk şartıdır.', 'Yüksel ki yerin bu yer değildir. Dünyaya gelmek hüner değildir.', 'Ülküsüz topluluk ye!rinde sayan, ülkülü topluluk yürüyen bir yığındır.', 'Türkler hem ahlaklı, hem de iradeli bir millettir. Zaten bu ikisi, çok kere birlikte bulunur.', 'Milletler fedakar fertlerin çokluğu nisbetinde yükselir.', 'Türk’ü, gerçek olarak, Türk’den başkası sevemez.', 'Bize bir gençlik lazımdır. Temelinde cehalet, duvarlarında riya, tavanlarında dalkavukluk bulunmasın.', 'Biz Türküz. Tarihimize ve en yakın mazimize dayanarak Türküz der ve bundan haklı bir iftihar duyarız.', 'Dinin bir ruh ihtiyacı olduğunu bilim kabul etmiştir.', 'Dünyaya yayılmaya çalışmak, dünyadan silinmek korkusunun tepkisidir.', 'Hem duyguya, hem de düşünceye dayanan milli şuur, bir milletin manevi kuvvetlerinden en önemlisidir.', 'İktisadi doktrinler çabuk değişir, değişmeyen prensipler, milliyetçilik prensipleridir.', 'Bir topluluktan müşterek ülküyü kaldırın, insanların hayvanlaştığını görürsünüz.', 'Milletimiz ne fedakarlıkta, ne millet severlikte, ne yaratıcılıkta ve ne de müminlikte hiçbir milletten geri değil ve hatta ileridir.', 'Her Türkçü, bulunduğu yerin görevini inançla yaparsa, Türkçülük ülküsü sağlamlaşır. Türklük güçlenir.', 'Gittikçe uyanan milli şuur karşısında gafiller ve hainler, Türk milletini daha çok aldatamayacaklardır. Kızıl elmanın yolunu kapatamayacaklardır.', 'Dil; bir milletin sembolüdür. O milleti bir arada tutan ve yok olmasını engelleyen biricik faktördür.', 'Bizim için önemli olan, dost kılıklı yabancıların milli ülküyü güya milli çıkar adına baltalamasının önüne geçmektir.', 'Bir millet için, büyümekten korkmak kadar ölümcül düşünce olamaz.', 'Bana göre Ticanilik, Nurculuk, yobazlık, komünizm ve partizanlık gibi hastalıkların sebepleri, milli ülküden yoksunluktur.', 'Yabancı hakimiyetler altında kırılan, sürülen milyonlarca ırkdaşımızın bulunması bize vazifemizin büyüklüğünü ve şerefini hatırlatsın.', 'Ülkü yolunda yürüyen milletler başka milletleri hem korkutur, hem kendisine hayran bırakır. sozadresi.com', 'Türk Milleti, üç bin yıldan beri vardır. O’nun varoluşu, büyüklüğü, gücü, tarihe damgasını vuruşu, yalnız milli karakteriyle mümkün olabilmiştir.', 'Yalnız kazancımızı, midemizi, maddemizi düşünmeyelim. Bunu hayvanlar da yapar. Daha çok manaya, düşünceye, ülküye dönelim. İnsanlık budur.', 'Ülküler, gerçekle hayalin karışmasından doğmuş olan, düne bakarak yarını arayan, milletlere hız veren ve uğrunda ölünen büyük dileklerdir.', 'Bir millet, büyümek ve iş yapabilmek için kendisinin büyük bir millet olduğu inancını duymalıdır.', 'Büyük adam hususi hayatında da yüksek ve temiz olan adamdır. Bir takım meziyetleri bulunan bir rezil hiç bir zaman büyük değildir.', 'Gerçekten Türkçü olmak kolay değildir. Her önüne gelen Türkçü olamayacağı gibi, her Türkçüyüm diyen de Türkçü olamaz.', 'Her iman ahlaka yürüyeceğine göre, Türkçülük’de de sağlam bir ahlakın bulunması birinci şarttır.', 'İki millet arasındaki gerginlik ikisi arasında kalmıyorsa bunun sebebi, o ikisi arasındaki savaş sonunda doğacak durumun şu veya bu milletleri de başka açılardan ilgilendirecek nitelik taşımasıdır.', 'Milattan önceki yüzyıllarda Hunlar, çocuklarını, topluma faydalı olabilecek bir terbiye ile yetiştirirlerdi. Topluma faydası dokunmayacak kadar yaşlanmış olanlar ise intihar ederlerdi.', 'Herkes barıştan söz ettiği halde herkes savaşıyor. Çünkü herkes kendi yarınını, öbür gününü, daha uzak geleceğini emniyete almak istiyor. Çünkü kimse kimseye güvenmiyor. Çünkü herkes birbirinden korkuyor.', 'Eskiden Türkler arasında bir ayrılık konusunda Sünnilik-Şiilik meselesi de artık bahis konusu sayılmaz. Bunların hepsi Müslüman Türk‘dür ve Müslümanlığı anlayıştaki içtihat farkları, artık Türkler arasında ikilik doğuramaz.', 'Bize yalnız dans etmesini, iyi giyinmesini, kur yapmasını ve aşık olmasını bilen gencin lüzumu yoktur. Bize bugün mesleğinde usanmadan çalışacak, yarın hudutta göz kırpmadan ölebilecek genç lazımdır.', 'Ahlakın meydana gelmesinde en önemli sebep soydur. Bir toplumun ahlakı, soyunun karışması ile değişebilir.', 'Ümit, en sonra terk olunan şeydir.Ümitlerimiz kırık değildir. Uğrunda çalışanlar, ızdırap çekenler, ölenler bulundukça Türkçülük mutlaka zafer olacaktır.', 'Kendimize dönelim. Ahlak, edebiyat, musiki, giyim, zevk, yemek, eğlence, hukuk, aile, adet, anane ve her şeyde milli olalım.', 'Haritalarda ırkımızın yaşadığı yerlere baktık, milletimize fenalık edenleri tarihte okuduk ve milli kini ateşten damgalar gibi kalbimize yazdık.', 'Dün sultanlara taptığı zannolunan bu millet, milli mevcudiyetini tehlikede görünce bir kumandanın emri altına girmiş, hayatını ortaya atarak istiklalini ve istikbalini kazanmıştır.', 'Komünistlikten hüküm giymiş olanlar, Türk Milliyetçiliği’nin kökünü kazımak için kampanya açmış olan partiler, İslam beynelmilelciliği davası güdenler de hep milliyetçi olduklarını söylerler. Türkçülük bu türlü eksik ve yanlış milliyetçiliklerin hepsini reddeder.', 'Eski topraklarımızı kurtarmak isteğimiz emperyalizm ise emperyalistiz. Türkistan’ı, İdil-Ural’ı, Azerbaycan’ı, Kafkasya’yı, Kırım’ı ve Türkler‘in yaşadığı başka yerleri is!temek emperyalizm ise kutlu bir düşüncedir.', 'Maddileşmiş bir insan vatan için ölür mü? Bencil bir insan muhtaçlara yardım eder mi? Milletine inanmayan bir adam yabancı ile işbirliği yapmaz mı? Erdemi gülünç bulan birisi çalıp çırpmaz mı?', 'Yerinde kullanıldığı zaman bir hastayı diriltecek olan ilaç, yanlış kullanılırsa insanı öldürebilir. O zaman suç ilaçta değil, yanlış kullanandadır.', 'İnsanları insan yapan, büyük bir düşüncenin ardından koşmalarıdır. İnsan, şeref için ve muhteşem saydığı bir gaye için ölmesini bilen yaratıktır. sozadresi.com', 'Dünyadaki bütün milletler, yabancı devlet hakimiyetinde kalan soydaşlarını kendileriyle birleştirmek için silahlı ve silahsız savaşlar yaparlar. Bunun adı emperyalizm değildir, irredantelizmdir ki makbul bir davranıştır.', 'Milleti yapan unsurlardan biri de din olduğuna göre, Türkler‘in dini üzerinde de durmaya mecburuz. Hiç şüphe yok ki, Türkler‘in dini müslümanlıktır. Eski dinimiz olan Şamanlık’dan da bazı unsurlar alarak bir Türk müslümanlığı haline gelen bu din, on yüzyıldan beri bizim milli dinimiz olmuştur.', 'Bir gün ülkede milliyetçi geçinen politikacılar, yöneticiler, sanatçılar, aydınlar hiç bir çıkar kaygısına düşmeden, yiğitçe, korkusuzca Türkçü söylemlerde, Türkçü tavırlarla milletin karşısına çıkarlarsa o gün Türkçülük büyük bir utkuya yaklaşır.', 'Türkçülük dün bir kaynaktı, bugün bir çaydır. Yarın coşkun bir ırmak olacak ve önünde yabancı duygu ve düşüncelerden gelen bütün engeller yıkılacaktır. – Türkçülük insanlara hiç bir vaatte bulunmuyor, maddi veya manevi bir şey vermiyor. Yalnız istiyor… Fedakarlık ve feragat istiyor.']
ATSIZ_SIIR = [
    """
Dilek yolunda ölmek Türklere olmaz tasa,
Türk'e boyun eğdirir yalnız türeyle yasa;
Yedi ordu birleşip kaşımızda parlasa
Onu kanla söndürür parçalarız, yeneriz.

Biz Turfanı yarattık uyku uyurken Batı
Nuh doğmadan kişnedi ordularımızın atı.
Sorsan şöyle diyecek gök denilen şu çatı:
Türk gücü bir yıldırım, Türk bilgisi bir deniz.

Delinse yer, çökse gök,yansa, kül olsa dört yan,
Yüce dileğe doğru yine yürürüz yayan.
Yıldırımdan, tipiden, kasırgadan yılmayan,
Ölümlerle eğlenen tunç yürekli Türkleriz...
    """,
    """
Pınar başına geldi
Bir elinde güğümü;
Çattı yay kaşlarını
Görünce güldüğümü,
Bağlamıştı gönlümü
Saçlarını düğümü.
Bilmiyordum bu örgü
Acaba bir büğümü?

Sordum: nerdedir yerin?
Nedir senin değerin?
Yedi kral vurulmuş,
Ne bu ceylan gözlerin? Hangisine varırsın
Bu yedi ünlü erin?
Şöyle dedi bakarak
Göklere derin derin:

Kıralların taçları
Beni bağlar büğü mü?
Orduları açamaz
Gönlümdeki düğümü.
saraylarda süremem
Dağlarda sürdüğümü.
Bin cihana değişmem
Şu öksüz Türklüğümü...
""",
"""
Türk duygusu her Türkçüye en tatlı kımızdır;
Türk ülküsü candan da aziz bayrağımızdır.

Bayrak ki onun gölgesi Bozkurtları toplar;
Bayrak ki bütün kaybedilen yurtları toplar.

Nerden geliyor? Tanrıkut'un ordularından!
Lakin bize bir beyt okuyor kutlu yarından:

Darbeyle gönüllerde yatan ülkü silinmez!
Atsız yere düşmekle bu bayrak yere inmez!...
""",
"""
Ey vatan!
Güzel turan!
Sana feda biz varız.
Düşman oğlu meydana çık!
Kahramanlık kimde ise anlarız.
""",
"""
Ey sen ki kül ettin beni onmaz yakışınla, 
Ey sen ki gönüller tutuşur her bakışınla! 
Hançer gibi keskin ve çiçekler gibi ince 
Çehren bana uğrunda ölüm hazzı verince 
Gönlümdeki azgın devi rüzgarlara attım; 
Gözlerle günah işlemenin zevkini tattım. 
Gözler ki birer parçasıdır sende İlahın, 
Gözler ki senin en katı zulmün ve silahın, 
Vur şanlı silahınla gönül mülkü düzelsin; 
Sen öldürüyorken de vururken de güzelsin!""",
"""
Bu gün yollanıyorken bir gurbete yeniden 
Belki bir kişi bile gelmeyecektir bize. 
Bir kemiğin ardında saatlerce yol giden 
itler bile gülecek kimsesizliğimize 

Gidiyorum: gönlümde acısı yanıkların... 
Ordularla yenilmez bir gayız var kanımda. 
Dün benimle birlikte gülen tanıdıkların 
Yalnız bir hatırası kaldı artık yanımda.
""",
"""
Dilek yolunda ölmek Türklere olmaz tasa,
Türk’e boyun eğdirir yalnız türeyle yasa;
Yedi ordu birleşip karşımızda parlasa
Onu kanla söndürüp parçalarız, yeneriz .

Biz Tufanı yarattık uyku uyurken batı,
Nuh doğmadan kişnedi ordularımızın atı.
Sorsan şöyle diyecek gök denilen şu çatı:
Türk gücü bir yıldırım Türk bilgisi bir deniz.

Delinse yer, çökse gök yansa kül olsa dört yan,
Yüce dileğe doğru yine yürürüz yayan.
Yıldırımdan tipiden kasırgadan yılmayan,
Ölümlerle eğlenen tunç yürekli Türkleriz…
""",
"""
Atandan kalmış olan kılıcı iyi bile,
Onu bütün gücünle vuracaksın çağında.
Savaş….. Bunun tadını ey Türk sen bulamazsın,
Ne sevgili yanında, ne baba ocağında.

Savaşmaktan kaçınır, kim varsa alnı kara;
Kan dökmeyi bilenler hükmeder topraklara…
Kazanmanın sırrını bilmiyorsan git, ara,
“Çanakkale” ufkunda, “Sakarya” toprağında.

Siyasette muhabbet… Hepsi yalan palavra…
Doğru sözü “Kül Tegin” kitabesinde ara…
Lenin’den bahsederse karşında bir maskara,
Bir tebessüm belirsin sadece dudağında.

Yatağında ölmeyi hatırından sök, çıkar!
Döşeğin kara toprak, yorganındır belki kar…
Sen gurbette kalırsan, ben ölürsem ne çıkar?
Ruhlarımız buluşur elbet Tanrıdağı’nda…
""",
"""
Mukadderat isterse seni yoldan çevirsin,
Sen hele bu yollarda yıpranarak aşın da,
Varsın bütün ömrünce bir an nasip olmasın,
Yorgunluğunu gidermek serin bir su başında.

Bir gülüşten ne çıkar, ne çıkar ağlamaktan?
Kullar kancıklık eder, bela bulursun Hak’tan.
Gün olur ki bir yudum su ararsın bataktan,
Gün olur ki bir tutam tuz bulunmaz aşında.

Bir çığ gibi yürürsün bir lahza durmaksızın,
Bir ilahi kaynaktan geliyor çünkü hızın.
Duygular ölmüştür… Tapınılan bir kızın,
Bir füsun bulamazsın gözlerinde, kaşında.

Iztırabı kanına katta göz kırpmadan iç!
Varsın gülsün ardından, ne çıkar, bir iki piç…
Bu varlık dünyasında yalnız senin hiç mi hiç
Bir şeyin olmayacak… Hatta mezar taşın da…
""",
"""
Yer bulmasın gönlünde ne ihtiras, ne haset.
Sen bütün varlığına yurdumuzun malısın.
Sen bir insan değilsin; ne kemiksin, ne de et;
Tunçtan bir heykel gibi ebedi kalmalısın.

Iztırap çek, inleme… Ses çıkarmadan aşın.
Bir damlacık aksa da, bir acizdir göz yaşın;
Yarı yolda ölse de en yürekten yoldaşın
Tek başına dileğe doğru at salmalısın.

Ezilmekten çekinme… Gerilmekten sakın!
İradenle olmalı bütün uzaklar yakın,
Dolu dizgin yaparken ülküne doğru akın,
Ateşe atılmalı, denize dalmalısın.

Ölümlerden sakınma, meyus olmaktan utan!
Bir kere düşün nedir seni dünyada tutan?
Mefkuresinden başka her varlığı unutan
Kahramanlar gibi sen, ebedi kalmalısın…
"""
]

@register(outgoing=True, pattern="^.atsız$")
async def atsiz(e):
    """ Atsız sözlüğü """
    await e.edit(f"`{choice(ATSIZ)}`")

@register(outgoing=True, pattern="^.atsız şiir")
async def atsizs(e):
    """ Atsız şiir sözlüğü """
    await e.edit(f"`{choice(ATSIZ_SIIR)}`")


CmdHelp('atsız').add_command(
    'atsız', None, 'Bir Atsız sözü.'
).add_command(
    'atsız şiir', None, 'Bir Atsız şiiri.'
).add()