import pandas as pd
from models.converter import create_graph_and_write


def superclass_to_flavonoid_to_cancer():
    df = pd.read_csv('../input_data_files/flav.csv')

    with open("../outfiles/csv.rela", "w") as file:
        for index, row in df.iterrows():
            file.write("[{}]-({})->[{}]\n".format(row["Subclass"], "is_a_sub_class_of", row["Class"]))
            file.write("[{}]-({})->[{}]\n".format((str)(row["Label"]).replace('"', ''), "is_a_sub_class_of", row["Subclass"]))
            file.write("[{}]-({})->[{} Cancer]\n".format((str)(row["Label"]).replace('"', ''), "helps_prevent", row["Cancer"]))

    create_graph_and_write("../outfiles/csv.rela", "outfiles/csv.xml")


def subclass_to_cancer(rela_file):
    df = pd.read_csv('input_data_files/flav.csv')
    already_seen = {}
    with open(rela_file, "w") as file:
        for index, row in df.iterrows():
            if (str)(row["Cancer"]) + (str)(row["Subclass"]) not in already_seen:
                file.write("{}-{}-{} Cancer\n".format((str)(row["Subclass"]), "helps_prevent", (str)(row["Cancer"])))
                already_seen[(str)(row["Cancer"]) + (str)(row["Subclass"])] = 1

    create_graph_and_write(rela_file, "outfiles/current_graph.xml")
    return 1


def food_to_cancer(rela_file):
    df = pd.read_csv('input_data_files/flav.csv')
    already_seen = {}
    with open(rela_file, "w") as file:
        for index, row in df.iterrows():
            if (str)(row["Cancer"]) + (str)(row["Kilas"]).split()[0] not in already_seen:
                file.write("{}-{}-{} Cancer\n".format((str)(row["Kilas"]).split()[0], "helps_prevent", (str)(row["Cancer"])))
                already_seen[(str)(row["Cancer"]) + (str)(row["Kilas"]).split()[0]] = 1

    create_graph_and_write(rela_file, "outfiles/current_graph.xml")
    return 1