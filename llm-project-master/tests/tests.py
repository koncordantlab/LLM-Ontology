import pandas as pd
import pytest

from controllers.controller import merge_graphs, get_graph_names, load_graph, create_graph_chatgpt, extend_graph_chatgpt, controller_extract_from_abstracts, graph_name_exists_in_database, create_flav_to_cancer, create_food_to_cancer
from models.database import retrieve_data_and_write
from models.chatgpt import get_chatgpt_response
from models.converter import create_graph_and_write, merge_graphs_write
from models.csv_to_graph import superclass_to_flavonoid_to_cancer, subclass_to_cancer, food_to_cancer

def test_merge_graphs_calls_merge(mocker):
    testfunction1 = mocker.patch('controllers.controller.retrieve_data_and_write', return_value=True)
    testfunction2 = mocker.patch('controllers.controller.merge_graphs_write', return_value=True)
    testfunction3 = mocker.patch('controllers.controller.upload_data', return_value=True)
    merge_graphs("graphzzz", "graphzz", "newgraph1463")
    testfunction2.assert_called_once_with("outfiles/preExtension.rela", "outfiles/current_graph.rela", "outfiles/current_graph.xml")

def test_merge_graphs_calls_retrieve(mocker):
    testfunction1 = mocker.patch('controllers.controller.retrieve_data_and_write', return_value=True)
    testfunction2 = mocker.patch('controllers.controller.merge_graphs_write', return_value=True)
    testfunction3 = mocker.patch('controllers.controller.upload_data', return_value=True)
    merge_graphs("graphzzz", "graphzz", "newgraph1463")
    assert testfunction1.call_count == 2

def test_merge_graphs_calls_upload(mocker):
    testfunction1 = mocker.patch('controllers.controller.retrieve_data_and_write', return_value=True)
    testfunction2 = mocker.patch('controllers.controller.merge_graphs_write', return_value=True)
    testfunction3 = mocker.patch('controllers.controller.upload_data', return_value=True)
    merge_graphs("graphzzz", "graphzz", "newgraph1463")
    testfunction3.assert_called_once_with("outfiles/current_graph.rela", "newgraph1463")

def test_get_graph_names(mocker):
    testfunction = mocker.patch('controllers.controller.models.database.get_all_graph_ids', return_value=['a','b','c'])
    get_graph_names()
    testfunction.assert_called_once_with()

def test_load_graph(mocker):
    testfunction1 = mocker.patch('controllers.controller.retrieve_data_and_write', return_value=True)
    testfunction2 = mocker.patch('controllers.controller.create_graph_and_write', return_value=True)
    graph_name = "graph1"
    load_graph(graph_name)
    testfunction1.assert_called_once_with("outfiles/current_graph.rela", graph_name)
    testfunction2.assert_called_once_with("outfiles/current_graph.rela", "outfiles/current_graph.xml")

