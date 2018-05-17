from typing import List, Dict, TypeVar, Callable, Iterable
from data import list_workers, list_works, Worker, Work


candidates: Dict[int, float] = {}


def init():
    workers = list_workers()
    for work in list_works():
        candidates[work.id] = sum(employability(worker, work) for worker in workers)


# предрасположенность соискателя worker к вакансии work
def employability(worker: Worker, work: Work) -> float:
    work_cnt = len(work.competencies)
    worker_cnt = len(worker.competencies)
    common_cnt = len(set(work.competencies) & set(worker.competencies))
    all_cnt = work_cnt + (worker_cnt - common_cnt) / 2
    return (common_cnt / all_cnt) ** 2


# повышение предрасположенности соискателя worker к вакансии work при замене бесполезной компетенции на полезную
def employability_diff(worker: Worker, work: Work) -> float:
    work_cnt = len(work.competencies)
    worker_cnt = len(worker.competencies)
    common_cnt = len(set(work.competencies) & set(worker.competencies))
    values = []
    for common_up in 1, 0:
        all_cnt = work_cnt + ((worker_cnt+1) - (common_cnt+common_up))/2
        values += ((common_cnt+common_up) / all_cnt)**2,
    useful, useless = values
    return useful - useless


T = TypeVar('T')


def _get_top_n(list1: Iterable[T], n: int, get_key: Callable[[T], float]) -> List[T]:
    list2 = []
    for elem in list1:
        key = get_key(elem)
        if key != 0:
            list2.append((-key, elem))
    list2.sort(key=lambda x: x[0])
    list2 = list2[:n]
    list2 = [elem[1] for elem in list2]
    return list2


def best_works(worker: Worker) -> List[Work]:
    # трудоустраиваемость на вакансию work
    def get_key(work: Work) -> float:
        return employability(worker, work) / candidates[work.id] * work.salary

    return _get_top_n(list_works(), 10, get_key)


def best_workers(work: Work) -> List[Worker]:
    def get_key(worker: Worker) -> float:
        return employability(worker, work)

    return _get_top_n(list_workers(), 10, get_key)


# вычисляет потребности в компетенциях соискателя worker и заносит найденные значения в employabilities_up
def _count_employabilities_up(worker: Worker, works: List[Work], employabilities_up: Dict[int, float]):
    for work in works:
        employability_on_vacancy_diff = employability_diff(worker, work) / candidates[work.id] * work.salary
        for competency in work.competencies:
            if competency not in worker.competencies:
                employabilities_up[competency] = employabilities_up.get(competency, 0) + employability_on_vacancy_diff


def demanded_competencies(worker: Worker) -> List[int]:
    employabilities_up: Dict[int, float] = {}
    _count_employabilities_up(worker, list_works(), employabilities_up)
    return _get_top_n(employabilities_up, 10, employabilities_up.__getitem__)


def global_demanded_competencies() -> List[int]:
    employabilities_up: Dict[int, float] = {}
    works = list_works()
    for worker in list_workers():
        _count_employabilities_up(worker, works, employabilities_up)
    return _get_top_n(employabilities_up, 10, employabilities_up.__getitem__)
