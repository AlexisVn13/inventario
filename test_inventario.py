import pytest
from inventario_logic import add_producto, update_producto, delete_producto

@pytest.fixture
def data():
    return {"productos": []}

def test_add_item(data):
    producto = {"nombre": "Test", "cantidad": 10}
    result = add_producto(data, producto)
    
    assert len(result["productos"]) == 1
    assert result["productos"][0]["nombre"] == "Test"

def test_update_item(data):
    add_producto(data, {"nombre": "Test", "cantidad": 10})
    
    update_producto(data, 0, 20)
    assert data["productos"][0]["cantidad"] == 20

def test_delete_item(data):
    add_producto(data, {"nombre": "Test", "cantidad": 10})
    
    delete_producto(data, 0)
    assert len(data["productos"]) == 0