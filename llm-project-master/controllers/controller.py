import models.database
from models.converter import create_graph_and_write, extend_graph_and_write, merge_graphs_write
from models.chatgpt import get_chatgpt_response
from models.llama import get_llama_response
from models.prompt_builder import build_prompt, build_insights_prompt, build_new_cancer_relations_prompt, build_new_cancer_relations_prompt_with_known_relations, build_new_food_cancer_relations_prompt, build_general_abstract_prompt
from models.paper_scrape import get_flavonoid_abstracts
from models.csv_to_graph import subclass_to_cancer, food_to_cancer
from models.database import upload_data, retrieve_data_and_write, get_all_graph_ids


def merge_graphs(graph1, graph2, new_graph_name):
    rela_graph1 = "outfiles/preExtension.rela"
    rela_graph2 = "outfiles/current_graph.rela"
    output_file = "outfiles/current_graph.xml"
    retrieve_data_and_write(rela_graph1, graph1)
    retrieve_data_and_write(rela_graph2, graph2)
    merge_graphs_write(rela_graph1, rela_graph2, output_file)

    upload_data(rela_graph2, new_graph_name)

def get_graph_names():
    graph_names = models.database.get_all_graph_ids()
    return graph_names


def load_graph(graph_name):
    retrieve_data_and_write("outfiles/current_graph.rela", graph_name)
    create_graph_and_write("outfiles/current_graph.rela", "outfiles/current_graph.xml")
    return True

def create_graph_chatgpt(prompt, concepts, relations, use_llama, graph_name):
    print("herex1")
    input = build_prompt(concepts, relations, prompt)
    print(input)
    output = ''
    if use_llama:
        output = get_llama_response(input)
    else:
        output = get_chatgpt_response(input)

    output = output.replace("[", "")
    output = output.replace("]", "")
    output = output.replace("(", "")
    output = output.replace(")", "")
    output = output.replace(" ", "")
    output = output.replace("*", "")
    output = output.replace(">", "")


    print("\n\n")
    print(output)
    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'
    with open(in_fname, 'w') as f:
        outputs = output.split("\n")
        for line in outputs:
            if "-" in line:
                f.write(line)
                f.write("\n")
    create_graph_and_write(in_fname, out_fname)
    print("created graph file success")
    upload_data(in_fname, graph_name)
    print('uploaded graph success')
    return True


def extend_graph_chatgpt(prompt, concepts, relations, use_llama, graph_name):
    input = build_prompt(concepts, relations, prompt)
    print(input)
    output = ''
    if use_llama:
        output = get_llama_response(input)
    else:
        output = get_chatgpt_response(input)

    output = output.replace("[", "")
    output = output.replace("]", "")
    output = output.replace("(", "")
    output = output.replace(")", "")
    output = output.replace(" ", "")
    output = output.replace("*", "")

    retrieve_data_and_write("outfiles/preExtension.rela", graph_name)
    create_graph_and_write("outfiles/preExtension.rela", "outfiles/preExtension.xml")

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'
    with open(in_fname, 'w') as f:
        outputs = output.split("\n")
        for line in outputs:
            if "-" in line:
                f.write(line)
                f.write("\n")
    extend_graph_and_write(in_fname, out_fname)
    upload_data(in_fname, graph_name)
    return True

def get_insights(graph_name, use_llama):
    rela_file_name = "outfiles/current_graph.rela"

    retrieve_data_and_write(rela_file_name, graph_name)
    create_graph_and_write(rela_file_name, "outfiles/current_graph.xml")

    relations = ''
    with open(rela_file_name, 'r') as f:
        relations = f.read()
    input = build_insights_prompt(relations)
    print(input)
    output = ''
    if use_llama:
        output = get_llama_response(input)
    else:
        output = get_chatgpt_response(input)
    return output


