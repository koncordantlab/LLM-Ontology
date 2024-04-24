import pandas as pd
from models.converter import create_graph_and_write

df = pd.read_csv('../input_data_files/flav.csv')

print(df.to_string())
print(df.info())

already_seen = {}

with open("../outfiles/csv_in_natural_text.txt", "w") as file:
    for index, row in df.iterrows():
        if (str)(row["Cancer"]) + (str)(row["Subclass"]) not in already_seen:
            #file.write("{} has chemical composition component {} and {} has a therapeutic effect on {} cancer.\n".format((str)(row["Kilas"]).split()[0], (str)(row["Label"]).replace('"', ''), (str)(row["Label"]).replace('"', ''), row["Cancer"]))
            file.write(
                "{} has a therapeutic effect on {} cancer.\n".format(
                    (str)(row["Subclass"]), row["Cancer"]))
            already_seen[(str)(row["Cancer"]) + (str)(row["Subclass"])] = 1