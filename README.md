# INFORMACIJOS FAILAS – Echolokacijos šūksnių atpažinimas

1. PASKIRTIS
Ši programa apdoroja spektrogramų nuotraukas ir išgauna šikšnosparnių balsų signalus.

2. SISTEMOS REIKALAVIMAI
- Windows 7 ar naujesnė versija (64-bitų)
- Jokia papildoma programinė įranga nereikalinga (visos priklausomybės įtrauktos į išoriniame faile)

3. Quick start 
- Atsisiųsti: Sikusnosparniu_Balsu_Atpazinimas.exe
- Dukart spustelėti norėdami paleisti (arba nurodykite vaizdo kelią kaip argumentą)
- Pasirinkti vaizdą, kai bus paprašyta (PNG/JPG/BMP)
- Naudoti GUI mygtukus konfigūracijai ir apdorojimui

4. ĮVESTIES REIKALAVIMAI
- Įvestis: spektrogramos vaizdas (PNG/JPG/BMP)
- Vaizdas turi atvaizduoti laiką (x ašis) ir dažnį (y ašis)
- Šikšnosparnių balsai pasirodo kaip aukštesnio kontrasto regionai

5. IŠVESTIS
- Dvejetainio kaukės vaizdas: BWlygmuo.png
- Aptiktų regionų sąrašas su koordinatėmis:
  formatas: (x, y, plotis, aukštis)
- Tekstinis failas: output.txt su visomis regionų koordinatėmis, išrūšiuotomis pagal x padėtį

6. ALGORITMO APŽVALGA
- HSV spalvų erdvės konvertavimas
- Spalvomis paremtas slenkstis (reguliuojamas per GUI)
- Medianinis blur filtravimas triukšmui sumažinti
- Sujungtų komponentų analizė 
- Regionų filtravimas pagal:
  - Minimalus dydis (konfiguruojamas)
  - Pernelyg didelių regionų (>90% vaizdo) pašalinimas
- Rezultatai išrūšiuoti pagal x koordinatę

7. KONFIGŪRACIJA
- Parametrai saugomi: args.ini
- Gali būti keičiami per GUI arba redaguojami tiesiogiai
- Nustatymai išlieka tarp sesijų

8. PYTHON ŠALTINIS (plėtrai)
- Python 3.13+
- Reikalingas bibliotekos: opencv-python, numpy, PyQt5
- Automatiškai instaliuoja trūkstamas priklausomybes pirmą kartą

## NAUDOJIMO INSTRUKCIJOS

1. PROGRAMOS PALEIDIMAS
- Dukart spustelėti Siksnosparniu_Balsu_Atpazinimas.exe
- Pirmą kartą paleidus atsiras failų parinkiklis
- Pasirinkti spektrogramos vaizdą (PNG/JPG/BMP)
- Arba paleisti iš komandinės eilutės su vaizdo keliu:
  Siksnosparniu_Balsu_Atpazinimas.exe \"C:\\kelias\\iki\\vaizdo.png\"

2. PAGRINDINIS LANGAS
- Rodomas pasirinktas įvesties vaizdas
- Trys mygtukai viršutinėje juostoje:
  • Argumentai – pakoreguoti aptikimo parametrus
  • Ribų radimas – interaktyvus HSV spalvų pasirinkimas
  • Išvestis – peržiūrėti rezultatus ir aptiktų regionų koordinates

3. ARGUMENTAI (PARAMETRAI)
- Spustelėti „Argumentai“ mygtuką, norint atidaryti nustatymų langą
- Pakoreguoti parametrus:
  • MinRegionSize: minimalus regionų dydis (numatytasis: 2 pikseliai)
  • LH, LS, LV: apatinės HSV ribos (numatytoji: 17, 0, 248)
  • UH, US, UV: viršutinės HSV ribos (numatytoji: 180, 184, 255)
- Nustatymai automatiškai išsaugomi uždarius langą

4. RIBŲ RADIMAS (INTERAKTYVUS HSV PASIRINKIMAS)
- Spustelėti „Ribų radimas“, norint atidaryti HSV spalvų parinkiklio langą
- Gyva kaukės peržiūra atnaujinama reguliuojant slankiklius:
  • Žemesnieji H/S/V: apatinės HSV ribos
  • Aukštesnieji H/S/V: viršutinės HSV ribos
- Spauskite ESC arba uždarykite langą, norint išsaugoti pasirinkimą
- Pasirinktos vertės išsaugomos į args.ini

5. VAIZDO APDOROJIMAS
- Po parametrų pakoregavimo spustelėkite „Ribų radimas“, norint aptikti regionus
- Apdorojimas išgauna regionus, atitinkančius HSV diapazoną
- Rezultatai automatiškai išsaugomi

6. IŠVESTIS
- Spustelėti „Išvestis“, norint peržiūrėti:
  • Apdorotą dvejetainę kaukę
  • Visų aptiktų regionų koordinačių sąrašą
- Formatas: Regionas N: x=X, y=Y, plotis=PLOTIS, aukštis=AUKSTIS
- Koordinatės išrūšiuotos pagal x padėtį

7. IŠVESTIES FAILAI
- BWlygmuo.png – dvejetainė kaukė
- output.txt – aptiktų regionų koordinatės
- args.ini – nustatymai

8. PATARIMAI
- Geras kontrastas pagerina rezultatus
- Naudoti HSV slankiklius optimaliam nustatymui
- Koreguoti MinRegionSize triukšmo mažinimui
- Siaurinti HSV jei per daug regionų

9. PROBLEMŲ SPRENDIMAS
- Juoda kaukė: išplėsti HSV ribas
- Balta kaukė: susiaurinti HSV ribas
- Per mažai regionų: mažinti MinRegionSize
- Per daug regionų: didinti MinRegionSize arba siaurinti HSV
- Nepasileidžia: patikrinti failo kelią ir formatą
