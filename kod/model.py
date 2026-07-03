# -*- coding: utf-8 -*-
# =====================================================================================
#  model.py  —  Optimizacija rasporeda vozova (konstruisanje reda voznje)
#  Tema 3 — Marta Brankovic, Andjelina Minovic
#  Formulacija prema Udzbeniku, poglavlje 5.1.1.1 (model dispeciranja vozova
#  na mrezi prostor-vreme — celobrojno programiranje).
#
#  Ideja modela:
#   - Pruga je niz stanica poredjanih od severa ka jugu: S = {0,1,...,s}.
#   - Vreme je diskretizovano na periode: Q = {0,1,...,q-1}.
#   - Gradi se MREZA PROSTOR-VREME u kojoj je svaki cvor par (stanica, vreme).
#   - Svaki voz je jedna "roba" (commodity) koja putuje jedinicnim tokom od svog
#     izvorisnog (otpremnog) cvora do svog odredisnog (prispecnog) cvora.
#   - Promenljiva x^t_ij = 1 ako voz t koristi luk (i,j) u mrezi, inace 0 (luk 5-11).
#   - Troskove nose SAMO lukovi zadrzavanja (cekanja u stanici); cilj je da se
#     ukupno zadrzavanje (kasnjenje) svih vozova svede na minimum (kriterijum 5-4).
# =====================================================================================

import pulp  # PuLP — biblioteka za linearno/celobrojno programiranje (gradi LP i poziva CBC solver)


# -------------------------------------------------------------------------------------
#  Pomocna funkcija: ruta voza (niz stanica koje voz redom prolazi)
# -------------------------------------------------------------------------------------
def ruta_voza(polazna, odredisna):
    # Ako je odredisna stanica veceg indeksa, voz ide ka jugu (indeksi rastu) -> korak +1
    if odredisna >= polazna:
        return list(range(polazna, odredisna + 1))      # npr. 0->3 daje [0,1,2,3]
    # U suprotnom voz ide ka severu (indeksi opadaju) -> korak -1
    return list(range(polazna, odredisna - 1, -1))       # npr. 3->0 daje [3,2,1,0]


