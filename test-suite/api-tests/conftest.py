import pytest
import requests

BASE = "http://localhost:3000"

@pytest.fixture
def valid_payment():
    """
    Creates a fresh payment before each test that needs one.
    Prevents cascading failures when payment endpoint changes.
    Each test gets its own isolated payment ID.
    """
    response = requests.post(f"{BASE}/payments",
        json={"amount": 100, "currency": "EUR", "account_id": "acc_001"})
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def valid_payment_id(valid_payment):
    """Returns just the payment ID string."""
    return valid_payment["id"]
