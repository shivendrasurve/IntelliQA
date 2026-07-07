import requests
import pytest

BASE = "http://localhost:3000"

def test_transfers_happy_path():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "to_account": "acc_002", "amount": 100})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_transfers_from_account_not_found():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_999", "to_account": "acc_002", "amount": 100})
    assert response.status_code == 404

def test_transfers_to_account_not_found():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "to_account": "acc_999", "amount": 100})
    assert response.status_code == 404

def test_transfers_insufficient_funds():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "to_account": "acc_002", "amount": 999999})
    assert response.status_code == 400
    assert response.json()["error"] == "Insufficient funds"

def test_transfers_invalid_amount():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "to_account": "acc_002", "amount": -100})
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid transfer amount"

def test_transfers_zero_amount():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "to_account": "acc_002", "amount": 0})
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid transfer amount"

def test_transfers_missing_from_account():
    response = requests.post(f"{BASE}/transfers",
        json={"to_account": "acc_002", "amount": 100})
    assert response.status_code == 400

def test_transfers_missing_to_account():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "amount": 100})
    assert response.status_code == 400

def test_transfers_missing_amount():
    response = requests.post(f"{BASE}/transfers",
        json={"from_account": "acc_001", "to_account": "acc_002"})
    assert response.status_code == 400