# -------------------------------------------------------------------------------------
#  Glavna funkcija: gradi mrezu prostor-vreme, formira model i resava ga
#
#  Parametri:
#   stanice         — broj stanica S (koristimo indekse 0..S-1)
#   vozovi          — lista recnika; svaki voz ima:
#                       'naziv'        : ime voza (npr. "V1")
#                       'polazna'      : indeks polazne stanice (otprema)
#                       'odredisna'    : indeks odredisne stanice (prispece)
#                       'ed'           : najranije/idealno vreme otpreme (period)
#                       'md'           : maksimalno dopusteno zadrzavanje (broj perioda)
#                       'vreme_voznje' : vreme voznje po jednoj deonici (broj perioda)
#                       'tezina'       : prioritet voza (mnozi cenu zadrzavanja)
#   q               — broj vremenskih perioda (duzina horizonta Q)
#   kapacitet_pruge — koliko vozova sme istovremeno na jednoj deonici (1 = jednokolosecna)
#   kapacitet_stanice — koliko vozova sme istovremeno da se zadrzava u jednoj stanici
#   ispis_solvera   — True ako zelimo da CBC ispisuje tok resavanja
# -------------------------------------------------------------------------------------
def resi_model(stanice, vozovi, q, kapacitet_pruge=1, kapacitet_stanice=1, ispis_solvera=False):

    # --- 1) Definicija problema: minimizacija (kriterijumska funkcija 5-4) ---
    problem = pulp.LpProblem("Raspored_vozova", pulp.LpMinimize)  # prazan model tipa "minimizuj"

    # --- 2) Strukture u koje skupljamo lukove i promenljive ---
    x = {}                       # x[(naziv_voza, indeks_luka)] -> binarna promenljiva (luk 5-11)
    lukovi = {}                  # lukovi[naziv_voza] -> lista lukova (od_cvora, do_cvora, cena, tip)
    izlazni = {}                 # izlazni[(voz, cvor)] -> lista promenljivih koje IZLAZE iz cvora
    ulazni = {}                  # ulazni[(voz, cvor)]  -> lista promenljivih koje ULAZE u cvor
    zadrzavanja_po_stanici = {}  # (stanica, vreme) -> lista promenljivih zadrzavanja (za ogr. 5-9)
    zauzetost_deonice = {}       # (deonica, vreme) -> lista promenljivih kretanja (za ogr. 5-10)

    # Pomocna funkcija koja registruje da promenljiva v ULAZI u cvor "do" i IZLAZI iz cvora "od"
    def upisi_incidenciju(voz, od_cvora, do_cvora, v):
        izlazni.setdefault((voz, od_cvora), []).append(v)   # v doprinosi izlaznom toku cvora "od"
        ulazni.setdefault((voz, do_cvora), []).append(v)    # v doprinosi ulaznom toku cvora "do"

    # --- 3) Za svaki voz gradimo njegov deo mreze prostor-vreme i njegove lukove ---
    for voz in vozovi:                                   # prolazimo kroz sve vozove (sve "robe")
        naziv = voz["naziv"]                             # ime voza, koristi se kao kljuc
        ruta = ruta_voza(voz["polazna"], voz["odredisna"])  # niz stanica koje voz prolazi
        ed = voz["ed"]                                   # najranije/idealno vreme otpreme
        ld = ed + voz["md"]                              # najkasnije vreme otpreme = ed + max. zadrzavanje
        vv = voz["vreme_voznje"]                         # vreme voznje po deonici (u periodima)
        tezina = voz["tezina"]                           # prioritet (cena jednog perioda zadrzavanja)

        lukovi[naziv] = []                               # lista lukova ovog voza (pocinje prazna)

        # Definisemo virtuelne cvorove: izvor 'O' (otprema) i ponor 'D' (prispece) ovog voza
        cvor_izvor = ("O", naziv)                        # iz njega krece tacno 1 jedinica toka (ogr. 5-6)
        cvor_ponor = ("D", naziv)                        # u njega ulazi tacno 1 jedinica toka (ogr. 5-7)

        # (a) IZVORISNI LUK: voz ulazi u mrezu u svojoj polaznoj stanici u idealnom trenutku ed.
        #     Eventualno kasnjenje otpreme bice modelovano kao zadrzavanje u polaznoj stanici.
        idx = len(lukovi[naziv])                         # redni broj novog luka
        v = pulp.LpVariable(f"x_{naziv}_{idx}", cat="Binary")  # binarna promenljiva za ovaj luk
        x[(naziv, idx)] = v                              # cuvamo promenljivu
        lukovi[naziv].append((cvor_izvor, ("S", voz["polazna"], ed), 0, "izvor"))  # luk bez cene
        upisi_incidenciju(naziv, cvor_izvor, ("S", voz["polazna"], ed), v)         # azuriraj incidenciju

        # (b) LUKOVI ZADRZAVANJA: u svakoj stanici na ruti voz moze cekati 1 period (cena = tezina).
        for s in ruta:                                   # za svaku stanicu na ruti voza
            for k in range(q - 1):                       # za svaki period osim poslednjeg (jer ide k -> k+1)
                idx = len(lukovi[naziv])                 # redni broj luka
                v = pulp.LpVariable(f"x_{naziv}_{idx}", cat="Binary")  # binarna promenljiva
                x[(naziv, idx)] = v                      # cuvamo promenljivu
                lukovi[naziv].append((("S", s, k), ("S", s, k + 1), tezina, "zadrzavanje"))  # cena = tezina
                upisi_incidenciju(naziv, ("S", s, k), ("S", s, k + 1), v)          # incidencija
                zadrzavanja_po_stanici.setdefault((s, k), []).append(v)            # za ogranicenje 5-9

        # (c) LUKOVI KRETANJA (voznje): sa stanice na susednu stanicu, vreme napreduje za vv (cena 0).
        for poz in range(len(ruta) - 1):                 # za svaki par uzastopnih stanica na ruti
            i = ruta[poz]                                # trenutna stanica
            j = ruta[poz + 1]                            # sledeca stanica na ruti
            deonica = (min(i, j), max(i, j))             # deonica (par susednih stanica), nezavisno od smera
            for k in range(q):                           # za svaki moguci trenutak polaska sa stanice i
                if k + vv <= q - 1:                      # samo ako voz stigne u horizont vremena
                    idx = len(lukovi[naziv])             # redni broj luka
                    v = pulp.LpVariable(f"x_{naziv}_{idx}", cat="Binary")  # binarna promenljiva
                    x[(naziv, idx)] = v                  # cuvamo promenljivu
                    lukovi[naziv].append((("S", i, k), ("S", j, k + vv), 0, "kretanje"))  # cena 0
                    upisi_incidenciju(naziv, ("S", i, k), ("S", j, k + vv), v)            # incidencija
                    for kk in range(k, k + vv):          # voz drzi deonicu tokom celog vremena voznje
                        zauzetost_deonice.setdefault((deonica, kk), []).append(v)         # za ogr. 5-10

        # (d) ODREDISNI LUKOVI: voz napusta mrezu kad stigne u odredisnu stanicu (cena 0).
        for k in range(q):                               # za svaki trenutak moguceg prispeca
            idx = len(lukovi[naziv])                     # redni broj luka
            v = pulp.LpVariable(f"x_{naziv}_{idx}", cat="Binary")  # binarna promenljiva
            x[(naziv, idx)] = v                          # cuvamo promenljivu
            lukovi[naziv].append((("S", voz["odredisna"], k), cvor_ponor, 0, "ponor"))  # luk bez cene
            upisi_incidenciju(naziv, ("S", voz["odredisna"], k), cvor_ponor, v)         # incidencija

    # --- 4) KRITERIJUMSKA FUNKCIJA (5-4): minimizuj zbir cena svih izabranih lukova ---
    #        Posto cenu nose samo lukovi zadrzavanja, ovo je ukupno (ponderisano) kasnjenje.
    problem += pulp.lpSum(
        cena * x[(naziv, i)]                                   # cena luka * (da li je luk izabran)
        for naziv in lukovi                                   # za svaki voz
        for i, (_od, _do, cena, _tip) in enumerate(lukovi[naziv])  # za svaki luk tog voza
    ), "Ukupno_zadrzavanje"

    # --- 5) OGRANICENJE (5-6): iz izvorisnog cvora svakog voza izlazi tacno 1 jedinica toka ---
    for voz in vozovi:                                        # za svaki voz
        naziv = voz["naziv"]                                  # ime voza
        problem += pulp.lpSum(izlazni[(naziv, ("O", naziv))]) == 1, f"Izvor_{naziv}"  # suma izlaza = 1

    # --- 6) OGRANICENJE (5-7): u odredisni cvor svakog voza ulazi tacno 1 jedinica toka ---
    for voz in vozovi:                                        # za svaki voz
        naziv = voz["naziv"]                                  # ime voza
        problem += pulp.lpSum(ulazni[(naziv, ("D", naziv))]) == 1, f"Ponor_{naziv}"   # suma ulaza = 1

    # --- 7) OGRANICENJE (5-8): ocuvanje toka u svim stacionarnim cvorovima (ulaz = izlaz) ---
    for voz in vozovi:                                        # za svaki voz
        naziv = voz["naziv"]                                  # ime voza
        ruta = ruta_voza(voz["polazna"], voz["odredisna"])    # stanice na ruti voza
        for s in ruta:                                        # za svaku stanicu na ruti
            for k in range(q):                                # za svaki vremenski period
                cvor = ("S", s, k)                            # stacionarni cvor (stanica, vreme)
                u = ulazni.get((naziv, cvor), [])             # promenljive koje ulaze u cvor
                iz = izlazni.get((naziv, cvor), [])           # promenljive koje izlaze iz cvora
                if u or iz:                                    # samo ako cvor uopste postoji za ovaj voz
                    problem += pulp.lpSum(u) - pulp.lpSum(iz) == 0, f"Tok_{naziv}_{s}_{k}"  # ulaz = izlaz

    # --- 8) OGRANICENJE (5-9): kapacitet zadrzavanja u stanici (broj vozova koji cekaju <= kapacitet) ---
    for (s, k), promenljive in zadrzavanja_po_stanici.items():  # za svaki par (stanica, vreme)
        problem += pulp.lpSum(promenljive) <= kapacitet_stanice, f"KapStanice_{s}_{k}"  # ogranici cekanje

    # --- 9) OGRANICENJE (5-10): kapacitet deonice / sprecavanje konflikata (ukrstanje/preticanje) ---
    #        Na jednokolosecnoj deonici u jednom trenutku sme biti najvise 1 voz (oba smera zajedno).
    for (deonica, k), promenljive in zauzetost_deonice.items():  # za svaku deonicu i svaki trenutak
        problem += pulp.lpSum(promenljive) <= kapacitet_pruge, f"KapPruge_{deonica[0]}_{deonica[1]}_{k}"

    # --- 10) Resavanje modela CBC solverom (lukovi 5-11 su vec binarni po definiciji promenljivih) ---
    solver = pulp.PULP_CBC_CMD(msg=ispis_solvera)             # podesi CBC solver (msg kontrolise ispis)
    problem.solve(solver)                                     # pokreni resavanje

    # --- 11) Sklapanje rezultata u recnik koji vracamo pozivaocu ---
    rezultat = {
        "status": pulp.LpStatus[problem.status],             # status resenja ("Optimal", "Infeasible"...)
        "vrednost_cilja": pulp.value(problem.objective),     # optimalna vrednost kriterijuma (ukupno kasnjenje)
        "raspored": izvuci_raspored(vozovi, lukovi, x),      # citljiv raspored po vozovima i stanicama
        "putanje": izvuci_putanje(vozovi, lukovi, x),        # pune putanje (vreme,stanica) za string-line dijagram
        "broj_promenljivih": len(x),                         # ukupan broj binarnih promenljivih (velicina modela)
        "broj_ogranicenja": len(problem.constraints),        # ukupan broj ogranicenja (velicina modela)
    }
    return rezultat                                          # vrati sve rezultate jednim recnikom


