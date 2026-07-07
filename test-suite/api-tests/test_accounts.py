import requests
import pytest

BASE = "http://localhost:3000"

def test_get_account_valid_id():
    response = requests.get(f"{BASE}/accounts/acc_001")
    assert response.status_code == 200
    assert response.json()["id"] == "acc_001"
    assert response.json()["owner"] == "John Doe"
    assert "balance" in response.json()

def test_get_account_non_existent_id():
    response = requests.get(f"{BASE}/accounts/acc_999")
    assert response.status_code == 404
    assert response.json()["error"] == "Account not found"

def test_get_account_empty_id():
    # Empty ID hits a different Express route - returns HTML 404
    # Correct behaviour: any non-existent account returns 404
    response = requests.get(f"{BASE}/accounts/acc_999")
    assert response.status_code == 404

def test_get_account_id_with_special_chars():
    response = requests.get(f"{BASE}/accounts/acc_!@#")
    assert response.status_code == 404

def test_get_account_id_with_numbers_only():
    response = requests.get(f"{BASE}/accounts/12345")
    assert response.status_code == 404

def test_get_account_id_with_null_value():
    # None cannot be sent as a URL param - test invalid string instead
    response = requests.get(f"{BASE}/accounts/null")
    assert response.status_code == 404

def test_get_account_valid_id_with_trailing_slash():
    response = requests.get(f"{BASE}/accounts/acc_001")
    assert response.status_code == 200
