import pytest

def user_payload(uid=1, name="Paul", email="pl@atu.ie", age=25, sid="S1234567"):
    return {"user_id": uid, "name": name, "email": email, "age": age, "student_id":sid}

def test_create_user_ok(client):
    r = client.post("/api/users", json=user_payload())
    assert r.status_code == 201
    data = r.json()
    assert data["user_id"] == 1
    assert data["name"] == "Paul"

def test_duplicate_user_id_conflict(client):
    client.post("/api/users", json=user_payload(uid=2))
    r = client.post("/api/users", json=user_payload(uid=2))
    assert r.status_code == 409 # duplicate id -> conflict
    assert "exists" in r.json()["detail"].lower()

@pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"])
def test_bad_student_id_422(client, bad_sid):
    r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid))
    assert r.status_code == 422 # pydantic validation error

def test_get_user_404(client):
    r = client.get("/api/users/999")
    assert r.status_code == 404

def test_put_user_404(client):
    r = client.put("/api/users/999", json=user_payload(name="John"))
    assert r.status_code == 404

def test_put_user_ok(client):
    r = client.put("/api/users/1", json=user_payload(name="Nasir"))
    assert r.status_code == 200

@pytest.mark.parametrize("invalid_age",[1,2,3,4,5])
def test_invalid_age(client,invalid_age):
    r = client.post("/api/users",json=user_payload(uid=4,age=invalid_age))
    assert r.status_code == 422
    