# -------------------------------------------------------------------------------------
#  Funkcija koja iz vrednosti promenljivih rekonstruise konkretan raspored:
#  za svaki voz daje vreme polaska/prolaska/dolaska po svakoj stanici.
# -------------------------------------------------------------------------------------
def izvuci_raspored(vozovi, lukovi, x):
    raspored = {}                                            # raspored[naziv_voza] -> {stanica: vreme}
    for voz in vozovi:                                       # za svaki voz
        naziv = voz["naziv"]                                 # ime voza
        vremena_u_stanici = {}                               # za ovaj voz: stanica -> najranije vreme prisustva
        for i, (od_cvora, do_cvora, _cena, tip) in enumerate(lukovi[naziv]):  # kroz sve lukove voza
            if x[(naziv, i)].value() is not None and x[(naziv, i)].value() > 0.5:  # ako je luk izabran (=1)
                for cvor in (od_cvora, do_cvora):            # pogledaj oba kraja luka
                    if cvor[0] == "S":                       # ako je to stacionarni cvor (stanica, vreme)
                        _, s, k = cvor                       # raspakuj stanicu s i vreme k
                        if s not in vremena_u_stanici or k < vremena_u_stanici[s]:  # zadrzi najranije vreme
                            vremena_u_stanici[s] = k         # vreme kada voz prvi put stigne u stanicu s
        raspored[naziv] = dict(sorted(vremena_u_stanici.items()))  # uredi po indeksu stanice
    return raspored                                          # vrati raspored svih vozova


