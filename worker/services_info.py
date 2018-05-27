from typing import List
import requests
from security import get_current_user_id


class Caller:
    def __init__(self, address: str):
        self.address = address

    def get(self, address: str, params=None):
        return requests.get(self.address + address, params=params).json()

    def put(self, address: str, args):
        return requests.put(self.address + address, json=args).json()

    def post(self, address: str, args):
        return requests.post(self.address + address, json=args).json()


competency_manager = Caller('http://127.0.0.1:5001')
labor_manager = Caller('http://127.0.0.1:5002')


def _load_competencies(labor):
    labor['competencies'] = [get_competency(comp_id) for comp_id in labor['competencies']]
    return labor


def get_worker_info(worker_id: int):
    return _load_competencies(labor_manager.get('/workers/%d' % worker_id))


def get_work_info(work_id: int):
    return _load_competencies(labor_manager.get('/works/%d' % work_id))


def get_employer_info(employer_id: int):
    return labor_manager.get('/employers/%d' % employer_id)


def get_current_user():
    return get_worker_info(get_current_user_id())


def add_worker(name: str) -> int:
    worker = labor_manager.post('/workers', {'name': name})
    print(worker)
    return worker['id']


def remove_comp_from_worker(worker_id: int, comp_id: int):
    worker_comps = labor_manager.get('/workers/%d' % worker_id)['competencies']
    worker_comps.remove(comp_id)
    labor_manager.put('/workers/%d' % worker_id, {'competencies': worker_comps or [-1]})


def append_comp_to_worker(worker_id: int, comp_id: int):
    worker_comps = labor_manager.get('/workers/%d' % worker_id)['competencies']
    worker_comps = sorted(set(worker_comps) | {comp_id})
    labor_manager.put('/workers/%d' % worker_id, {'competencies': worker_comps or [-1]})


def get_professions():
    return competency_manager.get('/professions')


def get_profession(prof_id: int):
    return competency_manager.get('/professions/%d' % prof_id)


def get_competencies(area_id: int, prof_id: int, description: str):
    return competency_manager.get('/competencies', {'area': area_id, 'profession': prof_id, 'description': description})


def get_competency(comp_id: int):
    return competency_manager.get('/competencies/%d' % comp_id)


def get_areas():
    return competency_manager.get('/areas')


def get_area_profs(area_id: int) -> List:
    return competency_manager.get('/professions', params={'area': area_id})


def get_best_works(worker_id: int) -> List:
    return list(map(_load_competencies, labor_manager.get('/best_works/%d' % worker_id)))


def get_demanded_competencies(worker_id: int) -> List:
    return labor_manager.get('/demanded_competencies/%d' % worker_id)


def get_employer_works(employer_id: int) -> List:
    return list(map(_load_competencies, labor_manager.get('/employer_works/%d' % employer_id)))
