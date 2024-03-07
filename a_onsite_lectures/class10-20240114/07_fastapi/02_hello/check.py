import requests

r = requests.get('http://127.0.0.1:8000')
r = requests.get('http://127.0.0.1:8000/hi')
r = requests.get('http://127.0.0.1:8000/hi/Muhammad Qasim')

print(r)
print(r.status_code)
print(r.headers)
print(r.json())
print(r.text)