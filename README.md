# DSADice – Talentrechner (DSA 4.1, 3W20-Probe)

Berechnet **exakt** (alle 8000 Wurfkombinationen, keine Simulation), wie wahrscheinlich
eine Talentprobe nach den Regeln des Schwarze-Auges-Regelwerks 4.1 gelingt.

## Start

```bash
python3 dsa_probenrechner_gui.py
```

Voraussetzung: Python 3 mit tkinter (in offiziellen Python-Installationen enthalten;
sonst je nach Distribution: Debian/Ubuntu `sudo apt install python3-tk`,
Fedora/RHEL/openSUSE `sudo dnf install python3-tkinter`).

## Eingaben

- Drei Eigenschaftswerte (je 1–25)
- Talentwert TaW (−10 bis 25)

## Umgesetzte Regeln (DSA 4.1, Wege des Helden / Wege des Schwertes, S. 13)

- Drei W20, je einer gegen jeden Eigenschaftswert. Erreicht/Unterschreiten = gelungen.
- Misslungene Teilwürfe werden mit Talentpunkten ausgeglichen: Die Summe der Defizite
  (Würfel − Eigenschaftswert) darf den TaW nicht übersteigen, sonst misslingt die Probe.
- TaW unter 0 (auch durch Modifikatoren): Betrag unter 0 wird zu jedem der drei Würfe
  addiert und darf den jeweiligen Eigenschaftswert dennoch nicht übertreffen.
- Doppelte 1 (auch dreifach): automatischer Erfolg (spektakulärer Erfolg).
- Doppelte 20 (auch dreifach): Patzer, immer misslungen; dreifache 20 = katastrophaler Patzer.

## Ausgaben (grafische Oberfläche)

- Erfolgschance / Misserfolgsquote (mit Balkendiagramm)
- Anteil spektakulärer Erfolge (Doppel-1) und Patzer (Doppel-20)
- Durchschnittlich übrige TaP* bei Erfolg
- Häufigkeit des katastrophalen Patzers (Dreifach-20)

## Tests

```bash
python3 test_probenrechner.py
```

Prüft u. a. den Referenzwert 13/12/14 mit TaW 8 → 85,94 % (publizierte DSA-4.1-Referenz:
85,9 %), Doppel-1/Doppel-20-Sonderregeln, negative TaW und Brute-Force-Vergleiche.
