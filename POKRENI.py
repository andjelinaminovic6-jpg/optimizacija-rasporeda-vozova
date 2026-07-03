# -*- coding: utf-8 -*-
# =====================================================================================
#  POKRENI.py  —  JEDINI FAJL KOJI TREBA DA POKRENES
# =====================================================================================
#
#  Sta ovaj fajl radi (ukratko):
#    1. Sam pronadje gde se nalazi (radi bez obzira odakle ga pokrenes).
#    2. Sam proveri da li su instalirane potrebne biblioteke (pulp, matplotlib)
#       i ako nisu — sam ih instalira. Ne moras nista rucno da kucas.
#    3. Sam pokrene sve tri skripte seminarskog rada, jednu po jednu.
#    4. Na kraju ti kaze gde su napravljene slike i rezultati.
#
#  KAKO SE POKRECE (dva nacina, oba rade):
#    A) U VS Code-u: otvori ovaj fajl i klikni na dugme  ▶ Run  (gore desno),
#       ili pritisni tastere Ctrl + F5.
#    B) Dupli-klik na fajl "POKRENI.bat" (ne treba ti nijedan program).
#
#  Ako nesto ne radi — pogledaj PDF uputstvo koje ide uz projekat.
# =====================================================================================

import os          # rad sa folderima i putanjama
import sys          # pristup Python interpreteru koji trenutno radi
import subprocess   # pokretanje drugih programa (pip i skripti) iz ovog programa


# -------------------------------------------------------------------------------------
#  1) Gde se nalazi ovaj fajl?
#     __file__ je putanja do ovog fajla. Od nje racunamo folder projekta i folder "kod".
#     Zato ovaj launcher radi i ako ga pokrenes duplim-klikom, i iz VS Code-a, i iz
#     bilo kog foldera — uvek sam nadje svoje fajlove.
# -------------------------------------------------------------------------------------
OVDE = os.path.dirname(os.path.abspath(__file__))   # folder u kome je POKRENI.py
KOD = os.path.join(OVDE, "kod")                      # folder "kod" (u njemu su skripte)
SLIKE = os.path.join(OVDE, "slike")                 # folder "slike" (tu se snimaju grafici)


# -------------------------------------------------------------------------------------
#  2) Osiguraj da je biblioteka instalirana. Ako nije — instaliraj je automatski.
#     "Biblioteka" je gotov tudji kod koji koristimo (pulp resava matematiku,
#     matplotlib crta grafike). Bez njih program ne moze da radi.
# -------------------------------------------------------------------------------------
def osiguraj_biblioteku(ime_za_pip, ime_za_uvoz=None):
    ime_za_uvoz = ime_za_uvoz or ime_za_pip          # obicno je isto ime za pip i za "import"
    try:
        __import__(ime_za_uvoz)                       # probaj da ucitas biblioteku
        return                                        # ako uspe — vec je instalirana, izlazimo
    except ImportError:
        pass                                          # nije instalirana — instaliramo je ispod

    print(f"   Instaliram biblioteku '{ime_za_pip}' (ovo se desava samo prvi put)...")
    # Prvo probaj obicnu instalaciju...
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", ime_za_pip]
        )
        return
    except subprocess.CalledProcessError:
        pass
    # ...ako to ne uspe (npr. nema administratorskih prava), probaj instalaciju "za korisnika".
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet", "--user", ime_za_pip]
    )


# -------------------------------------------------------------------------------------
#  3) Glavni tok programa
# -------------------------------------------------------------------------------------
def main():
    print("=" * 64)
    print("  SEMINARSKI RAD — OPTIMIZACIJA RASPOREDA VOZOVA")
    print("  Pokretanje pocinje. Sacekaj, prvi put moze da potraje minut-dva.")
    print("=" * 64)
    print()

    # (a) Proveri/instaliraj biblioteke
    print("[1/2] Proveravam potrebne biblioteke...")
    osiguraj_biblioteku("pulp")                       # biblioteka za resavanje modela
    osiguraj_biblioteku("matplotlib")                 # biblioteka za crtanje grafika
    print("      Biblioteke su spremne.")
    print()

    # (b) Napravi folder "slike" ako ne postoji (da snimanje grafika ne pukne)
    os.makedirs(SLIKE, exist_ok=True)

    # (c) Pokreni sve tri skripte. Svaku pokrecemo kao zaseban program, iz foldera "kod",
    #     da bi putanje tipa "../slike/..." unutar skripti radile ispravno.
    skripte = [
        ("instanca_mala.py",        "Instanca manjih dimenzija (4 stanice, 3 voza)"),
        ("instanca_srednja.py",     "Instanca srednjih dimenzija (10 stanica, 10 vozova)"),
        ("analiza_osetljivosti.py", "Analiza osetljivosti (tri eksperimenta)"),
    ]

    print("[2/2] Pokrecem skripte seminarskog rada...")
    print()
    for redni_broj, (fajl, opis) in enumerate(skripte, start=1):
        print("-" * 64)
        print(f"  ({redni_broj}/{len(skripte)}) {opis}")
        print("-" * 64)
        # cwd=KOD znaci: pokreni kao da si "u" folderu kod (zbog putanja ../slike/...)
        subprocess.run([sys.executable, fajl], cwd=KOD, check=True)
        print()

    # (d) Zavrsna poruka
    print("=" * 64)
    print("  GOTOVO! Sve je uspesno pokrenuto.")
    print(f"  Grafici (slike) su u folderu:  {SLIKE}")
    print("  Rezultati su ispisani iznad u ovom prozoru.")
    print("=" * 64)

    # (e) Ako smo na Windows-u, otvori folder sa slikama da ih student odmah vidi
    try:
        if os.name == "nt":                           # "nt" znaci Windows
            os.startfile(SLIKE)                        # otvori folder u Windows Explorer-u
    except Exception:
        pass                                          # ako ne uspe, nije strasno


# -------------------------------------------------------------------------------------
#  Ovaj deo pokrece funkciju main() kada se fajl pokrene direktno (Play / dupli-klik).
# -------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as greska:
        # Ako se bilo sta neocekivano desi, ispisi jasnu poruku umesto ruznog "crash"-a.
        print()
        print("!" * 64)
        print("  DOSLO JE DO GRESKE prilikom pokretanja:")
        print(f"    {greska}")
        print("  Prekopiraj ovu poruku i pogledaj PDF uputstvo (poglavlje 'Sta ako nesto ne radi').")
        print("!" * 64)
    # Sacekaj Enter da se prozor ne zatvori odmah (vazno kod duplog-klika).
    try:
        input("\nPritisni Enter da zatvoris ovaj prozor...")
    except Exception:
        pass
