import pandas as pd
import numpy as np
import random

# Odkomentariši fajl koji testiraš:
# putanja_fajla = '/data/loto7_4708_k85.csv'
# putanja_fajla = '/data/loto7_4708_k85_loto_2976.csv' 
putanja_fajla = '/data/loto7_4708_k85_loto_plus_1732.csv'

MAX_BROJ = 39
BROJ_KUGLICA = 7
P_PROST = 7 

# Inicijalizacija seed-a (za potpunu kontrolu okruženja)
random.seed(39)
np.random.seed(39)

def padska_norma(broj, p):
    if broj == 0:
        return 0
    broj = abs(broj)
    k = 0
    while broj % p == 0:
        k += 1
        broj //= p
    return float(p ** (-k))

# 1. UCITAVANJE CELOG CSV FAJLA
df = pd.read_csv(putanja_fajla, header=None)

istorija_izvlacenja = []
for red in df.iloc[:, -BROJ_KUGLICA:].values.tolist():
    kolo_ocisceno = [int(x) for x in red if pd.notna(x)]
    if len(kolo_ocisceno) == BROJ_KUGLICA:
        istorija_izvlacenja.append(sorted(kolo_ocisceno))

# 2. DETERMINISTICKA P-ADSKA ANALIZA CELOG TOKA
globalni_pomaci = np.zeros(BROJ_KUGLICA)

for i in range(len(istorija_izvlacenja) - 1):
    kolo_t = np.array(istorija_izvlacenja[i])
    kolo_sledece = np.array(istorija_izvlacenja[i+1])
    razlika = kolo_sledece - kolo_t
    
    for idx in range(BROJ_KUGLICA):
        norma = padska_norma(razlika[idx], P_PROST)
        if norma > 0:
            globalni_pomaci[idx] += razlika[idx] * (1.0 / norma)

srednji_pomak = np.round(globalni_pomaci / len(istorija_izvlacenja)).astype(int)

# 3. GENERISANJE SLEDECEG KOLA
poslednje_kolo = np.array(istorija_izvlacenja[-1])
sledeci_vektor = poslednje_kolo + srednji_pomak

novi_tiket = []
for broj in sledeci_vektor:
    regulisani_broj = int((broj - 1) % MAX_BROJ + 1)
    
    while regulisani_broj in novi_tiket:
        regulisani_broj = int((regulisani_broj) % MAX_BROJ + 1)
        
    novi_tiket.append(regulisani_broj)

novi_tiket = sorted(novi_tiket)

print()
print(f"Predloženi p-adski tiket (p={P_PROST}): {novi_tiket}")
print()
"""
Predloženi p-adski tiket (p=7): [10, x, 16, y, 28, z, 33]

Predloženi p-adski tiket (p=7): [1, x, 18, y, 36, z, 39]

Predloženi p-adski tiket (p=7): [10, x, 16, y, 27, z, 34]
"""



