from typing import List
import requests


def post(address: str, params) -> requests.Response:
    return requests.post('http://127.0.0.1:5001' + address, json=params)


def add_competency(name: str, indicators: List[str]) -> int:
    response = post('/competencies', {'name': name, 'indicators': indicators})
    return response.json()['id']


def add_profession(name: str, area: int, competencies: List[int]):
    post('/professions', {'name': name, 'area': area, 'competencies': competencies})


def add_area(name: str):
    response = post('/areas', {'id': name})
    return response.json()['id']
