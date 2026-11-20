"""DSA 4.1 Talentrechner: Wahrscheinlichkeiten fuer Talentproben (3W20).

Start:  python3 dsa_probenrechner_gui.py
"""

import tkinter as tk
from tkinter import messagebox, ttk

from dsa_probenrechner import probabilities


MIN_EIGENSCHAFT = 1
MAX_EIGENSCHAFT = 25
MIN_TAW = -10
MAX_TAW = 25


class Probenrechner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DSA 4.1 – Talentrechner (3W20-Probe)")
        self.resizable(False, False)

        main = ttk.Frame(self, padding=12)
        main.grid(sticky="nsew")

        eingaben = ttk.LabelFrame(main, text="Eingaben", padding=10)
        eingaben.grid(row=0, column=0, sticky="ew")

        self.entries = []
        labels = (
            "Eigenschaft 1 (z. B. Mut):",
            "Eigenschaft 2 (z. B. Klugheit):",
            "Eigenschaft 3 (z. B. Gewandtheit):",
            "Talentwert (TaW):",
        )
        for i, label in enumerate(labels):
            ttk.Label(eingaben, text=label).grid(row=i, column=0, sticky="w", pady=3)
            entry = ttk.Spinbox(
                eingaben,
                from_=MIN_TAW if i == 3 else MIN_EIGENSCHAFT,
                to=MAX_TAW if i == 3 else MAX_EIGENSCHAFT,
                width=6,
            )
            entry.grid(row=i, column=1, sticky="w", pady=3, padx=(8, 0))
            entry.insert(0, "12" if i < 3 else "6")
            self.entries.append(entry)

        ttk.Button(eingaben, text="Berechnen", command=self.berechnen).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0)
        )

        ergebnisse = ttk.LabelFrame(
            main, text="Ergebnisse (exakt berechnet über alle 8000 Wurfkombinationen)", padding=10
        )
        ergebnisse.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        self.balken = {}
        texte = {
            "erfolg": "Probe gelungen:",
            "misserfolg": "Probe misslungen:",
            "spektakulaer": "   · spektakulärer Erfolg (Doppel-1):",
            "patzer": "   · Patzer (Doppel-20):",
        }
        for row, key in enumerate(("erfolg", "misserfolg", "spektakulaer", "patzer")):
            ttk.Label(ergebnisse, text=texte[key]).grid(row=row, column=0, sticky="w")
            canvas = tk.Canvas(
                ergebnisse, width=250, height=18, bg="#ffffff",
                highlightthickness=1, highlightbackground="#b0b0b0",
            )
            canvas.grid(row=row, column=1, padx=8, pady=2)
            farbe = "#3fa34d" if key in ("erfolg", "spektakulaer") else "#c0392b"
            prozent = ttk.Label(ergebnisse, text="–", width=10, anchor="w")
            prozent.grid(row=row, column=2, sticky="w")
            self.balken[key] = (canvas, farbe, prozent)

        self.details = ttk.Label(main, text="", anchor="w", justify="left")
        self.details.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        hinweis = ttk.Label(
            main,
            text=("Regeln DSA 4.1: Misslungene Teilwürfe werden mit Talentpunkten ausgeglichen.\n"
                  "Negativer TaW: Erschwernis auf jeden der drei Würfe. Doppel-1 = automatischer Erfolg,\n"
                  "Doppel-20 = Patzer."),
            foreground="#555555",
            wraplength=460,
            justify="left",
        )
        hinweis.grid(row=3, column=0, sticky="ew", pady=(10, 0))

    def lies_werte(self):
        eigenschaften = []
        for entry in self.entries[:3]:
            wert = int(entry.get())
            if not MIN_EIGENSCHAFT <= wert <= MAX_EIGENSCHAFT:
                raise ValueError(f"Eigenschaftswerte müssen zwischen {MIN_EIGENSCHAFT} und {MAX_EIGENSCHAFT} liegen.")
            eigenschaften.append(wert)
        taw = int(self.entries[3].get())
        if not MIN_TAW <= taw <= MAX_TAW:
            raise ValueError(f"Der Talentwert muss zwischen {MIN_TAW} und {MAX_TAW} liegen.")
        return eigenschaften, taw

    def berechnen(self):
        try:
            eigenschaften, taw = self.lies_werte()
        except (ValueError, TypeError):
            messagebox.showerror("Ungültige Eingabe", "Bitte ganze Zahlen in den erlaubten Bereichen eingeben.")
            return

        p = probabilities(eigenschaften, taw)
        anteile = {
            "erfolg": p["erfolg"],
            "misserfolg": p["misserfolg"],
            "spektakulaer": p["spektakulaer_erfolg"],
            "patzer": p["patzer"],
        }
        for key, (canvas, farbe, prozent) in self.balken.items():
            anteil = anteile[key]
            canvas.delete("all")
            breite = round(anteil * 248)
            if breite > 0:
                canvas.create_rectangle(0, 0, breite, 18, fill=farbe, width=0)
            prozent.config(text=f"{anteil * 100:5.1f} %")

        e_text = " / ".join(str(e) for e in eigenschaften)
        selbst = (
            f"Bei Eigenschaften {e_text} und Talentwert {taw:+d}:\n"
            f"Erfolgschance: {p['erfolg'] * 100:.2f} %   "
            f"Misserfolg: {p['misserfolg'] * 100:.2f} %\n"
            f"Ø übrige TaP* bei Erfolg: {p['durchschnitt_tap_bei_erfolg']:.2f}   "
            f"(spektakulärer Erfolg zählt als TaP* = 0)\n"
            f"Dreifache 20 (katastrophaler Patzer): {p['katastrophaler_patzer'] * 100:.3f} %"
        )
        self.details.config(text=selbst)


if __name__ == "__main__":
    Probenrechner().mainloop()
