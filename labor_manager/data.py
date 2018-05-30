from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()


class Employer(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    description: str = db.Column(db.String, nullable=False)


class Worker(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    competencies: List[int] = db.Column(db.PickleType, nullable=False)


class Work(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    description: str = db.Column(db.String, nullable=False)
    salary: int = db.Column(db.Integer, nullable=False)
    competencies: List[int] = db.Column(db.PickleType, nullable=False)

    employer_id: int = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)
    employer = db.relationship('Employer', backref=db.backref('works', lazy=True))


def add_work(description: str, salary: int, employer_id: int, competencies: List[int]) -> Work:
    work = Work(description=description, salary=salary, employer_id=employer_id, competencies=competencies)
    db.session.add(work)
    db.session.commit()
    return work


def get_work(work_id: int) -> Work:
    return Work.query.get_or_404(work_id)


def change_work(work_id: int, description: str = None, salary: int = None, competencies: List[int] = None) -> Work:
    work = Work.query.get_or_404(work_id)
    if description is not None:
        work.description = description
    if salary is not None:
        work.salary = salary
    if competencies is not None:
        work.competencies = [] if competencies == [-1] else competencies  # hack for requests
    db.session.commit()
    return work


def list_works() -> List[Work]:
    return Work.query.all()


def add_worker(name: str, competencies: List[int]) -> Worker:
    worker = Worker(name=name, competencies=competencies or [])
    db.session.add(worker)
    db.session.commit()
    return worker


def get_worker(worker_id: int) -> Worker:
    return Worker.query.get_or_404(worker_id)


def change_worker(worker_id: int, name: str, competencies: List[int]) -> Worker:
    worker = get_worker(worker_id)
    if name is not None:
        worker.description = name
    if competencies is not None:
        worker.competencies = [] if competencies == [-1] else competencies  # hack for requests
    db.session.commit()
    return worker


def list_workers() -> List[Worker]:
    return Worker.query.all()


def add_employer(name: str, description: str) -> Employer:
    employer = Employer(name=name, description=description)
    db.session.add(employer)
    db.session.commit()
    return employer


def get_employer(employer_id: int) -> Employer:
    return Employer.query.get_or_404(employer_id)


def change_employer(employer_id: int, name: str, description: str) -> Employer:
    employer = get_employer(employer_id)
    employer.name = name
    employer.description = description
    db.session.commit()
    return employer


def list_employers() -> List[Employer]:
    return Employer.query.all()


def employer_works(employer_id: int) -> List[Work]:
    return get_employer(employer_id).works


def create_bd():
    db.drop_all()
    db.create_all()
