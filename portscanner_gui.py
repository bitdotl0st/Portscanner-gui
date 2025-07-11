import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from queue import Queue
from datetime import datetime

# ------------------ Globale Objekte ------------------
port_queue = Queue()
scan_resultate = []
ziel_host = ""

# ------------------ Worker-Thread ------------------
def scan_worker():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ziel_host, port)) == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "Unbekannt"
                    msg = f"✅ Port {port} offen ({service})"
                    ausgabe_box.insert(tk.END, msg)
                    scan_resultate.append(msg)
        finally:
            port_queue.task_done()

# ------------------ Scan starten (in Extra-Thread) ------------------
def start_scan_threaded():
    threading.Thread(target=start_scan, daemon=True).start()

def start_scan():
    global ziel_host, scan_resultate
    ausgabe_box.delete(0, tk.END)
    scan_resultate = []

    # -------- Eingaben prüfen --------
    ziel_host = eingabe_host.get().strip()
    try:
        socket.gethostbyname(ziel_host)
    except OSError:
        messagebox.showerror("Fehler", "Ungültiger Hostname oder IP-Adresse.")
        return

    try:
        port_von = int(eingabe_von.get())
        port_bis = int(eingabe_bis.get())
    except ValueError:
        messagebox.showerror("Fehler", "Portbereiche müssen Zahlen sein.")
        return

    if not (1 <= port_von <= port_bis <= 65535):
        messagebox.showerror("Fehler", "Portbereich ungültig.")
        return

    # -------- Scan vorbereiten --------
    start_time = datetime.now()
    ausgabe_box.insert(tk.END, f"⏱️ Scan gestartet {start_time.strftime('%H:%M:%S')}")
    ausgabe_box.insert(tk.END, "--------------------------------------------")

    for port in range(port_von, port_bis + 1):
        port_queue.put(port)

    # -------- Threads anwerfen --------
    for _ in range(100):          # 100 gleichzeitige Verbindungen
        threading.Thread(target=scan_worker, daemon=True).start()

    port_queue.join()             # warten bis alles abgearbeitet
    dauer = (datetime.now() - start_time).total_seconds()
    ausgabe_box.insert(tk.END, "--------------------------------------------")
    ausgabe_box.insert(tk.END, f"✅ Scan fertig in {dauer:.2f}s")

# ------------------ Ergebnisse speichern ------------------
def speichern():
    if not scan_resultate:
        messagebox.showinfo("Hinweis", "Keine Scan-Ergebnisse vorhanden.")
        return
    datei = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Textdateien", "*.txt")],
        title="Scan-Ergebnisse speichern"
    )
    if datei:
        with open(datei, "w", encoding="utf-8") as f:
            f.write(f"Scan von {ziel_host}\n")
            f.write("\n".join(scan_resultate))
        messagebox.showinfo("Gespeichert", "Ergebnisse gespeichert.")

# ------------------ GUI-Aufbau ------------------
root = tk.Tk()
root.title("🔍 Portscanner GUI")
root.geometry("620x520")
root.resizable(False, False)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

# Ziel-Eingabe
ttk.Label(frame, text="Ziel (IP / Domain):").grid(row=0, column=0, sticky="w")
eingabe_host = ttk.Entry(frame, width=42)
eingabe_host.grid(row=0, column=1, padx=5, pady=5)

# Portbereich
ttk.Label(frame, text="Ports von:").grid(row=1, column=0, sticky="w")
eingabe_von = ttk.Entry(frame, width=8)
eingabe_von.insert(0, "1")
eingabe_von.grid(row=1, column=1, sticky="w")

ttk.Label(frame, text="bis:").grid(row=1, column=1, padx=80, sticky="w")
eingabe_bis = ttk.Entry(frame, width=8)
eingabe_bis.insert(0, "1024")
eingabe_bis.grid(row=1, column=1, padx=(120,0), sticky="w")

# Buttons
ttk.Button(frame, text="🔍 Scan starten", command=start_scan_threaded)\
    .grid(row=2, column=1, sticky="e", pady=10)
ttk.Button(frame, text="💾 Ergebnisse speichern", command=speichern)\
    .grid(row=2, column=0, sticky="w", pady=10)

# Ausgabefeld
ausgabe_box = tk.Listbox(root, font=("Courier New", 10), height=20)
ausgabe_box.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
