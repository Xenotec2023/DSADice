"""Tests für die Wahrscheinlichkeitsberechnung (python3 test_probenrechner.py)."""

from itertools import product

from dsa_probenrechner import evaluate, probabilities


def brute_force(attributes, taw):
    n = 0
    for dice in product(range(1, 21), repeat=3):
        bestanden, _, _ = evaluate(dice, attributes, taw)
        if bestanden:
            n += 1
    return n / 8000


def test_referenzwert():
    p = probabilities((13, 12, 14), 8)
    assert abs(p["erfolg"] - 0.859) < 0.001


def test_doppel_eins():
    assert abs(probabilities((1, 1, 1), 0)["erfolg"] - 58 / 8000) < 1e-12
    assert abs(probabilities((1, 1, 20), 0)["erfolg"] - 58 / 8000) < 1e-12


def test_doppel_zwanzig():
    p = probabilities((20, 20, 20), 25)
    assert abs(p["misserfolg"] - 58 / 8000) < 1e-12
    assert abs(p["katastrophaler_patzer"] - 1 / 8000) < 1e-12


def test_negativer_taw():
    p = probabilities((12, 12, 12), -3)
    assert abs(p["erfolg"] - 762 / 8000) < 1e-12


def test_brute_force():
    for taw in (0, 1, 3, 8, 15, 25):
        for attributes in [(10, 10, 10), (13, 12, 14), (8, 14, 17)]:
            p = probabilities(attributes, taw)
            assert abs(p["erfolg"] - brute_force(attributes, taw)) < 1e-12


def test_monotonie_taw():
    prev = -1
    for taw in range(-10, 26):
        cur = probabilities((13, 12, 14), taw)["erfolg"]
        assert cur >= prev - 1e-12
        prev = cur


def test_summe_eins():
    p = probabilities((14, 11, 17), 4)
    assert abs(p["erfolg"] + p["misserfolg"] - 1) < 1e-12


if __name__ == "__main__":
    for name, func in sorted(globals().items()):
        if name.startswith("test_"):
            func()
            print(f"{name}: OK")
    print("Alle Tests OK")
