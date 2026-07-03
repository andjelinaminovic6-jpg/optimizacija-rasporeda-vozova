# Seminarski rad — Tema 3: Optimizacija rasporeda vozova

**Predmet:** Upravljanje železničkim saobraćajem i transportom
**Studenti:** Marta Branković, Anđelina Minović
**Model:** poglavlje 5.1.1.1 udžbenika (dispečiranje vozova na mreži prostor-vreme)

## Sadržaj foldera (ono što se predaje)

| Fajl / folder | Opis |
|---|---|
| **`POKRENI.bat`** | **Dupli-klik za pokretanje na Windows-u (ne treba nijedan program).** |
| **`POKRENI.py`** | **Pokretač: u VS Code otvori ovaj fajl i klikni ▶ Run. Sam instalira biblioteke i pokreće sve.** |
| `requirements.txt` | Spisak potrebnih biblioteka (pulp, matplotlib). |
| `.vscode/` | Podešavanja da dugme „Run" u VS Code odmah radi. |
| `kod/` | Python (PuLP) izvorni kod modela i instanci. |
| `slike/` | Grafikoni vozova i grafici analize osetljivosti. |
| `rezultati/` | Tekstualni izlazi pokretanja skripti (zapis rezultata). |

## Pokretanje koda — najlakši način (preporučeno)

Ne treba ništa ručno da se instalira. Dovoljno je jedno od dva:

- **Windows, bez ijednog programa:** dupli-klik na **`POKRENI.bat`**.
- **U VS Code:** otvori folder, otvori **`POKRENI.py`** i klikni dugme **▶ Run**
  (ili `Ctrl + F5`).

`POKRENI.py` sam proveri i instalira `pulp` i `matplotlib`, pa pokrene sve tri
skripte iz ispravnog foldera i snimi grafike u `slike/`. Detaljno korak-po-korak
uputstvo je u **`OSNOVE_ZA_POCETNIKE.pdf`**.

## Pokretanje koda — ručno (za napredne / poznavaoce)

```bash
pip install pulp matplotlib          # instalacija biblioteka
cd kod
python3 instanca_mala.py             # instanca manjih dimenzija (4 stanice, 3 voza)
python3 instanca_srednja.py          # instanca srednjih dimenzija (10 stanica, 10 vozova)
python3 analiza_osetljivosti.py      # tri eksperimenta analize osetljivosti
```

> Napomena: skripte koriste putanje tipa `../slike/...`, pa se ručno **moraju**
> pokretati iz foldera `kod`. `POKRENI.py` to rešava automatski, zato je
> preporučeni način.

## Fajlovi u `kod/`

- `model.py` — formulacija modela (5.1.1.1) u PuLP-u; gradi mrežu prostor-vreme,
  postavlja kriterijum (5-4) i ograničenja (5-6)–(5-11) i rešava CBC solverom.
- `crtanje.py` — crtanje grafikona vozova (string-line) i grafika osetljivosti.
- `instanca_mala.py`, `instanca_srednja.py` — dve test instance.
- `analiza_osetljivosti.py` — analiza osetljivosti (tip pruge, intenzitet, vreme vožnje).
