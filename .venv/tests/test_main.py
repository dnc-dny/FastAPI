from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_item():
    response = client.get("/items/item_a")
    assert response.status_code == 200
    assert response.json() == {"name": "item_a", "price": 200}
