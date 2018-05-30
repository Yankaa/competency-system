from flask_sqlalchemy import SQLAlchemy
from typing import List
import semantic

db = SQLAlchemy()


class Competency(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    vector = db.Column(db.PickleType)
    indicators: str = db.Column(db.String, nullable=False)


competency_profession = db.Table('competency_profession',
    db.Column('competency_id', db.Integer, db.ForeignKey('competency.id'), primary_key=True),
    db.Column('profession_id', db.Integer, db.ForeignKey('profession.id'), primary_key=True)
)


class Area(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)


class Profession(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String, nullable=False)
    area_id: int = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship('Area', backref=db.backref('professions', lazy=True))
    competencies: List[Competency] = db.relationship('Competency', secondary=competency_profession, backref='professions')


def add_competency(name: str, indicators: List[str]) -> Competency:
    vector = semantic.text_to_vec(indicators)
    competency = Competency(name=name, vector=vector, indicators='\n'.join(indicators))
    db.session.add(competency)
    db.session.commit()
    return competency


def add_profession(name: str, area_id: int, competencies_id: List[int]):
    competencies = [get_competency(comp_id) for comp_id in competencies_id]
    profession = Profession(name=name, area_id=area_id, competencies=competencies)
    db.session.add(profession)
    db.session.commit()
    return profession


def add_area(name: str):
    area = Area(name=name)
    db.session.add(area)
    db.session.commit()
    return area


def get_competency(comp_id: int) -> Competency:
    return Competency.query.get_or_404(comp_id)


def get_profession(prof_id: int) -> Profession:
    return Profession.query.get_or_404(prof_id)


def get_area(area_id: int) -> Area:
    return Area.query.get_or_404(area_id)


def change_profession(prof_id: int, added: List[int] = None, deleted: List[int] = None) -> Profession:
    prof: Profession = Profession.query.get_or_404(prof_id)
    if added is not None:
        for x in added:
            comp = Competency.query.get(x)
            if comp is not None:
                prof.competencies.append(comp)
    if deleted is not None:
        deleted = set(deleted)
        prof.competencies = [comp for comp in prof.competencies if comp.id not in deleted]
    db.session.commit()
    return prof


def change_area(area_id: int, name: str) -> Area:
    area: Area = Profession.query.get_or_404(area_id)
    area.name = name
    db.session.commit()
    return area


def list_competencies(args=None) -> List[Competency]:
    if args is None:
        return Competency.query.all()[:10]

    if args.profession:
        competencies = list(Profession.query.get_or_404(args.profession).competencies)
    elif args.area:
        competencies = Competency.query.join((Profession, Competency.professions)).filter(Profession.area_id == args.area).all()
    else:
        competencies = Competency.query.all()

    if args.description:
        vec = semantic.text_to_vec(args.description)
        competency_similarities = []
        for competency in competencies:
            competency_similarities.append((semantic.similarity(competency.vector, vec), competency))
        competency_similarities.sort(key=lambda pair: pair[0], reverse=True)
        competencies = [pair[1] for pair in competency_similarities]

    return competencies[:10]


def list_professions(area_id: int=None) -> List[Profession]:
    if area_id:
        return Profession.query.filter(Profession.area_id == area_id).all()
    return Profession.query.all()


def list_areas() -> List[Area]:
    return Area.query.all()


def create_bd():
    db.drop_all()
    db.create_all()
