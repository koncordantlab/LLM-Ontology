prompt_variations = \
    {
        'has_relations' : 'Here is a list of relations, generate an ontology using the following format and must only use relations from the specified list:\n\nFormat:\n[Concept A]-(Relation)-[Concept B]\ne.g. [X]-(is_child_of)-[Y]\n\n',
        'has_concepts' : 'Here is a list of concepts, generate an ontology with relations using the following format and must only use concepts from the specified list:\n\nFormat:\n[Concept A]-(Relation)-[Concept B]\ne.g. [X]-(is_child_of)-[Y]\n\n',
        'neither' : 'Here is some context, generate an ontology with relations and concepts using the following format:\n\nFormat:\n[Concept A]-(Relation)-[Concept B]\ne.g. [X]-(is_child_of)-[Y]\n\n',
        'both' : 'Here is a list of concepts and relations, generate an ontology using the following format and must only use relations from the specified list:\n\nFormat:\n[Concept A]-(Relation)-[Concept B]\ne.g. [X]-(is_child_of)-[Y]\n\n'
    }

def build_prompt(concepts, relations, initial_prompt):
    concepts = concepts.replace(';', '\n')
    relations = relations.replace(';', '\n')
    concepts = concepts.replace(' ', '')
    relations = relations.replace(' ', '')

    has_concepts = not (concepts == '')
    has_relations = not (relations == '')

    final_prompt = ''
    if has_concepts and has_relations:
        print('\n\nBranch 1\n\n')
        final_prompt = prompt_variations['both'] + 'Concepts:\n' + concepts + '\n\nRelations:\n' + relations + '\n\nContext:\n' + initial_prompt
    elif has_concepts:
        print('\n\nBranch 2\n\n')
        final_prompt = prompt_variations['has_concepts'] + 'Concepts:\n' + concepts\
                            + '\n\nContext:\n' + initial_prompt
    elif has_relations:
        print('\n\nBranch 3\n\n')
        final_prompt = prompt_variations['has_relations'] + 'Relations:\n' + relations\
                            + '\n\nContext:\n' + initial_prompt
    else:
        print('\n\nBranch 4\n\n')
        final_prompt = prompt_variations['neither'] + 'Context:\n' + initial_prompt
    return final_prompt


insights_prompt = 'Given the following relations (with format: [entity1]-(relation)->[entity2]), give me any interesting insights you can find from this data:\n\n'


def build_insights_prompt(relations):
    return insights_prompt + relations


def build_new_cancer_relations_prompt(abstract):
    return new_cancer_relations_prompt + abstract


def build_new_cancer_relations_prompt_with_known_relations(abstract):
    return new_cancer_relations_prompt_with_known_relations + abstract

def build_new_food_cancer_relations_prompt(abstract):
    return new_food_cancer_relations_prompt + abstract

def build_general_abstract_prompt(entity_classes, abstract):
    return new_general_relations_prompt.replace("{}", entity_classes.replace(",", " and ")) + abstract

new_general_relations_prompt = '''We are trying to figure out the relations between {}. Here is an abstract. Interpret the abstract and generate an ontology output using the following format that shows the relationships of the entities:

        Format:
        [Entity A]-(relation)-[Entity B]

        e.g. [X]-(relation)-[Y]

        Context: '''

new_cancer_relations_prompt = '''We are trying to figure out which flavonoids help with which cancers. Here is a list of cancers, flavonoids, and relations along with an abstract. Interpret the abstract and generate an output using the following format and must only use cancers and flavonoids and relations from the specified list:

        Format:
        [Flavonoid A]-(relation)-[Cancer B]

        e.g. [X]-(relation)-[Y]

        Cancers:
        Prostate
        Bone
        Breast
        Colorectal
        Leukemia
        Liver
        Bladder
        Cervical
        Esophageal
        Lung
        Colon
        Oral
        Skin
        Gastric
        Myeloid
        Lymphoid
        Tongue
        Pancreatic

        Flavonoids:
        Cyanidin
        Delphinidin
        Pelargonidin
        Catechin
        Epicatechin
        Apigenin
        Luteolin
        Kaempferol
        Myricetin
        Epigallocatechin gallate
        Hesperetin
        Naringenin
        Isorhamnetin
        Quercetin
        Eriocitrin
        
        Relations:
        is_therapeutic_for
        is_preventative_for

        Context: '''

