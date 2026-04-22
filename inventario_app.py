import tkinter as tk
from tkinter import ttk, messagebox

from inventario_logic import (
    load_data, save_data,
    add_producto, update_producto, delete_producto,
    validate_user, add_user
)

# ─── Estilos ─────────────────────────────────────────────────────────

BG       = "#0F1117"
PANEL    = "#1A1D27"
CARD     = "#22263A"
ACCENT   = "#4F8EF7"
ACCENT2  = "#7B5EA7"
TEXT     = "#E8EAF0"
SUBTEXT  = "#7A7F99"
SUCCESS  = "#3DDC84"
DANGER   = "#F05C5C"
BORDER   = "#2E3249"

FONT_H   = ("Helvetica", 22, "bold")
FONT_S   = ("Helvetica", 11)

# ─── App ────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario Pro")
        self.geometry("900x600")
        self.configure(bg=BG)

        self.data = load_data()
        self.current_user = None

        self._show_login()

    # ─── Login ───────────────────────────────────────────────────────

    def _show_login(self):
        self._clear()

        frame = tk.Frame(self, bg=BG)
        frame.pack(expand=True)

        tk.Label(frame, text="Inventario Pro", font=FONT_H, bg=BG, fg=TEXT).pack(pady=20)

        self.user = tk.Entry(frame)
        self.user.pack(pady=5)

        self.password = tk.Entry(frame, show="*")
        self.password.pack(pady=5)

        tk.Button(frame, text="Login", bg=ACCENT, fg="white",
                  command=self._login).pack(pady=10)

    def _login(self):
        if validate_user(self.data, self.user.get(), self.password.get()):
            self.current_user = self.user.get()
            self._dashboard()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    # ─── Dashboard ───────────────────────────────────────────────────

    def _dashboard(self):
        self._clear()

        tk.Button(self, text="Agregar", command=self._add).pack()
        tk.Button(self, text="Eliminar", command=self._delete).pack()

        self.tree = ttk.Treeview(self, columns=("Nombre", "Cantidad"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.pack(fill="both", expand=True)

        self._refresh()

    def _refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for i, p in enumerate(self.data["productos"]):
            self.tree.insert("", "end", iid=i,
                             values=(p["nombre"], p["cantidad"]))

    # ─── CRUD UI ─────────────────────────────────────────────────────

    def _add(self):
        win = tk.Toplevel(self)
        win.title("Agregar")

        name = tk.Entry(win)
        name.pack()

        qty = tk.Entry(win)
        qty.pack()

        def save():
            producto = {
                "nombre": name.get(),
                "cantidad": int(qty.get()),
                "precio": 0,
                "categoria": "",
                "descripcion": ""
            }
            add_producto(self.data, producto)
            self._refresh()
            win.destroy()

        tk.Button(win, text="Guardar", command=save).pack()

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            return

        delete_producto(self.data, int(sel[0]))
        self._refresh()

    # ─── Helpers ─────────────────────────────────────────────────────

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


# ─── Run ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()