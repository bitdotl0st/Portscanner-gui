# 🔍 GUI-Portscanner mit Multithreading & Service-Erkennung

Ein leistungsstarker, lokal laufender Portscanner mit moderner GUI, Multithreading und optionalem Speichern von Ergebnissen.

Ideal für dein **Cybersecurity-Portfolio** – kein externer Dienst nötig, nur Python!

---
![Vorschau](screenshot.png)

## 🧰 Features

- ✅ Eingabe von IP-Adresse oder Domain
- ✅ Portbereich (z. B. 1–1024) frei wählbar
- ✅ Multithreaded für schnellen Scan
- ✅ GUI mit `tkinter` + `ttk` (keine externe Abhängigkeit)
- ✅ Erkennt Standard-Services (z. B. Port 22 → SSH)
- ✅ Ergebnisse in Textdatei speicherbar
- ✅ Blockiert die GUI nicht (läuft asynchron)

---

## 🚀 Schnellstart

### 🔧 Voraussetzungen

- Python 3.10+  
- Keine externen Libraries nötig

### ▶️ Ausführen

```bash
python portscanner_gui.py
