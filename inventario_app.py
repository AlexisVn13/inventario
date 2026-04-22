import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
from datetime import datetime

# ─── Configuración de datos ───────────────────────────────────────────────────

DATA_FILE = "inventario_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "users": {
            "admin": {
                "password": hashlib.sha256("admin123".encode()).hexdigest(),
                "role": "admin",
                "name": "Administrador"
            }
        },
        "productos": []
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ─── Paleta y estilos ─────────────────────────────────────────────────────────

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
FONT_M   = ("Helvetica", 13)
FONT_S   = ("Helvetica", 11)
FONT_XS  = ("Helvetica", 9)

# ─── Aplicación principal ─────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario Pro")
        self.geometry("420x560")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.data = load_data()
        self.current_user = None

        # Centrar ventana
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 420) // 2
        y = (self.winfo_screenheight() - 560) // 2
        self.geometry(f"420x560+{x}+{y}")

        self._show_login()

    # ── Login ──────────────────────────────────────────────────────────────────

    def _show_login(self):
        self._clear()
        self.geometry("420x560")
        self.resizable(False, False)

        # Fondo decorativo superior
        canvas = tk.Canvas(self, width=420, height=140, bg=BG, highlightthickness=0)
        canvas.place(x=0, y=0)
        canvas.create_rectangle(0, 0, 420, 120, fill=PANEL, outline="")
        canvas.create_rectangle(0, 118, 420, 122, fill=ACCENT, outline="")
        canvas.create_text(210, 55, text="📦", font=("Helvetica", 38), fill=ACCENT)
        canvas.create_text(210, 100, text="Inventario Pro", font=FONT_H, fill=TEXT)

        frame = tk.Frame(self, bg=BG)
        frame.place(x=40, y=155, width=340)

        tk.Label(frame, text="Bienvenido de vuelta", font=("Helvetica", 14, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(frame, text="Inicia sesión para continuar", font=FONT_XS,
                 bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(0, 20))

        # Usuario
        tk.Label(frame, text="Usuario", font=FONT_S, bg=BG, fg=SUBTEXT).pack(anchor="w")
        self.entry_user = self._entry(frame)
        self.entry_user.pack(fill="x", pady=(2, 12))

        # Contraseña
        tk.Label(frame, text="Contraseña", font=FONT_S, bg=BG, fg=SUBTEXT).pack(anchor="w")
        self.entry_pass = self._entry(frame, show="●")
        self.entry_pass.pack(fill="x", pady=(2, 24))

        # Botón login
        btn = tk.Button(frame, text="Iniciar sesión", font=("Helvetica", 12, "bold"),
                        bg=ACCENT, fg="white", activebackground="#3A7DE0",
                        activeforeground="white", relief="flat", cursor="hand2",
                        height=2, command=self._do_login)
        btn.pack(fill="x")

        # Info credenciales demo
        tk.Label(frame, text="Demo: admin / admin123", font=FONT_XS,
                 bg=BG, fg=SUBTEXT).pack(pady=(16, 0))

        self.entry_user.focus()
        self.bind("<Return>", lambda e: self._do_login())

    def _do_login(self):
        user = self.entry_user.get().strip()
        pw   = self.entry_pass.get()
        users = self.data.get("users", {})
        if user in users and users[user]["password"] == hash_password(pw):
            self.current_user = {"username": user, **users[user]}
            self._show_dashboard()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    # ── Dashboard ──────────────────────────────────────────────────────────────

    def _show_dashboard(self):
        self._clear()
        self.geometry("900x620")
        self.resizable(True, True)
        x = (self.winfo_screenwidth() - 900) // 2
        y = (self.winfo_screenheight() - 620) // 2
        self.geometry(f"900x620+{x}+{y}")

        # ── Sidebar
        sidebar = tk.Frame(self, bg=PANEL, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="📦", font=("Helvetica", 28), bg=PANEL, fg=ACCENT).pack(pady=(24, 0))
        tk.Label(sidebar, text="Inventario", font=("Helvetica", 13, "bold"),
                 bg=PANEL, fg=TEXT).pack()
        tk.Label(sidebar, text="Pro", font=("Helvetica", 10),
                 bg=PANEL, fg=ACCENT).pack(pady=(0, 24))

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=8)

        name = self.current_user.get("name", self.current_user["username"])
        role = self.current_user.get("role", "usuario")
        tk.Label(sidebar, text=f"👤 {name}", font=FONT_S, bg=PANEL, fg=TEXT).pack(padx=16, anchor="w")
        tk.Label(sidebar, text=role.capitalize(), font=FONT_XS, bg=PANEL, fg=SUBTEXT).pack(padx=16, anchor="w")

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=16)

        # Menú lateral
        self._nav_btn(sidebar, "📋  Inventario", self._tab_inventario)
        self._nav_btn(sidebar, "➕  Agregar producto", self._tab_agregar)
        if self.current_user.get("role") == "admin":
            self._nav_btn(sidebar, "👥  Usuarios", self._tab_usuarios)

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=16, side="bottom")
        tk.Button(sidebar, text="🚪  Cerrar sesión", font=FONT_S,
                  bg=PANEL, fg=DANGER, relief="flat", cursor="hand2",
                  activebackground=PANEL, activeforeground=DANGER,
                  command=self._logout).pack(side="bottom", padx=16, pady=16, anchor="w")

        # ── Área principal
        self.main_area = tk.Frame(self, bg=BG)
        self.main_area.pack(side="right", fill="both", expand=True)

        self._tab_inventario()

    def _nav_btn(self, parent, text, cmd):
        btn = tk.Button(parent, text=text, font=FONT_S, bg=PANEL, fg=TEXT,
                        relief="flat", anchor="w", padx=20, cursor="hand2",
                        activebackground=CARD, activeforeground=ACCENT,
                        command=cmd)
        btn.pack(fill="x", pady=2)

    # ── Tab: Inventario ────────────────────────────────────────────────────────

    def _tab_inventario(self):
        self._clear_main()
        frame = self.main_area

        # Header
        hdr = tk.Frame(frame, bg=BG)
        hdr.pack(fill="x", padx=24, pady=(20, 0))
        tk.Label(hdr, text="Inventario", font=FONT_H, bg=BG, fg=TEXT).pack(side="left")

        # Buscador
        search_frame = tk.Frame(frame, bg=CARD, highlightbackground=BORDER,
                                highlightthickness=1)
        search_frame.pack(fill="x", padx=24, pady=12)
        tk.Label(search_frame, text="🔍", bg=CARD, fg=SUBTEXT, font=FONT_M).pack(side="left", padx=8)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *a: self._refresh_table())
        tk.Entry(search_frame, textvariable=self.search_var, bg=CARD, fg=TEXT,
                 insertbackground=TEXT, relief="flat", font=FONT_S,
                 highlightthickness=0).pack(side="left", fill="x", expand=True, pady=8)

        # Tabla
        cols = ("ID", "Nombre", "Categoría", "Cantidad", "Precio", "Actualizado")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=32,
                        font=FONT_S, borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                        background=PANEL, foreground=ACCENT,
                        font=("Helvetica", 10, "bold"), relief="flat")
        style.map("Custom.Treeview", background=[("selected", ACCENT2)])

        tree_frame = tk.Frame(frame, bg=BG)
        tree_frame.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings",
                                 style="Custom.Treeview")
        widths = [50, 180, 120, 80, 90, 140]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Botones de acción
        btn_frame = tk.Frame(frame, bg=BG)
        btn_frame.pack(fill="x", padx=24, pady=(0, 16))
        tk.Button(btn_frame, text="✏️  Editar", font=FONT_S, bg=ACCENT,
                  fg="white", relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._editar_producto).pack(side="left", padx=(0, 8))
        tk.Button(btn_frame, text="🗑️  Eliminar", font=FONT_S, bg=DANGER,
                  fg="white", relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._eliminar_producto).pack(side="left")

        self._refresh_table()

    def _refresh_table(self):
        query = self.search_var.get().lower() if hasattr(self, "search_var") else ""
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, p in enumerate(self.data["productos"]):
            if query and query not in p["nombre"].lower() and query not in p.get("categoria", "").lower():
                continue
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", iid=str(i), values=(
                p.get("id", i+1),
                p["nombre"],
                p.get("categoria", "-"),
                p["cantidad"],
                f"${p['precio']:.2f}",
                p.get("fecha", "-")
            ), tags=(tag,))
        self.tree.tag_configure("even", background=CARD)
        self.tree.tag_configure("odd", background="#1E2235")

    def _editar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Aviso", "Selecciona un producto para editar.")
            return
        idx = int(sel[0])
        prod = self.data["productos"][idx]
        self._form_producto(edit_idx=idx, data=prod)

    def _eliminar_producto(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Aviso", "Selecciona un producto para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            idx = int(sel[0])
            self.data["productos"].pop(idx)
            save_data(self.data)
            self._refresh_table()

    # ── Tab: Agregar producto ──────────────────────────────────────────────────

    def _tab_agregar(self):
        self._clear_main()
        self._form_producto()

    def _form_producto(self, edit_idx=None, data=None):
        self._clear_main()
        frame = self.main_area
        title = "Editar producto" if edit_idx is not None else "Agregar producto"
        tk.Label(frame, text=title, font=FONT_H, bg=BG, fg=TEXT).pack(padx=24, pady=(20, 16), anchor="w")

        card = tk.Frame(frame, bg=CARD, padx=24, pady=24)
        card.pack(fill="x", padx=24)

        fields = [
            ("Nombre del producto", "nombre"),
            ("Categoría", "categoria"),
            ("Cantidad", "cantidad"),
            ("Precio (MXN)", "precio"),
            ("Descripción", "descripcion"),
        ]

        entries = {}
        for label, key in fields:
            tk.Label(card, text=label, font=FONT_S, bg=CARD, fg=SUBTEXT).pack(anchor="w")
            e = self._entry(card)
            e.pack(fill="x", pady=(2, 12))
            if data:
                e.insert(0, str(data.get(key, "")))
            entries[key] = e

        def guardar():
            nombre = entries["nombre"].get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio.")
                return
            try:
                cantidad = int(entries["cantidad"].get())
                precio   = float(entries["precio"].get())
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser entero y precio decimal.")
                return

            prod = {
                "id": (edit_idx + 1) if edit_idx is not None else len(self.data["productos"]) + 1,
                "nombre":      nombre,
                "categoria":   entries["categoria"].get().strip(),
                "cantidad":    cantidad,
                "precio":      precio,
                "descripcion": entries["descripcion"].get().strip(),
                "fecha":       datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
            if edit_idx is not None:
                self.data["productos"][edit_idx] = prod
            else:
                self.data["productos"].append(prod)
            save_data(self.data)
            messagebox.showinfo("Éxito", "Producto guardado correctamente.")
            self._tab_inventario()

        tk.Button(card, text="💾  Guardar", font=("Helvetica", 12, "bold"),
                  bg=SUCCESS, fg="white", relief="flat", cursor="hand2",
                  padx=16, pady=8, command=guardar).pack(anchor="w")

    # ── Tab: Usuarios (admin) ──────────────────────────────────────────────────

    def _tab_usuarios(self):
        self._clear_main()
        frame = self.main_area
        tk.Label(frame, text="Gestión de usuarios", font=FONT_H, bg=BG, fg=TEXT).pack(
            padx=24, pady=(20, 16), anchor="w")

        # Lista
        card = tk.Frame(frame, bg=CARD, padx=24, pady=16)
        card.pack(fill="x", padx=24, pady=(0, 16))

        cols = ("Usuario", "Nombre", "Rol")
        style = ttk.Style()
        style.configure("U.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, rowheight=30, font=FONT_S, borderwidth=0)
        style.configure("U.Treeview.Heading", background=PANEL, foreground=ACCENT,
                        font=("Helvetica", 10, "bold"), relief="flat")

        self.user_tree = ttk.Treeview(card, columns=cols, show="headings",
                                      style="U.Treeview", height=8)
        for col in cols:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=160, anchor="center")
        self.user_tree.pack(fill="x")

        self._refresh_users()

        # Formulario nuevo usuario
        tk.Label(frame, text="Agregar usuario", font=("Helvetica", 13, "bold"),
                 bg=BG, fg=TEXT).pack(padx=24, anchor="w")

        form = tk.Frame(frame, bg=CARD, padx=24, pady=16)
        form.pack(fill="x", padx=24, pady=8)

        tk.Label(form, text="Usuario", font=FONT_S, bg=CARD, fg=SUBTEXT).grid(row=0, column=0, sticky="w")
        self.nu_user = self._entry(form)
        self.nu_user.grid(row=1, column=0, padx=(0, 12), pady=(2, 8), sticky="ew")

        tk.Label(form, text="Nombre", font=FONT_S, bg=CARD, fg=SUBTEXT).grid(row=0, column=1, sticky="w")
        self.nu_name = self._entry(form)
        self.nu_name.grid(row=1, column=1, padx=(0, 12), pady=(2, 8), sticky="ew")

        tk.Label(form, text="Contraseña", font=FONT_S, bg=CARD, fg=SUBTEXT).grid(row=0, column=2, sticky="w")
        self.nu_pass = self._entry(form, show="●")
        self.nu_pass.grid(row=1, column=2, padx=(0, 12), pady=(2, 8), sticky="ew")

        tk.Label(form, text="Rol", font=FONT_S, bg=CARD, fg=SUBTEXT).grid(row=0, column=3, sticky="w")
        self.nu_role = ttk.Combobox(form, values=["admin", "empleado"],
                                    state="readonly", width=10)
        self.nu_role.set("empleado")
        self.nu_role.grid(row=1, column=3, pady=(2, 8), sticky="ew")

        form.columnconfigure((0, 1, 2), weight=1)

        tk.Button(form, text="➕ Agregar usuario", font=FONT_S, bg=ACCENT,
                  fg="white", relief="flat", cursor="hand2", padx=12, pady=6,
                  command=self._agregar_usuario).grid(row=2, column=0, columnspan=4, sticky="w")

    def _refresh_users(self):
        for row in self.user_tree.get_children():
            self.user_tree.delete(row)
        for uname, info in self.data["users"].items():
            self.user_tree.insert("", "end", values=(uname, info.get("name", "-"), info.get("role", "-")))

    def _agregar_usuario(self):
        uname = self.nu_user.get().strip()
        name  = self.nu_name.get().strip()
        pw    = self.nu_pass.get()
        role  = self.nu_role.get()
        if not uname or not pw:
            messagebox.showerror("Error", "Usuario y contraseña son obligatorios.")
            return
        if uname in self.data["users"]:
            messagebox.showerror("Error", "Ese usuario ya existe.")
            return
        self.data["users"][uname] = {
            "password": hash_password(pw),
            "role": role,
            "name": name or uname
        }
        save_data(self.data)
        messagebox.showinfo("Éxito", "Usuario creado.")
        self._tab_usuarios()

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _entry(self, parent, show=None):
        e = tk.Entry(parent, bg=CARD, fg=TEXT, insertbackground=TEXT,
                     relief="flat", font=FONT_S, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT)
        if show:
            e.configure(show=show)
        return e

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _clear_main(self):
        for w in self.main_area.winfo_children():
            w.destroy()

    def _logout(self):
        self.current_user = None
        self.geometry("420x560")
        self.resizable(False, False)
        self._show_login()


# ─── Punto de entrada ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
