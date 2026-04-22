import json
import os
import hashlib
from datetime import datetime

DATA_FILE = "inventario_data.json"

# ─── Utilidades ──────────────────────────────────────────────────────────────

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ─── Carga y guardado de datos ───────────────────────────────────────────────

def load_data():
    # Si ya existe, lo carga
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # 🔥 Si NO existe, lo crea automáticamente
    data = {
        "users": {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin",
                "name": "Administrador"
            }
        },
        "productos": []
    }

    save_data(data)
    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── CRUD de productos ───────────────────────────────────────────────────────

def add_producto(data, producto):
    producto["id"] = len(data["productos"]) + 1
    producto["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["productos"].append(producto)
    save_data(data)
    return data

def update_producto(data, index, nueva_cantidad):
    if index < 0 or index >= len(data["productos"]):
        raise IndexError("Producto no encontrado")

    data["productos"][index]["cantidad"] = nueva_cantidad
    data["productos"][index]["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_data(data)
    return data

def delete_producto(data, index):
    if index < 0 or index >= len(data["productos"]):
        raise IndexError("Producto no encontrado")

    data["productos"].pop(index)
    save_data(data)
    return data

# ─── CRUD de usuarios ────────────────────────────────────────────────────────

def add_user(data, username, password, role="empleado", name=None):
    if username in data["users"]:
        raise ValueError("El usuario ya existe")

    data["users"][username] = {
        "password": hash_password(password),
        "role": role,
        "name": name or username
    }

    save_data(data)
    return data

def validate_user(data, username, password):
    users = data.get("users", {})
    if username in users:
        return users[username]["password"] == hash_password(password)
    return False