new_cancer_relations_prompt_with_known_relations = '''We are trying to figure out which flavonoids help with which cancers. Here is a list of cancers, flavonoids, relations, and some already known relations along with an abstract. Interpret the abstract and generate an output using the following format and must only use cancers and flavonoids and relations from the specified list and the output should be new (meaning not in the known relations):

        Format:
        [Flavonoid A]-(relation)-[Cancer B]

        e.g. [X]-(relation)-[Y]

        Cancers:
        Prostate
        Bone
        Breast
        Colorectal
        Leukemia
        Liver
        Bladder
        Cervical
        Esophageal
        Lung
        Colon
        Oral
        Skin
        Gastric
        Myeloid
        Lymphoid
        Tongue
        Pancreatic

        Flavonoids:
        Cyanidin
        Delphinidin
        Pelargonidin
        Catechin
        Epicatechin
        Apigenin
        Luteolin
        Kaempferol
        Myricetin
        Epigallocatechin gallate
        Hesperetin
        Naringenin
        Isorhamnetin
        Quercetin
        Eriocitrin

        Relations:
        is_therapeutic_for
        is_preventative_for
        
        Already Known Relations:
        Cyanidin has a therapeutic effect on Blood cancer.
        Cyanidin has a therapeutic effect on Breast cancer.
        Cyanidin has a therapeutic effect on Colorectal cancer.
        Cyanidin has a therapeutic effect on Leukemia cancer.
        Cyanidin has a therapeutic effect on Oral cancer.
        Delphinidin has a therapeutic effect on Breast cancer.
        Delphinidin has a therapeutic effect on Leukemia cancer.
        Delphinidin has a therapeutic effect on Liver cancer.
        Pelargonidin has a therapeutic effect on Bone cancer.
        Pelargonidin has a therapeutic effect on Breast cancer.
        Pelargonidin has a therapeutic effect on Leukemia cancer.
        Pelargonidin has a therapeutic effect on Liver cancer.
        Catechin has a therapeutic effect on Bladder cancer.
        Catechin has a therapeutic effect on Breast cancer.
        Catechin has a therapeutic effect on Cervical cancer.
        Catechin has a therapeutic effect on Esophageal cancer.
        Catechin has a therapeutic effect on Lung cancer.
        Catechin has a therapeutic effect on Prostate cancer.
        Epicatechin has a therapeutic effect on Gastric cancer.
        Epicatechin has a therapeutic effect on Prostate cancer.
        Epigallocatechin gallate has a therapeutic effect on Bladder cancer.
        Epigallocatechin gallate has a therapeutic effect on Breast cancer.
        Epigallocatechin gallate has a therapeutic effect on Leukemia cancer.
        Epigallocatechin gallate has a therapeutic effect on Lung cancer.
        Epigallocatechin gallate has a therapeutic effect on Prostate cancer.
        Eriodictyol has a therapeutic effect on Breast cancer.
        Hesperetin has a therapeutic effect on Breast cancer.
        Hesperetin has a therapeutic effect on Myeloid cancer.
        Naringenin has a therapeutic effect on Breast cancer.
        Naringenin has a therapeutic effect on Lymphoid cancer.
        Apigenin has a therapeutic effect on Breast cancer.
        Apigenin has a therapeutic effect on Colorectal cancer.
        Luteolin has a therapeutic effect on Breast cancer.
        Luteolin has a therapeutic effect on Lung cancer.
        Luteolin has a therapeutic effect on Tongue cancer.
        Isorhamnetin has a therapeutic effect on Breast cancer.
        Kaempferol has a therapeutic effect on Bone cancer.
        Kaempferol has a therapeutic effect on Breast cancer.
        Kaempferol has a therapeutic effect on Prostate cancer.
        Myricetin has a therapeutic effect on Breast cancer.
        Myricetin has a therapeutic effect on Colon cancer.
        Myricetin has a therapeutic effect on Prostate cancer.
        Quercetin has a therapeutic effect on Bladder cancer.
        Quercetin has a therapeutic effect on Breast cancer.
        Quercetin has a therapeutic effect on Colorectal cancer.
        Quercetin has a therapeutic effect on Kidney cancer.
        Quercetin has a therapeutic effect on Pancreatic cancer.
        Quercetin has a therapeutic effect on Prostate cancer.
        Quercetin has a therapeutic effect on Squamous cell (skin) cancer.
        Eriocitrin has a therapeutic effect on Breast cancer.
        Hesperidin has a therapeutic effect on Breast cancer.
        Epicatechin has a therapeutic effect on Breast cancer.

        Context: '''


new_food_cancer_relations_prompt = '''We are trying to figure out which foods help with which cancers. Here is a list of cancers and relations along with an abstract. See if their and any foods mentioned in the abstract with a relation to a cancer. Interpret the abstract and generate an output using the following format and must only use cancers and relations from the specified list:

        Format:
        [Food A]-(relation)-[Food B]

        e.g. [X]-(relation)-[Y]

        Cancers:
        Prostate
        Bone
        Breast
        Colorectal
        Leukemia
        Liver
        Bladder
        Cervical
        Esophageal
        Lung
        Colon
        Oral
        Skin
        Gastric
        Myeloid
        Lymphoid
        Tongue
        Pancreatic
        
        Relations:
        is_therapeutic_for
        is_preventative_for

        Context: '''