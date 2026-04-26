import tkinter as tk
import subprocess
import datetime
import time

def draw_banner():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    text.insert("end", "╔════════════════════════════════╗\n")
    text.insert("end", "║     MERIDIAN WORKSPACE v1.2    ║\n")
    text.insert("end", "╚════════════════════════════════╝\n")
    text.insert("end", f"  Date: {date_str}  |  Time: {time_str}\n")
    text.insert("end", " ──────────────────────────────────\n")
    text.insert("end", "Type 'help' for commands.\n\n")

current_color = {"value": "#00ff88"}

def enter_command(event=None):
    cmd = entry.get()

    text.config(state="normal")
    start_index = text.index("end-1c")
    text.insert("end", f"> {cmd}\n")

    if cmd == "help":
        text.insert("end",
            "  Commands:\n"
            "    help       — show this menu\n"
            "    clear      — clear the screen\n"
            "    time       — show current time\n"
            "    date       — show current date\n"
            "    canvas     — open drawing canvas(hold left mouse button for draw right for erasing)\n"
            "    exit       — quit\n"
            "    blue       — set text color to blue\n"
            "    green      — set text color to green\n"
        )
    elif cmd == "exit":
        root.quit()

    elif cmd == "calendar":
         def open_notepad():
            NOTEPAD_FILE = "meridian_notes.txt"

    win = tk.Toplevel()
    win.title("Meridian Notepad")
    win.configure(bg="#0d0d0d")
    win.geometry("600x400")

    tk.Label(win, text="MERIDIAN NOTEPAD", bg="#0d0d0d",
             fg=current_color["value"], font=("Consolas", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 4))

    notepad = tk.Text(win, bg="#111111", fg=current_color["value"],
                      font=("Consolas", 11), insertbackground=current_color["value"],
                      bd=0, padx=10, pady=10)
    notepad.pack(fill="both", expand=True, padx=14, pady=(0, 6))

    if os.path.exists(NOTEPAD_FILE):
        with open(NOTEPAD_FILE, "r") as f:
            notepad.insert("1.0", f.read())

    def save():
        with open(NOTEPAD_FILE, "w") as f:
            f.write(notepad.get("1.0", "end-1c"))

    tk.Button(win, text="SAVE", command=save, bg="#1a1a1a", fg=current_color["value"],
              font=("Consolas", 10), bd=0, padx=12, pady=6,
              activebackground="#2a2a2a", cursor="hand2").pack(pady=(0, 10))

    win.bind("<Control-s>", lambda e: save())
    win.protocol("WM_DELETE_WINDOW", lambda: (save(), win.destroy()))
 

    if cmd == "time":
        text.insert("end", f"{time.ctime()}\n")

    elif cmd == "date":
        text.insert("end", f"{datetime.date.today()}\n")

    elif cmd == "clear":
        text.delete("1.0", "end")
        draw_banner()
    elif cmd == "blue":
        current_color["value"] = "#14bcbf"
        text.config(fg="#14bcbf")
        entry.config(fg="#14bcbf", insertbackground="#14bcbf")
        entry_label.config(fg="#14bcbf")

    elif cmd == "green":
        current_color["value"] = "#00f888"
        text.config(fg="#00f888")
        entry.config(fg="#00f888", insertbackground="#00f888")
        entry_label.config(fg="#00f888")

    elif cmd == "canvas":
        window = tk.Toplevel()
        window.geometry("600x400")
        window.title("Canvas")

        canvas = tk.Canvas(window, bg="white")
        canvas.pack(fill="both", expand=1)

        lasx = lasy = 0

        def get_x_and_y(event):
            nonlocal lasx, lasy
            lasx, lasy = event.x, event.y

        def draw(event):
            nonlocal lasx, lasy
            canvas.create_line(lasx, lasy, event.x, event.y, fill="black", width=2)
            lasx, lasy = event.x, event.y

        def erase(event):
            nonlocal lasx, lasy
            canvas.create_line(lasx, lasy, event.x, event.y, fill="white", width=2)
            lasx, lasy = event.x, event.y

        canvas.bind("<Button-1>", get_x_and_y)
        canvas.bind("<B1-Motion>", draw)
        canvas.bind("<Button-3>", get_x_and_y)
        canvas.bind("<B3-Motion>", erase)

    else:
        text.delete(start_index, "end")
        text.insert("end", f"Unknown command: '{cmd}'\n")

    text.config(state="disabled")
    text.see("end")
    entry.delete(0, "end")


root = tk.Tk()
root.title("Meridian Workspace")
root.configure(bg="#000000")

text = tk.Text(
    root,
    bg="black",
    fg="#00f888",
    font=("Consolas", 13),
    state="disabled"
)
text.pack(fill="both", expand=True)
entry_frame = tk.Frame(root, bg="#000000")
entry_frame.pack(fill="x", side="bottom", padx=10, pady=6)

entry_label = tk.Label(
    entry_frame,text="> ", bg="#0d0d0d", fg="#00f888",
    font=("Consolas", 12), padx=6
)
entry_label.pack(side="left")
entry = tk.Entry(
    entry_frame,
    bg="black",
    fg="#00f888",
    insertbackground="#00f888",
    highlightcolor="#00f888",
    highlightthickness=0,
    bd=0,
)
entry.pack(side="left", fill="x", expand=True)
entry.bind("<Return>", enter_command)
entry_frame.bind("<Button-1>", lambda e: entry.focus_set())

text.config(state="normal")
draw_banner()
text.config(state="disabled")

root.mainloop()