import pytest
from main import app

def test_extract_expiry():
    print("Testing expiry OCR extraction...")
    # This is a placeholder; real OCR test would require an image file
    from ocr.expiry_ocr import extract_expiry
    assert extract_expiry("image_data") == "2025-12-31"

def test_api_product_crud():
    client = app.test_client()
    # Login first
    resp = client.post('/login', json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    # Create product
    resp = client.post('/api/products', json={"name": "TestProduct", "expiry": "2030-01-01"})
    assert resp.status_code == 201
    prod = resp.get_json()
    pid = prod["id"]
    # Update product
    resp = client.put(f'/api/products/{pid}', json={"name": "TestProduct2", "expiry": "2030-12-31"})
    assert resp.status_code == 200
    # Delete product
    resp = client.delete(f'/api/products/{pid}')
    assert resp.status_code == 204
    # Logout
    client.post('/logout')