def test_create_graph_chatgpt(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    testfunction1 = mocker.patch('controllers.controller.build_prompt', return_value="prompt2")
    testfunction2 = mocker.patch('controllers.controller.get_chatgpt_response', return_value="hello")
    testfunction3 = mocker.patch('controllers.controller.create_graph_and_write', return_value=True)
    testfunction4 = mocker.patch('controllers.controller.upload_data', return_value=True)

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'

    prompt = "prompt"
    concepts = "concepts"
    relations = "relations"
    use_llama = False
    graph_name = "graph1"
    create_graph_chatgpt(prompt, concepts, relations, use_llama, graph_name)

    testfunction1.assert_called_once_with(concepts, relations, prompt)
    testfunction2.assert_called_once_with("prompt2")
    testfunction3.assert_called_once_with(in_fname, out_fname)
    testfunction4.assert_called_once_with(in_fname, graph_name)

def test_extend_graph_chatgpt(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    testfunction1 = mocker.patch('controllers.controller.build_prompt', return_value="prompt2")
    testfunction2 = mocker.patch('controllers.controller.get_llama_response', return_value="hello")
    testfunction3 = mocker.patch('controllers.controller.extend_graph_and_write', return_value=True)
    testfunction4 = mocker.patch('controllers.controller.upload_data', return_value=True)
    testfunction5 = mocker.patch('controllers.controller.retrieve_data_and_write', return_value=True)
    testfunction6 = mocker.patch('controllers.controller.create_graph_and_write', return_value=True)

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'

    prompt = "prompt"
    concepts = "concepts"
    relations = "relations"
    use_llama = True
    graph_name = "graph1"
    extend_graph_chatgpt(prompt, concepts, relations, use_llama, graph_name)

    testfunction1.assert_called_once_with(concepts, relations, prompt)
    testfunction2.assert_called_once_with("prompt2")
    testfunction3.assert_called_once_with(in_fname, out_fname)
    testfunction4.assert_called_once_with(in_fname, graph_name)
    testfunction5.assert_called_once_with("outfiles/preExtension.rela", graph_name)
    testfunction6.assert_called_once_with("outfiles/preExtension.rela", "outfiles/preExtension.xml")


def test_controller_extract_from_abstracts(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    rv1 = ["abstract1"]
    testfunction1 = mocker.patch('controllers.controller.get_flavonoid_abstracts', return_value=rv1)
    testfunction2 = mocker.patch('controllers.controller.build_general_abstract_prompt', return_value="prompt")
    testfunction3 = mocker.patch('controllers.controller.get_chatgpt_response', return_value="hello")
    testfunction4 = mocker.patch('controllers.controller.create_graph_and_write', return_value=True)
    testfunction5 = mocker.patch('controllers.controller.upload_data', return_value=True)

    in_fname = 'outfiles/current_graph.rela'
    out_fname = 'outfiles/current_graph.xml'

    query = "query"
    entity_classes = "class1"
    num_abstracts = 1
    graph_name = "graph1"

    controller_extract_from_abstracts(query, entity_classes, num_abstracts, graph_name)

    testfunction1.assert_called_once_with(num_abstracts, query)
    testfunction2.assert_called_once_with(entity_classes, "abstract1")
    testfunction3.assert_called_once_with("prompt")
    testfunction4.assert_called_once_with(in_fname, out_fname)
    testfunction5.assert_called_once_with(in_fname, graph_name)

def test_chatgpt_response(mocker):

    testfunction1 = mocker.patch('models.chatgpt.get_key', return_value="hello")
    testfunction2 = mocker.patch("models.chatgpt.openai.ChatCompletion.create", return_value="testflag999")

    input = "hello"

    messages = [{"role": "system", "content":
        input}]

    get_chatgpt_response("hello")

    testfunction2.assert_called_once_with(model="gpt-3.5-turbo", messages=messages, temperature = 0.2)

def test_create_graph_and_write(mocker):

    testfunction1 = mocker.patch('models.converter.raw_relations_to_graph', return_value=None)
    testfunction2 = mocker.patch('models.converter.serialize', return_value=None)

    create_graph_and_write("1", "2")

    testfunction2.assert_called_once_with(None, "2")

def test_merge_graphs_write(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    testfunction1 = mocker.patch('models.converter.raw_relations_to_graph', return_value=None)
    testfunction2 = mocker.patch('models.converter.serialize', return_value=None)

    merge_graphs_write("1", "2", "3")

    testfunction2.assert_called_once_with(None, "3")

def test_superclass_to_flavonoid_to_cancer(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    testfunction1 = mocker.patch('models.csv_to_graph.pd.read_csv', return_value=pd.DataFrame())
    testfunction2 = mocker.patch('models.csv_to_graph.create_graph_and_write', return_value=None)

    superclass_to_flavonoid_to_cancer()

    testfunction2.assert_called_once_with("../outfiles/csv.rela", "outfiles/csv.xml")

def test_subclass_to_cancer(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    testfunction1 = mocker.patch('models.csv_to_graph.pd.read_csv', return_value=pd.DataFrame())
    testfunction2 = mocker.patch('models.csv_to_graph.create_graph_and_write', return_value=None)

    subclass_to_cancer("hello")

    testfunction2.assert_called_once_with("hello", "outfiles/current_graph.xml")

def test_food_to_cancer(mocker):
    mocked_etc_release_data = mocker.mock_open(read_data=" random text")
    builtin_open = "builtins.open"
    mocker.patch(builtin_open, mocked_etc_release_data)

    testfunction1 = mocker.patch('models.csv_to_graph.pd.read_csv', return_value=pd.DataFrame())
    testfunction2 = mocker.patch('models.csv_to_graph.create_graph_and_write', return_value=None)

    food_to_cancer("hello")

    testfunction2.assert_called_once_with("hello", "outfiles/current_graph.xml")

def test_graph_name_exists_in_database(mocker):
    testfunction1 = mocker.patch('controllers.controller.get_all_graph_ids', return_value=["graph2", "graph1"])

    value = graph_name_exists_in_database("graph1")

    assert value == True

def test_create_flav_to_cancer(mocker):
    testfunction1 = mocker.patch('controllers.controller.subclass_to_cancer', return_value=True)
    testfunction2 = mocker.patch('controllers.controller.upload_data', return_value=True)

    create_flav_to_cancer("graph1")

    testfunction2.assert_called_once_with("outfiles/current_graph.rela", "graph1")

def test_create_food_to_cancer(mocker):
    testfunction1 = mocker.patch('controllers.controller.food_to_cancer', return_value=True)
    testfunction2 = mocker.patch('controllers.controller.upload_data', return_value=True)

    create_food_to_cancer("graph1")

    testfunction2.assert_called_once_with("outfiles/current_graph.rela", "graph1")







