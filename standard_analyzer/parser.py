import xml.etree.ElementTree as Et
from typing import List, Tuple
import paths

LaborActions = List[str]
RequiredSkills = List[str]
NecessaryKnowledges = List[str]
Pwf = Tuple[str, LaborActions, RequiredSkills, NecessaryKnowledges]
Gwf = Tuple[str, List[Pwf]]
Standard = Tuple[str, str, List[Gwf]]


def children(el: Et.Element, *tags) -> List[Et.Element]:
    children_ = list(el)
    assert len(children_) == len(tags)
    for child_, tag in zip(children_, tags):
        assert child_.tag == tag
    return children_


def child(el: Et.Element, tag) -> Et.Element:
    child_, = list(el)
    assert child_.tag == tag
    return child_


def children_list(el: Et.Element, tag) -> List[Et.Element]:
    children_ = list(el)
    for child_ in children_:
        assert child_.tag == tag
    return children_


def parse_professional_standard(standard_id: str) -> Standard:
    node: Et.Element = Et.parse(paths.downloaded(standard_id).path).getroot()
    assert node.tag == 'XMLCardInfo'

    node = child(node, 'ProfessionalStandarts')
    node = child(node, 'ProfessionalStandart')
    name_professional_standard, _, _, _, first_section, third_section, _ = children(node,
        'NameProfessionalStandart', 'RegistrationNumber', 'OrderNumber', 'DateOfApproval', 'FirstSection', 'ThirdSection', 'FourthSection')

    _, code_of_professional_activity, _, _ = children(first_section,
        'KindProfessionalActivity', 'CodeKindProfessionalActivity', 'PurposeKindProfessionalActivity', 'EmploymentGroup')

    standard = (name_professional_standard.text, code_of_professional_activity.text, [])

    generalized_work_functions = child(child(third_section, 'WorkFunctions'), 'GeneralizedWorkFunctions')
    for generalized_work_function in children_list(generalized_work_functions, 'GeneralizedWorkFunction'):

        _, name_otf, _, _, _, _, _, _, _, particular_work_functions = children(generalized_work_function,
            'CodeOTF', 'NameOTF', 'LevelOfQualification', 'PossibleJobTitles', 'EducationalRequirements', 'RequirementsWorkExperiences',
            'SpecialConditionsForAdmissionToWork', 'OtherCharacteristics', 'OtherCharacteristicPlus', 'ParticularWorkFunctions')

        gwf: Gwf = (name_otf.text, [])

        for particular_work_function in children_list(particular_work_functions, 'ParticularWorkFunction'):

            _, name_tf, _, labor_actions, required_skills, necessary_knowledges, _, _ = children(particular_work_function,
                'CodeTF', 'NameTF', 'SubQualification', 'LaborActions', 'RequiredSkills', 'NecessaryKnowledges', 'OtherCharacteristics',
                'ListFootnes')

            pwf: Pwf = (
                name_tf.text,
                [labor_action.text for labor_action in children_list(labor_actions, 'LaborAction')],
                [required_skill.text for required_skill in children_list(required_skills, 'RequiredSkill')],
                [necessary_knowledge.text for necessary_knowledge in children_list(necessary_knowledges, 'NecessaryKnowledge')]
            )

            gwf[1].append(pwf)

        standard[2].append(gwf)

    return standard


def convert(standards: List[str]):
    for standard_id in standards:
        standard = parse_professional_standard(standard_id)
        paths.parsed(standard_id).write(repr(standard))
