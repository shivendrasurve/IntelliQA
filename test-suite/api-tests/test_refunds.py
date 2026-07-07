import requests
import pytest

def test_refund_happy_path():
    payment_response = requests.post('http://localhost:3000/payments', json={'amount': 100, 'currency': 'EUR', 'account_id': 'acc_001'})
    assert payment_response.status_code == 201
    payment_id = payment_response.json()['id']
    refund_response = requests.post('http://localhost:3000/refunds', json={'payment_id': payment_id, 'amount': 50})
    assert refund_response.status_code == 201
    assert refund_response.json()['payment_id'] == payment_id
    assert refund_response.json()['amount'] == 50
    assert refund_response.json()['status'] == 'refunded'

def test_refund_payment_not_found():
    refund_response = requests.post('http://localhost:3000/refunds', json={'payment_id': 'pay_999', 'amount': 50})
    assert refund_response.status_code == 404
    assert refund_response.json()['error'] == 'Payment not found'

def test_refund_refund_exceeds_original_payment():
    payment_response = requests.post('http://localhost:3000/payments', json={'amount': 100, 'currency': 'EUR', 'account_id': 'acc_001'})
    assert payment_response.status_code == 201
    payment_id = payment_response.json()['id']
    refund_response = requests.post('http://localhost:3000/refunds', json={'payment_id': payment_id, 'amount': 200})
    assert refund_response.status_code == 400
    assert refund_response.json()['error'] == 'Refund exceeds original payment'

def test_refund_missing_payment_id():
    refund_response = requests.post('http://localhost:3000/refunds', json={'amount': 50})
    assert refund_response.status_code == 400

def test_refund_missing_amount():
    payment_response = requests.post('http://localhost:3000/payments', json={'amount': 100, 'currency': 'EUR', 'account_id': 'acc_001'})
    assert payment_response.status_code == 201
    payment_id = payment_response.json()['id']
    refund_response = requests.post('http://localhost:3000/refunds', json={'payment_id': payment_id})
    assert refund_response.status_code == 400

def test_refund_zero_amount():
    payment_response = requests.post('http://localhost:3000/payments', json={'amount': 100, 'currency': 'EUR', 'account_id': 'acc_001'})
    assert payment_response.status_code == 201
    payment_id = payment_response.json()['id']
    refund_response = requests.post('http://localhost:3000/refunds', json={'payment_id': payment_id, 'amount': 0})
    assert refund_response.status_code == 400

def test_refund_negative_amount():
    payment_response = requests.post('http://localhost:3000/payments', json={'amount': 100, 'currency': 'EUR', 'account_id': 'acc_001'})
    assert payment_response.status_code == 201
    payment_id = payment_response.json()['id']
    refund_response = requests.post('http://localhost:3000/refunds', json={'payment_id': payment_id, 'amount': -50})
    assert refund_response.status_code == 400