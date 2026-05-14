from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_read() -> None:
    """Перевіряє створення елемента та його отримання за ідентифікатором"""

    data = {"title": "Test", "price": 1.23, "owner_id": 1}
    resp = client.post("/items/", json=data)

    assert resp.status_code == 201

    item = resp.json()

    assert item["title"] == "Test"
    assert item["price"] == 1.23
    assert item["owner_id"] == 1

    get_resp = client.get(f"/items/{item['id']}")

    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == item["id"]


def test_filter_by_owner_id() -> None:
    """Перевіряє фільтрацію елементів за ідентифікатором власника"""

    client.post("/items/", json={"title": "Owner 1 Item", "price": 10, "owner_id": 1})
    client.post("/items/", json={"title": "Owner 2 Item", "price": 20, "owner_id": 2})

    resp = client.get("/items/?owner_id=1")

    assert resp.status_code == 200

    items = resp.json()

    assert len(items) >= 1
    assert all(item["owner_id"] == 1 for item in items)


def test_owner_can_update_item() -> None:
    """Перевіряє, що власник може оновити свій елемент"""

    create_resp = client.post("/items/", json={"title": "Old title", "price": 10, "owner_id": 1})
    item = create_resp.json()

    update_resp = client.put(
        f"/items/{item['id']}?owner_id=1",
        json={"title": "New title"}
    )

    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New title"


def test_not_owner_cannot_update_item() -> None:
    """Перевіряє, що не власник не може оновити чужий елемент"""

    create_resp = client.post("/items/", json={"title": "Private item", "price": 10, "owner_id": 1})
    item = create_resp.json()

    update_resp = client.put(
        f"/items/{item['id']}?owner_id=2",
        json={"title": "Hacked title"}
    )

    assert update_resp.status_code == 403
    assert update_resp.json()["detail"] == "Only owner can update this item"


def test_owner_can_delete_item() -> None:
    """Перевіряє, що власник може видалити свій елемент"""

    create_resp = client.post("/items/", json={"title": "Delete me", "price": 10, "owner_id": 1})
    item = create_resp.json()

    delete_resp = client.delete(f"/items/{item['id']}?owner_id=1")

    assert delete_resp.status_code == 204

    get_resp = client.get(f"/items/{item['id']}")

    assert get_resp.status_code == 404


def test_not_owner_cannot_delete_item() -> None:
    """Перевіряє, що не власник не може видалити чужий елемент"""

    create_resp = client.post("/items/", json={"title": "Do not delete", "price": 10, "owner_id": 1})
    item = create_resp.json()

    delete_resp = client.delete(f"/items/{item['id']}?owner_id=2")

    assert delete_resp.status_code == 403
    assert delete_resp.json()["detail"] == "Only owner can delete this item"


def test_pagination() -> None:
    """Перевіряє обмеження кількості елементів у відповіді"""

    for index in range(5):
        client.post(
            "/items/",
            json={"title": f"Pagination Item {index}", "price": index, "owner_id": 1}
        )

    resp = client.get("/items/?skip=0&limit=2")

    assert resp.status_code == 200
    assert len(resp.json()) <= 2


def test_search_by_title() -> None:
    """Перевіряє пошук елементів за назвою"""

    client.post("/items/", json={"title": "Unique Phone", "price": 500, "owner_id": 1})
    client.post("/items/", json={"title": "Laptop", "price": 1000, "owner_id": 1})

    resp = client.get("/items/?search=Phone")

    assert resp.status_code == 200

    items = resp.json()

    assert len(items) >= 1
    assert all("Phone" in item["title"] for item in items)


def test_sort_by_price_desc() -> None:
    """Перевіряє сортування елементів за ціною у спадному порядку"""

    client.post("/items/", json={"title": "Cheap item", "price": 10, "owner_id": 1})
    client.post("/items/", json={"title": "Expensive item", "price": 100, "owner_id": 1})

    resp = client.get("/items/?sort_by=price&sort_order=desc")

    assert resp.status_code == 200

    items = resp.json()

    prices = [item["price"] for item in items]

    assert prices == sorted(prices, reverse=True)
