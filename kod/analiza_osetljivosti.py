# -*- coding: utf-8 -*-
# =====================================================================================
#  analiza_osetljivosti.py  —  ANALIZA OSETLJIVOSTI
#  Ispitujemo kako se optimalna vrednost cilja (ukupno zadrzavanje) menja kada
#  menjamo kljucne ulazne parametre modela. Time procenjujemo koliko je resenje
#  "osetljivo" na pojedine pretpostavke (kapacitet stanica i intenzitet saobraćaja).
# =====================================================================================

from model import resi_model                              # funkcija koja gradi i resava model
from crtanje import nacrtaj_osetljivost, nacrtaj_stubice   # funkcije za crtanje rezultata osetljivosti
import copy                                               # copy — za bezbedno kopiranje liste vozova

BROJ_STANICA = 10                           # ista pruga kao u instanci srednjih dimenzija (10 stanica)
HORIZONT = 40                               # isti vremenski horizont

# Bazni skup od 10 vozova, poredjan NAIZMENICNO (jug, sever, jug, sever, ...) zbog
# eksperimenta sa intenzitetom saobraćaja (da svaki podskup ima oba smera).
vozovi_baza = [
    {"naziv": "J1", "polazna": 0, "odredisna": 9, "ed": 0,  "md": 14, "vreme_voznje": 2, "tezina": 3},
    {"naziv": "S1", "polazna": 9, "odredisna": 0, "ed": 1,  "md": 14, "vreme_voznje": 2, "tezina": 3},
    {"naziv": "J2", "polazna": 0, "odredisna": 8, "ed": 3,  "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "S2", "polazna": 8, "odredisna": 0, "ed": 4,  "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "J3", "polazna": 1, "odredisna": 9, "ed": 6,  "md": 14, "vreme_voznje": 2, "tezina": 2},
    {"naziv": "S3", "polazna": 9, "odredisna": 1, "ed": 7,  "md": 14, "vreme_voznje": 2, "tezina": 2},
    {"naziv": "J4", "polazna": 0, "odredisna": 7, "ed": 9,  "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "S4", "polazna": 7, "odredisna": 0, "ed": 10, "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "J5", "polazna": 2, "odredisna": 9, "ed": 12, "md": 14, "vreme_voznje": 2, "tezina": 2},
    {"naziv": "S5", "polazna": 9, "odredisna": 2, "ed": 13, "md": 14, "vreme_voznje": 2, "tezina": 2},
]

# =====================================================================================
#  EKSPERIMENT 1: Osetljivost na TIP PRUGE (jednokolosecna vs dvokolosecna)
#  Menjamo kapacitet deonice: 1 = jednokolosecna (vozovi se NE mogu mimoici na deonici),
#  2 = dvokolosecna (dva voza mogu istovremeno na istoj deonici).
#  Ocekivanje: dvokolosecna pruga drasticno smanjuje (ili ponistava) ukupno kasnjenje.
# =====================================================================================
print("=== EKSPERIMENT 1: osetljivost na tip pruge (jedno/dvokolosecna) ===")  # zaglavlje
ciljevi_pruga = []                                                      # vrednosti cilja za svaki tip pruge
for kap_pruge in [1, 2]:                                                # 1 = jednokolosecna, 2 = dvokolosecna
    r = resi_model(BROJ_STANICA, copy.deepcopy(vozovi_baza), HORIZONT,  # resi model sa tim kapacitetom pruge
                   kapacitet_pruge=kap_pruge, kapacitet_stanice=2)      # menjamo samo kapacitet deonice
    ciljevi_pruga.append(r["vrednost_cilja"])                          # zapamti vrednost cilja
    print(f"  kapacitet_pruge={kap_pruge} -> ukupno zadrzavanje={r['vrednost_cilja']}")  # ispis

nacrtaj_stubice(                                                         # nacrtaj poredjenje stubicima
    ["Jednokolosecna (1)", "Dvokolosecna (2)"],                        # nazivi scenarija
    ciljevi_pruga,                                                      # vrednosti cilja
    "Osetljivost cilja na tip pruge",                                  # naslov
    "../slike/osetljivost_pruga.png",                                  # izlazni fajl
)

# =====================================================================================
#  EKSPERIMENT 2: Osetljivost na INTENZITET SAOBRAĆAJA (broj vozova na pruzi)
#  Ocekivanje: vise vozova -> vise konflikata ukrstanja -> vece ukupno kasnjenje.
# =====================================================================================
print("=== EKSPERIMENT 2: osetljivost na intenzitet saobraćaja ===")    # zaglavlje
brojevi_vozova = [2, 4, 6, 8, 10]                                       # koliko vozova ukljucujemo
ciljevi_int = []                                                        # vrednosti cilja
for n in brojevi_vozova:                                                # za svaki broj vozova
    podskup = copy.deepcopy(vozovi_baza[:n])                            # uzmi prvih n vozova (oba smera)
    r = resi_model(BROJ_STANICA, podskup, HORIZONT,                     # resi model za taj podskup
                   kapacitet_pruge=1, kapacitet_stanice=2)              # fiksni kapaciteti
    ciljevi_int.append(r["vrednost_cilja"])                            # zapamti cilj
    print(f"  broj_vozova={n} -> ukupno zadrzavanje={r['vrednost_cilja']}")  # ispis

nacrtaj_osetljivost(                                                     # nacrtaj krivu osetljivosti
    brojevi_vozova, ciljevi_int,                                        # x = broj vozova, y = cilj
    "Broj vozova na pruzi (intenzitet saobraćaja)",                     # oznaka x-ose
    "Osetljivost cilja na intenzitet saobraćaja",                      # naslov
    "../slike/osetljivost_intenzitet.png",                             # izlazni fajl
)

# =====================================================================================
#  EKSPERIMENT 3: Osetljivost na VREME VOZNJE po deonici
#  Duze vreme voznje znaci da voz duze "drzi" deonicu, pa je vise konflikata -> vece kasnjenje.
# =====================================================================================
print("=== EKSPERIMENT 3: osetljivost na vreme voznje po deonici ===")  # zaglavlje
vremena_voznje = [1, 2, 3]                                              # testiramo vremena voznje po deonici
ciljevi_vv = []                                                        # vrednosti cilja
for vv in vremena_voznje:                                              # za svako vreme voznje
    podaci = copy.deepcopy(vozovi_baza)                               # kopija baznih vozova
    for voz in podaci:                                                # svakom vozu postavi isto vreme voznje
        voz["vreme_voznje"] = vv                                      # menjamo parametar vreme_voznje
    r = resi_model(BROJ_STANICA, podaci, HORIZONT,                    # resi model
                   kapacitet_pruge=1, kapacitet_stanice=2)            # jednokolosecna pruga
    ciljevi_vv.append(r["vrednost_cilja"])                           # zapamti cilj
    print(f"  vreme_voznje={vv} -> ukupno zadrzavanje={r['vrednost_cilja']}")  # ispis

nacrtaj_osetljivost(                                                    # nacrtaj krivu osetljivosti
    vremena_voznje, ciljevi_vv,                                        # x = vreme voznje, y = cilj
    "Vreme voznje po deonici (periodi)",                              # oznaka x-ose
    "Osetljivost cilja na vreme voznje po deonici",                   # naslov
    "../slike/osetljivost_vreme_voznje.png",                          # izlazni fajl
)

print("=== Analiza osetljivosti zavrsena ===")                          # kraj
