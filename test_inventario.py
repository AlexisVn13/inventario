import pytest
from inventario_logic import (
    load_data, add_producto, update_producto,
    delete_producto, validate_user, add_user
)

# ─── FIXTURE ─────────────────────────────────────────────

@pytest.fixture
def data():
    return {
        "users": {
            "admin": {
                "password": "dummy",
                "role": "admin",
                "name": "Admin"
            }
        },
        "productos": []
    }

# ─── TESTS NORMALES ──────────────────────────────────────

def test_add_producto(data):
    producto = {"nombre": "Mouse", "cantidad": 5}
    add_producto(data, producto)

    assert len(data["productos"]) == 1
    assert data["productos"][0]["nombre"] == "Mouse"


def test_update_producto(data):
    producto = {"nombre": "Teclado", "cantidad": 3}
    add_producto(data, producto)

    update_producto(data, 0, 10)

    assert data["productos"][0]["cantidad"] == 10


def test_delete_producto(data):
    producto = {"nombre": "Monitor", "cantidad": 2}
    add_producto(data, producto)

    delete_producto(data, 0)

    assert len(data["productos"]) == 0


def test_validate_user_correcto(data):
    from inventario_logic import hash_password
    data["users"]["admin"]["password"] = hash_password("1234")

    assert validate_user(data, "admin", "1234") == True


def test_validate_user_incorrecto(data):
    assert validate_user(data, "admin", "wrong") == False


def test_add_user(data):
    add_user(data, "alex", "1234")

    assert "alex" in data["users"]
    
# ─── PARAMETRIZADAS ─────────────────────────────────────

@pytest.mark.parametrize("nombre,cantidad", [
    ("Laptop", 5),
    ("Mouse", 10),
    ("Teclado", 7)
])
def test_add_producto_parametrizado(data, nombre, cantidad):
    producto = {"nombre": nombre, "cantidad": cantidad}
    add_producto(data, producto)

    assert data["productos"][-1]["nombre"] == nombre
    assert data["productos"][-1]["cantidad"] == cantidad


@pytest.mark.parametrize("cantidad_inicial,nueva_cantidad", [
    (5, 10),
    (1, 0),
    (100, 50)
])
def test_update_producto_parametrizado(data, cantidad_inicial, nueva_cantidad):
    producto = {"nombre": "Test", "cantidad": cantidad_inicial}
    add_producto(data, producto)

    update_producto(data, 0, nueva_cantidad)

    assert data["productos"][0]["cantidad"] == nueva_cantidad


@pytest.mark.parametrize("username,password,esperado", [
    ("admin", "1234", True),
    ("admin", "wrong", False),
    ("no_user", "1234", False)
])
def test_validate_user_parametrizado(data, username, password, esperado):
    from inventario_logic import hash_password
    data["users"]["admin"]["password"] = hash_password("1234")

    assert validate_user(data, username, password) == esperado