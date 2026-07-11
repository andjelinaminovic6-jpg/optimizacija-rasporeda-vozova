# -*- coding: utf-8 -*-
# =====================================================================================
#  crtanje.py  —  Crtanje grafikona vozova (string-line / Marey dijagram)
#  Prikazuje optimalni raspored kao linije u koordinatnom sistemu PROSTOR (stanica)
#  i VREME, isto kao Slika 5-1 u Udzbeniku.
# =====================================================================================

import os                                # rad sa folderima i putanjama
import matplotlib                       # matplotlib — biblioteka za crtanje grafika
matplotlib.use("Agg")                   # "Agg" backend: crta u fajl bez otvaranja prozora (radi na serveru)
import matplotlib.pyplot as plt         # pyplot — jednostavan interfejs za crtanje


# -------------------------------------------------------------------------------------
#  Funkcija crta grafikon vozova i snima ga u zadati fajl.
#   putanje    — recnik {naziv_voza: [(vreme, stanica), ...]} (rezultat modela)
#   broj_stanica — ukupan broj stanica (za oznake y-ose)
#   naslov     — naslov grafika
#   fajl       — putanja izlazne slike (npr. "slike/instanca_mala.png")
# -------------------------------------------------------------------------------------
def nacrtaj_grafikon_vozova(putanje, broj_stanica, naslov, fajl):
    plt.figure(figsize=(9, 5))                              # nova slika zadate velicine (sirina x visina)

    for naziv, tacke in putanje.items():                   # za svaki voz i njegovu putanju
        if not tacke:                                      # ako voz nema tacaka (preskoci)
            continue                                       # idi na sledeci voz
        vremena = [t for (t, s) in tacke]                  # x-koordinate = vremena duz putanje
        stanice = [s for (t, s) in tacke]                  # y-koordinate = stanice duz putanje
        plt.plot(vremena, stanice, marker="o", label=naziv)  # crta liniju voza sa tackama i imenom u legendi

    plt.xlabel("Vreme (periodi)")                          # oznaka x-ose
    plt.ylabel("Stanica (prostor)")                        # oznaka y-ose
    plt.title(naslov)                                      # naslov grafika
    plt.yticks(range(broj_stanica),                        # postavi oznake stanica na y-osu
               [chr(ord('A') + i) for i in range(broj_stanica)])  # stanice oznacavamo slovima A, B, C, ...
    plt.grid(True, linestyle="--", alpha=0.4)              # svetla mreza radi lakseg citanja
    plt.legend(loc="best", fontsize=8)                     # legenda sa imenima vozova
    plt.tight_layout()                                     # uredi razmake da se nista ne preklapa
    os.makedirs(os.path.dirname(os.path.abspath(fajl)), exist_ok=True)  # napravi ciljni folder ako ne postoji
    plt.savefig(fajl, dpi=150)                             # snimi sliku u fajl (150 dpi = jasna rezolucija)
    plt.close()                                            # zatvori figuru i oslobodi memoriju
    print(f"  -> grafikon sacuvan: {fajl}")                # poruka da je slika napravljena


# -------------------------------------------------------------------------------------
#  Funkcija crta krivu analize osetljivosti (vrednost cilja u zavisnosti od parametra).
#   x_vrednosti — lista vrednosti parametra (x-osa)
#   y_vrednosti — lista vrednosti kriterijumske funkcije (y-osa)
#   x_oznaka    — naziv parametra
#   naslov, fajl — naslov i izlazni fajl
# -------------------------------------------------------------------------------------
def nacrtaj_osetljivost(x_vrednosti, y_vrednosti, x_oznaka, naslov, fajl):
    plt.figure(figsize=(8, 5))                             # nova slika
    plt.plot(x_vrednosti, y_vrednosti, marker="s", color="tab:red")  # kriva osetljivosti sa tackama
    plt.xlabel(x_oznaka)                                   # oznaka x-ose (parametar koji menjamo)
    plt.ylabel("Ukupno zadrzavanje (vrednost cilja)")      # oznaka y-ose (rezultat modela)
    plt.title(naslov)                                      # naslov grafika
    plt.grid(True, linestyle="--", alpha=0.4)              # mreza
    plt.tight_layout()                                     # uredi razmake
    os.makedirs(os.path.dirname(os.path.abspath(fajl)), exist_ok=True)  # napravi ciljni folder ako ne postoji
    plt.savefig(fajl, dpi=150)                             # snimi sliku
    plt.close()                                            # zatvori figuru
    print(f"  -> grafikon sacuvan: {fajl}")                # poruka


# -------------------------------------------------------------------------------------
#  Funkcija crta stubicasti (bar) dijagram — za poredjenje malog broja scenarija.
#   oznake    — lista naziva scenarija (x-osa)
#   vrednosti — lista vrednosti cilja (visine stubica)
# -------------------------------------------------------------------------------------
def nacrtaj_stubice(oznake, vrednosti, naslov, fajl):
    plt.figure(figsize=(7, 5))                             # nova slika
    stubici = plt.bar(oznake, vrednosti, color=["tab:blue", "tab:green"])  # nacrtaj stubice
    for s, v in zip(stubici, vrednosti):                   # za svaki stubic i njegovu vrednost
        plt.text(s.get_x() + s.get_width() / 2, v,         # iznad stubica upisi vrednost
                 f"{v:.0f}", ha="center", va="bottom")     # centrirano, malo iznad vrha
    plt.ylabel("Ukupno zadrzavanje (vrednost cilja)")      # oznaka y-ose
    plt.title(naslov)                                      # naslov
    plt.tight_layout()                                     # uredi razmake
    os.makedirs(os.path.dirname(os.path.abspath(fajl)), exist_ok=True)  # napravi ciljni folder ako ne postoji
    plt.savefig(fajl, dpi=150)                             # snimi sliku
    plt.close()                                            # zatvori figuru
    print(f"  -> grafikon sacuvan: {fajl}")                # poruka
