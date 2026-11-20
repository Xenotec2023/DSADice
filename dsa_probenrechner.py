"""DSA 4.1 Talentprobe: exakte Wahrscheinlichkeiten (3W20 gegen drei Eigenschaften).

Regeln (DSA 4.1, Wege des Helden / Wege des Schwertes, S. 13):
- Es wird dreimal mit einem W20 gewuerfelt, je einmal gegen jeden der drei
  Eigenschaftswerte. Wird der Eigenschaftswert erreicht oder unterschritten,
  gilt der Teilwurf als gelungen.
- Mit TaP aus einem positiven Talentwert (TaW) werden misslungene Teilwuerfe
  ausgeglichen: Es wird fuer jeden misslungenen Wurf das Defizit
  (Wuerfel - Eigenschaftswert) vom TaW abgezogen. Gelingt der Ausgleich,
  ist die Probe bestanden (Rest TaP* = TaW - Summe der Defizite).
- Faellt der TaW durch Modifikatoren unter 0 (oder ist er von vornherein
  negativ), wird der Betrag unter 0 zu jedem der drei Wuerfe addiert und darf
  den jeweiligen Eigenschaftswert dennoch nicht uebertreffen
  (drei erschwerte Eigenschaftsproben, kein Ausgleich).
- Doppelte Eins (zwei oder drei 1en): automatischer Erfolg
  (spektakulaerer Erfolg).
- Doppelte Zwanzig (zwei oder drei 20en): Patzer, immer misslungen
  (dreifache 20: katastrophaler Patzer).
"""

from itertools import product


def evaluate(dice, attributes, taw):
    """Bewertet einen Wurf (d1, d2, d3) gegen (e1, e2, e3) mit TaW.

    Gibt zurueck: (bestanden: bool, special: str, tap_star: int)
    special ist eine von: "spektakulaer", "patzer", "katastrophe", "".
    """
    ones = dice.count(1)
    twenties = dice.count(20)
    if twenties >= 3:
        return False, "katastrophe", 0
    if twenties >= 2:
        return False, "patzer", 0
    if ones >= 2:
        return True, "spektakulaer", 0

    if taw < 0:
        for d, e in zip(dice, attributes):
            if d - taw > e:
                return False, "", 0
        return True, "", 0

    deficit = sum(max(0, d - e) for d, e in zip(dice, attributes))
    if deficit <= taw:
        return True, "", taw - deficit
    return False, "", 0


def probabilities(attributes, taw):
    """Exakte Wahrscheinlichkeiten fuer alle 8000 Wurfkombinationen.

    attributes: (e1, e2, e3) mit je 1..25; taw: -10..25.
    Liefert ein dict mit Anteilen (0..1) und den Restwerten in tap.
    """
    e1, e2, e3 = (max(1, min(25, e)) for e in attributes)
    result = {
        "erfolg": 0,
        "spektakulaer": 0,
        "patzer": 0,
        "katastrophe": 0,
        "tap": 0,
        "min_tap": None,
        "max_tap": None,
    }
    total = 20 ** 3
    for dice in product(range(1, 21), repeat=3):
        bestanden, special, tap = evaluate(dice, (e1, e2, e3), taw)
        if bestanden:
            result["erfolg"] += 1
            result["tap"] += tap
            result["min_tap"] = tap if result["min_tap"] is None else min(result["min_tap"], tap)
            result["max_tap"] = tap if result["max_tap"] is None else max(result["max_tap"], tap)
        if special == "spektakulaer":
            result["spektakulaer"] += 1
        elif special == "patzer":
            result["patzer"] += 1
        elif special == "katastrophe":
            result["katastrophe"] += 1
    probs = {key: count / total for key, count in result.items() if key != "tap"}
    return {
        "erfolg": probs["erfolg"],
        "misserfolg": 1.0 - probs["erfolg"],
        "spektakulaer_erfolg": probs["spektakulaer"],
        "patzer": probs["patzer"],
        "katastrophaler_patzer": probs["katastrophe"],
        "durchschnitt_tap": result["tap"] / total,
        "durchschnitt_tap_bei_erfolg": (result["tap"] / result["erfolg"]) if result["erfolg"] else 0.0,
    }
