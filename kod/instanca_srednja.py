# -*- coding: utf-8 -*-
# =====================================================================================
#  instanca_srednja.py  —  INSTANCA SREDNJIH DIMENZIJA (10 izvorista/odredista)
#  Jednokolosecna pruga sa 10 stanica (A..J) i 10 vozova (5 ka jugu, 5 ka severu)
#  sa razlicitim vremenima otpreme i prioritetima. Pokazuje rad modela na realnijem,
#  gusce opterecenom saobraćaju gde nastaje vise konflikata ukrstanja/preticanja.
# =====================================================================================

from model import resi_model                 # funkcija koja gradi i resava model
from crtanje import nacrtaj_grafikon_vozova   # funkcija za crtanje grafikona vozova

# --- Definicija podataka instance ---
BROJ_STANICA = 10                             # stanice 0..9 (A..J), poredjane od severa ka jugu
HORIZONT = 40                                 # vremenski horizont Q = 0..39

# 10 vozova: 5 polazi sa juga/severa u oba smera, sa razlicitim otpremama i prioritetima.
# (polazna, odredisna) odredjuje smer; "ed" je idealno vreme otpreme; "tezina" je prioritet.
vozovi = [
    # --- 5 vozova ka JUGU (od stanice A=0 ka visim indeksima) ---
    {"naziv": "J1", "polazna": 0, "odredisna": 9, "ed": 0,  "md": 14, "vreme_voznje": 2, "tezina": 3},
    {"naziv": "J2", "polazna": 0, "odredisna": 8, "ed": 3,  "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "J3", "polazna": 1, "odredisna": 9, "ed": 6,  "md": 14, "vreme_voznje": 2, "tezina": 2},
    {"naziv": "J4", "polazna": 0, "odredisna": 7, "ed": 9,  "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "J5", "polazna": 2, "odredisna": 9, "ed": 12, "md": 14, "vreme_voznje": 2, "tezina": 2},
    # --- 5 vozova ka SEVERU (od stanice J=9 ka nizim indeksima) ---
    {"naziv": "S1", "polazna": 9, "odredisna": 0, "ed": 1,  "md": 14, "vreme_voznje": 2, "tezina": 3},
    {"naziv": "S2", "polazna": 8, "odredisna": 0, "ed": 4,  "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "S3", "polazna": 9, "odredisna": 1, "ed": 7,  "md": 14, "vreme_voznje": 2, "tezina": 2},
    {"naziv": "S4", "polazna": 7, "odredisna": 0, "ed": 10, "md": 14, "vreme_voznje": 2, "tezina": 1},
    {"naziv": "S5", "polazna": 9, "odredisna": 2, "ed": 13, "md": 14, "vreme_voznje": 2, "tezina": 2},
]

# --- Resavanje modela ---
print("=== INSTANCA SREDNJIH DIMENZIJA (10 izvorista/odredista) ===")  # zaglavlje
rezultat = resi_model(                                                  # poziv modela
    stanice=BROJ_STANICA,                                               # broj stanica
    vozovi=vozovi,                                                      # lista od 10 vozova
    q=HORIZONT,                                                         # horizont 40 perioda
    kapacitet_pruge=1,                                                  # jednokolosecna pruga
    kapacitet_stanice=2,                                                # do 2 voza istovremeno u stanici
)

# --- Ispis rezultata ---
print("Status resenja:", rezultat["status"])                           # status (treba "Optimal")
print("Velicina modela:", rezultat["broj_promenljivih"], "promenljivih,",
      rezultat["broj_ogranicenja"], "ogranicenja")                     # dimenzije modela
print("Ukupno zadrzavanje (cilj):", rezultat["vrednost_cilja"])        # vrednost kriterijuma
print("Raspored (stanica: vreme dolaska) po vozovima:")                # zaglavlje rasporeda
for naziv, vremena in rezultat["raspored"].items():                    # za svaki voz
    citljivo = {chr(ord('A') + s): k for s, k in vremena.items()}      # indeks stanice -> slovo
    print(f"  {naziv}: {citljivo}")                                    # ispis

# --- Crtanje grafikona vozova ---
nacrtaj_grafikon_vozova(                                               # string-line dijagram
    rezultat["putanje"],                                               # putanje svih vozova
    BROJ_STANICA,                                                      # broj stanica
    "Grafikon vozova — instanca srednjih dimenzija (10 stanica, 10 vozova)",  # naslov
    "../slike/instanca_srednja.png",                                   # izlazna slika
)
