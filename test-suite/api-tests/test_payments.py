import requests
import pytest

def test_happy_path_payment():
    url = "http://localhost:3000/payments"
    data = {"amount": 100, "currency": "EUR", "account_id": "acc_001"}
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["amount"] == 100
    assert response.json()["currency"] == "EUR"
    assert response.json()["account_id"] == "acc_001"
    assert response.json()["status"] == "success"

def test_amount_missing_payment():
    url = "http://localhost:3000/payments"
    data = {"currency": "EUR", "account_id": "acc_001"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid amount"

def test_amount_zero_payment():
    url = "http://localhost:3000/payments"
    data = {"amount": 0, "currency": "EUR", "account_id": "acc_001"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid amount"

def test_amount_negative_payment():
    url = "http://localhost:3000/payments"
    data = {"amount": -100, "currency": "EUR", "account_id": "acc_001"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid amount"

def test_currency_missing_payment():
    url = "http://localhost:3000/payments"
    data = {"amount": 100, "account_id": "acc_001"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Currency is required"

def test_account_not_found_payment():
    url = "http://localhost:3000/payments"
    data = {"amount": 100, "currency": "EUR", "account_id": "acc_999"}
    response = requests.post(url, json=data)
    assert response.status_code == 404
    assert "error" in response.json()
    assert response.json()["error"] == "Account not found"

def test_insufficient_funds_payment():
    url = "http://localhost:3000/payments"
    data = {"amount": 1000000, "currency": "EUR", "account_id": "acc_001"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Insufficient funds"