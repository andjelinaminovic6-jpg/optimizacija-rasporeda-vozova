# -*- coding: utf-8 -*-
# =====================================================================================
#  instanca_mala.py  —  INSTANCA MANJIH DIMENZIJA
#  Jednokolosecna pruga sa 4 stanice (A, B, C, D) i 3 voza (dva ka jugu, jedan ka severu).
#  Cilj: pokazati kako model resava ukrstanje/preticanje na malom, citljivom primeru.
# =====================================================================================

from model import resi_model                 # uvozimo funkciju koja gradi i resava model
from crtanje import nacrtaj_grafikon_vozova   # uvozimo funkciju za crtanje grafikona vozova

# --- Definicija podataka instance ---
BROJ_STANICA = 4                              # stanice: 0=A, 1=B, 2=C, 3=D (od severa ka jugu)
HORIZONT = 16                                 # broj vremenskih perioda (Q = 0..15)

# Spisak vozova: svaki voz ima polaznu/odredisnu stanicu, vreme otpreme, max zadrzavanje,
# vreme voznje po deonici i tezinu (prioritet).
vozovi = [
    # Voz V1: ide ka jugu (A -> D), idealno krece u trenutku 0, najvisi prioritet (3)
    {"naziv": "V1", "polazna": 0, "odredisna": 3, "ed": 0, "md": 8, "vreme_voznje": 2, "tezina": 3},
    # Voz V2: ide ka jugu (A -> C), krece malo kasnije (trenutak 2), srednji prioritet (2)
    {"naziv": "V2", "polazna": 0, "odredisna": 2, "ed": 2, "md": 8, "vreme_voznje": 2, "tezina": 2},
    # Voz V3: ide ka severu (D -> A), krece u trenutku 0, najnizi prioritet (1) -> najverovatnije ceka
    {"naziv": "V3", "polazna": 3, "odredisna": 0, "ed": 0, "md": 8, "vreme_voznje": 2, "tezina": 1},
]

# --- Resavanje modela za zadatu instancu ---
print("=== INSTANCA MANJIH DIMENZIJA ===")                              # zaglavlje ispisa
rezultat = resi_model(                                                  # poziv glavne funkcije modela
    stanice=BROJ_STANICA,                                               # broj stanica
    vozovi=vozovi,                                                      # lista vozova
    q=HORIZONT,                                                         # vremenski horizont
    kapacitet_pruge=1,                                                  # jednokolosecna pruga (1 voz po deonici)
    kapacitet_stanice=2,                                                # u stanici mogu cekati do 2 voza
)

# --- Ispis rezultata ---
print("Status resenja:", rezultat["status"])                           # da li je nadjeno optimalno resenje
print("Velicina modela:", rezultat["broj_promenljivih"], "promenljivih,",
      rezultat["broj_ogranicenja"], "ogranicenja")                     # dimenzije modela
print("Ukupno zadrzavanje (cilj):", rezultat["vrednost_cilja"])        # optimalna vrednost kriterijuma
print("Raspored (stanica: vreme dolaska) po vozovima:")                # zaglavlje rasporeda
for naziv, vremena in rezultat["raspored"].items():                    # za svaki voz
    citljivo = {chr(ord('A') + s): k for s, k in vremena.items()}      # zameni indeks stanice slovom
    print(f"  {naziv}: {citljivo}")                                    # ispis rasporeda voza

# --- Crtanje grafikona vozova i snimanje slike ---
nacrtaj_grafikon_vozova(                                               # crtamo string-line dijagram
    rezultat["putanje"],                                               # pune putanje vozova
    BROJ_STANICA,                                                      # broj stanica za y-osu
    "Grafikon vozova — instanca manjih dimenzija",                     # naslov
    "../slike/instanca_mala.png",                                      # gde se snima slika
)