# -------------------------------------------------------------------------------------
#  Funkcija koja rekonstruise PUNU putanju voza kroz mrezu prostor-vreme:
#  prati izabrane lukove od izvora 'O' do ponora 'D' i vraca uredjen niz (vreme, stanica).
#  Ovaj niz se koristi za crtanje grafikona vozova (string-line / Slika 5-1).
# -------------------------------------------------------------------------------------
def izvuci_putanje(vozovi, lukovi, x):
    putanje = {}                                            # putanje[naziv] -> lista tacaka (vreme, stanica)
    for voz in vozovi:                                      # za svaki voz
        naziv = voz["naziv"]                                # ime voza
        sledeci = {}                                        # mapa: cvor -> naredni cvor po izabranom luku
        for i, (od_cvora, do_cvora, _cena, _tip) in enumerate(lukovi[naziv]):  # kroz sve lukove voza
            if x[(naziv, i)].value() is not None and x[(naziv, i)].value() > 0.5:  # ako je luk izabran
                sledeci[od_cvora] = do_cvora                # zapamti da iz "od" idemo u "do"
        tacke = []                                          # tacke putanje (vreme, stanica)
        cvor = ("O", naziv)                                 # krećemo od izvorisnog cvora voza
        while cvor in sledeci:                              # dok god postoji naredni izabrani luk
            cvor = sledeci[cvor]                            # predji na naredni cvor
            if cvor[0] == "S":                              # ako je stacionarni cvor (stanica, vreme)
                _, s, k = cvor                              # raspakuj stanicu i vreme
                tacke.append((k, s))                        # dodaj tacku (vreme, stanica)
        putanje[naziv] = tacke                              # sacuvaj putanju voza
    return putanje                                          # vrati putanje svih vozova
