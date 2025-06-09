import requests

def get_employees_data():
    response = requests.get('http://127.0.0.1:8000/api/employees/')
    if response.status_code == 200:
        return response.json()
    return []

def get_classificator_data():
    response = requests.get('http://127.0.0.1:8000/api/trainings/')
    if response.status_code == 200:
        return response.json()
    return []

print(get_classificator_data())