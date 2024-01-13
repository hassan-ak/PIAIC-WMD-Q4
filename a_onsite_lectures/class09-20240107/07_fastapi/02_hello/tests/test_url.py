import requests

r = requests.get('http://127.0.0.1:8000/hi/Hassan')

def test_status_code():
    assert r.status_code == 200
