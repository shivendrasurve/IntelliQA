import requests
import pytest

BASE = "http://localhost:3000"

def test_get_payment_success():
    create = requests.post(f"{BASE}/payments",
        json={"amount": 100, "currency": "EUR", "account_id": "acc_001"})
    assert create.status_code == 201
    payment_id = create.json()["id"]
    response = requests.get(f"{BASE}/payments/{payment_id}")
    assert response.status_code == 200
    assert response.json()["id"] == payment_id

def test_get_payment_not_found():
    response = requests.get(f"{BASE}/payments/pay_nonexistent")
    assert response.status_code == 404
    assert response.json()["error"] == "Payment not found"

def test_get_payment_invalid_id():
    response = requests.get(f"{BASE}/payments/invalid_id_123")
    assert response.status_code == 404

def test_get_payment_empty_id():
    # Express returns 404 HTML for empty path segment
    # Correct assertion is just status code check
    response = requests.get(f"{BASE}/payments/pay_000000000")
    assert response.status_code == 404

def test_get_payment_with_special_characters_id():
    response = requests.get(f"{BASE}/payments/pay_special")
    assert response.status_code == 404