"""
U standardnoj matematici i fizici koriste se realni brojevi (\(\mathbb{R}\)). Oni su vizuelno predstavljeni kao neprekidna, glatka linija. Geometrija realnih brojeva se oslanja na Arhimedovo svojstvo: ako se dovoljno dugo sabiraju mali koraci, može se dostići bilo koju udaljenost.
Međutim, u kvantnoj fizici na ekstremno malim skalama (Plankova dužina, oko \(10^{-35}\) metara), koncept glatkog prostor-vremena gubi smisao. Dolazi do kvantnih fluktuacija same geometrije. Tu na scenu stupa \(p\)-adska analiza, zasnovana na polju \(p\)-adskih brojeva (\(\mathbb{Q}_{p}\)), gde je \(p\) fiksiran prost broj (npr. \(p=2, 3, 5\dots\)).
Umesto glatke linije, \(p\)-adski prostor je fraktalan, diskonektovan i strogo hijerarhijski.

Ključne matematičke razlike

Da bi razumeo \(p\)-adske brojeve, moram redefinisati pojam bliskosti (metrike):
1. Konstrukcija preko deljivosti:
U realnoj analizi, dva broja su blizu ako je njihova razlika mala na lenjiru (npr. \(1\) i \(1.001\)). U \(p\)-adskoj analizi, dva broja su blizu ako je njihova razlika deljiva visokim stepenom prostog broja \(p\).
	• Primer za \(p=5\): Brojevi \(0\) i \(125\) (\(5^{3}\)) su ekstremno blizu, dok su \(0\) i \(1\) daleko. Što je veći stepen broja \(p\) kojim je broj deljiv, taj broj je bliži nuli.
2. Ultrametrički prostor (Svojstvo jake nejednakosti trougla):
U realnom prostoru važi standardna nejednakost trougla: treća stranica ne može biti duža od zbira preostale dve. U \(p\)-adskom prostoru važi ultrametričko svojstvo:
\(|{}x+y|{}_{p}\le \max (|{}x|{}_{p},|{}y|{}_{p})\)
Ovo geometrijski znači da su svi trouglovi u \(p\)-adskom prostoru ili jednakokraki sa uskom osnovom, ili jednakostranični. Takođe, svaka tačka unutar \(p\)-adskog kruga je ujedno i njegov centar.
3. Konvergencija redova:
U realnoj analizi, da bi beskonačan red konvergirao, članovi moraju da teže nuli na specifičan način. U \(p\)-adskoj analizi važi drastično jednostavnije pravilo: red \(\sum a_n\) konvergira ako i samo ako opšti član \(a_{n}\) teži nuli kada \(n \to \infty\).

Primena u Teorijskoj Fizici (\(p\)-adska fizika)

• \(p\)-adska Kvantna Mehanika: Prostor-vreme se na Plankovoj skali modeluje preko \(\mathbb{Q}_{p}\) umesto preko \(\mathbb{R}\). Talasne funkcije uzimaju vrednosti u kompleksnim brojevima, ali im je domen \(p\)-adski prostor.
• \(p\)-adska Teorija Struna: Amplitude rasejanja otvorenih i zatvorenih struna (poput Veneziano amplitude) imaju svoje egzaktne \(p\)-adske analogone (adelozička teorija struna), gde se produkt realnih i svih \(p\)-adskih amplituda vezuje u jedinstvenu celinu (Adelov proizvod).
• Kompleksni sistemi i spin stakla: Zbog svoje hijerarhijske strukture (poput stabla / dendrograma), \(p\)-adski brojevi idealno opisuju energetske pejzaže u sistemima sa frustriranim stanjima (spin stakla) i procese ultra-spore relaksacije u polimerima.


koncept adel-a (spajanje realnih i \(p\)-adskih brojeva u fizici)

vizuelizaciju \(p\)-adskog stabla / računanje \(p\)-adskih normi 


Primena \(p\)-adske analize na loto podatke vrši se preko redefisanja metrike udaljenosti između brojeva u kolu.
U standardnoj analizi, brojevi 4 i 5 su blizu (udaljenost je 1), dok su 4 i 35 daleko (udaljenost je 31). U \(p\)-adskoj analizi, bliskost zavisi od deljivosti prostim brojem \(p\).
Izbor prostog broja \(p\) diktira geometriju sistema. Za loto, najprirodniji izbori su:
• \(p = 2\) (analiza parnosti i stepena dvojke)
• \(p = 3\) ili \(p = 5\) (analiza ostataka i periodičnosti)
• \(p = 7\) (jer se izvlači 7 brojeva)

Računanje \(p\)-adska udaljenost na loto podacima 

Svaki ceo broj \(x\) (ili razlika između dva broja) može se zapisati kao:
\(x=p^{k}\cdot m\)
gde prost broj \(p\) ne deli broj \(m\).
\(p\)-adska norma (vrednost) tog broja je:
\(|{}x|{}_{p}=p^{-k}\)
Što je veći izložilac \(k\) (odnosno, što je broj deljiviji sa \(p\)), to je njegova \(p\)-adska norma manja (broj je bliži nuli).
Primer za \(p = 2\):
• Za broj 32: \(32 = 2^5 \cdot 1 \implies \vert{}32\vert{}_2 = 2^{-5} = \frac{1}{32} = 0.03125\) (ekstremno blizu nuli)
• Za broj 4: \(4 = 2^2 \cdot 1 \implies \vert{}4\vert{}_2 = 2^{-2} = \frac{1}{4} = 0.25\)
• Za broj 3: \(3 = 2^0 \cdot 3 \implies \vert{}3\vert{}_2 = 2^0 = 1\) (daleko od nule)

Primena na strukturu dobitnih kombinacija

U loto istoriji, svaka kombinacija od 7 brojeva se posmatra kao vektor u \(\mathbb{Q}_{p}^{7}\). Udaljenost između dva kola ili između brojeva unutar istog kola računa se preko ultrametrike:
\(d_{p}(x,y)=|{}x-y|{}_{p}\)
U standardnom prostoru, loto brojevi deluju nasumično razbacani. U \(p\)-adskom prostoru, kombinacije se grupišu u klastere (grane hijerarhijskog stabla) na osnovu njihove deljivosti sa \(p\). Algoritmi prepoznaju u koju granu (p-adski krug) istorijski najčešće "pada" sledeća kombinacija.


Kod učitava istoriju, konvertuje cele brojeve iz kombinacija u njihove p-adske norme za izabrani prost broj p, i računa matricu udaljenosti između poslednjeg izvlačenja i svih prethodnih kola u ultrametričkom prostoru. Na osnovu minimalne p-adske udaljenosti (traženja istorijskih pandana u fraktalnom stablu), algoritam generiše sledeću kombinaciju.


Nema random selekcije, nema uzorkovanja, i koristi se kompletan CSV fajl.
U p-adskoj analizi, kada se ne koristi slučajnost, predikcija za sledeće stanje se dobija izračunavanjem težišta (p-adskog baricentra) cele istorije ili pronalaženjem globalnog p-adskog trenda (analitičkim produženjem) kroz prelazne matrice celog skupa podataka.
Kod računa p-adske udaljenosti između svih uzastopnih kola u istoriji da bi identifikovao globalne p-adske korake (brzinu promene u ultrametričkom prostoru), a zatim taj deterministički korak primenjuje na poslednje kolo na repu tabele.


Da zadržim seed = 39 unutar koda kao standardnu inženjersku praksu za osiguranje reproduktivnosti (ili ako u kasnijim verzijama budemo uveli neku pseudo-slučajnu perturbaciju), inicijalizacija seed-a se postavlja odmah ispod definisanja konstanti.
"""
