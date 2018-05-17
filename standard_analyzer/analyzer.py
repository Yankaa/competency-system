from typing import List
from ast import literal_eval
from parser import Standard
from web import add_competency, add_profession, add_area


def analyze_standard(standard: Standard):
    profession_name, code_of_professional_activity, gwf_list = standard
    area = code_of_professional_activity.split('.')[0]
    area_id = add_area(area)

    competencies = []
    for gwf_name, pwf_list in gwf_list:
        indicators = [pwf_name for pwf_name, *lists in pwf_list]
        competency_id = add_competency(gwf_name, indicators)
        competencies.append(competency_id)

    add_profession(profession_name, area_id, competencies)


def analyze(fresh_standards: List[str]):
    for standard_id in fresh_standards:
        filename = 'parsed/' + standard_id + '.txt'
        file = open(filename, 'r')
        content = file.read()
        file.close()
        standard: Standard = literal_eval(content)
        analyze_standard(standard)
