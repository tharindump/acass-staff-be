from owlready2 import *


class ITOntologyManager(object):
    def __init__(self):
        path = 'D:/Workspace/Project_L4/acass-staff-be/ontology/IT_Curriculum_V4_.owl'
        onto_path.append('D:/Workspace/Project_L4/acass-staff-be/ontology')
        self.onto = get_ontology(path)
        self.onto.load()
        sync_reasoner()

    def get_synonyms(self, module_name):
        module = self.onto[module_name]
        if module:
            return module.hasSynonym
        else:
            return []


if __name__ == '__main__':
    onto_manager = ITOntologyManager()
    syns = onto_manager.get_synonyms('Artificial_Intelligence')
    print(syns)