def get_new_cancer_relations(num_abstracts, use_known_relations, graph_name):
    abstracts = get_flavonoid_abstracts(num_abstracts)

    outputs = []

    for abstract in abstracts:
        abstract1 = abstract
        if abstract1 is not None:
            input = ''
            if use_known_relations:
                input = build_new_cancer_relations_prompt_with_known_relations(abstract1)
            else:
                input = build_new_cancer_relations_prompt(abstract1)
            output = get_chatgpt_response(input)
            outputs.append(output)

    output_text = ''
    for thing in outputs:
        output_text += thing
        output_text += "\n"

    output_text = output_text.replace("[", "")
    output_text = output_text.replace("]", "")
    output_text = output_text.replace("(", "")
    output_text = output_text.replace(")", "")
    output_text = output_text.replace(" ", "")
    output_text = output_text.replace("*", "")
    output_text = output_text.replace(">", "")
    output_text = output_text.replace("\n\n", "\n")

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'
    with open(in_fname, 'w') as f:
        f.write(output_text)
    create_graph_and_write(in_fname, out_fname)
    upload_data(in_fname, graph_name)

    return True


def get_new_food_cancer_relations(num_abstracts, graph_name):
    abstracts = get_flavonoid_abstracts(num_abstracts)

    outputs = []

    for abstract in abstracts:
        abstract1 = abstract
        if abstract1 is not None:
            input = build_new_food_cancer_relations_prompt(abstract1)
            output = get_chatgpt_response(input)
            outputs.append(output)

    output_text = ''
    for thing in outputs:
        output_text += thing
        output_text += "\n"

    output_text = output_text.replace("[", "")
    output_text = output_text.replace("]", "")
    output_text = output_text.replace("(", "")
    output_text = output_text.replace(")", "")
    output_text = output_text.replace(" ", "")
    output_text = output_text.replace("*", "")
    output_text = output_text.replace(">", "")
    output_text = output_text.replace("\n\n", "\n")

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'
    with open(in_fname, 'w') as f:
        f.write(output_text)
    create_graph_and_write(in_fname, out_fname)
    upload_data(in_fname, graph_name)

    return True


def create_flav_to_cancer(graph_name):
    rela_file = "outfiles/current_graph.rela"
    subclass_to_cancer(rela_file)
    upload_data(rela_file, graph_name)
    return True


def create_food_to_cancer(graph_name):
    rela_file = "outfiles/current_graph.rela"
    food_to_cancer(rela_file)
    print("GRAPH NAME:")
    print(graph_name)
    upload_data(rela_file, graph_name)
    return True

def controller_extract_from_abstracts(query, entity_classes, num_abstracts, graph_name):
    abstracts = get_flavonoid_abstracts(num_abstracts, query)

    outputs = []

    for abstract in abstracts:
        abstract1 = abstract
        if abstract1 is not None:
            input = build_general_abstract_prompt(entity_classes, abstract1)
            output = get_chatgpt_response(input)
            outputs.append(output)

    output_text = ''
    for thing in outputs:
        output_text += thing
        output_text += "\n"

    output_text = output_text.replace("[", "")
    output_text = output_text.replace("]", "")
    output_text = output_text.replace("(", "")
    output_text = output_text.replace(")", "")
    output_text = output_text.replace(" ", "")
    output_text = output_text.replace("*", "")
    output_text = output_text.replace(">", "")
    output_text = output_text.replace("\n\n", "\n")

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'
    with open(in_fname, 'w') as f:
        f.write(output_text)
    create_graph_and_write(in_fname, out_fname)
    upload_data(in_fname, graph_name)

    return True

def graph_name_exists_in_database(graph_name):
    current_graph_names = get_all_graph_ids()
    return graph_name in current_graph_names

'''
#Probably trash, but maybe good for later
def extract_concepts(prompt):
    concepts_prompt = 
        From the following paragraph, extract potential ontological concepts (classes) and respond in the following format.

        Format:
        - name

        Paragraph:  + prompt
    print("\n\nConcepts Prompt:  " + concepts_prompt + "\n\n")
    return get_chatgpt_response(concepts_prompt)
'''