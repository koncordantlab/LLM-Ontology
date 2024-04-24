from flask import Flask, request, render_template
from controllers.controller import extend_graph_chatgpt, create_graph_chatgpt, get_insights, get_new_cancer_relations, create_flav_to_cancer, create_food_to_cancer, get_new_food_cancer_relations, get_graph_names, load_graph, merge_graphs, controller_extract_from_abstracts, graph_name_exists_in_database
from flask import jsonify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "create_graph":
            concepts = request.form["concepts"]
            relations = request.form["relations"]
            prompt = request.form["prompt"]
            graph_name = request.form["graph_name"]
            use_llama = False
            if request.form.get("UseLlama"):
                use_llama = True
            if request.form.get("extension"):
                if not graph_name_exists_in_database(graph_name):
                    error_message = "Graph name doesn't exist. Please choose a graph that exist to extend."
                    return render_template("home.html", active_tab="error", graph_names=get_graph_names(),error_message=error_message)
                extend_graph_chatgpt(prompt, concepts, relations, use_llama, graph_name)
                return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())
            if graph_name_exists_in_database(graph_name):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            create_graph_chatgpt(prompt, concepts, relations, use_llama, graph_name)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "load_graph":
            selected_graph = request.form.get("selected_graph")
            load_graph(selected_graph)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "merge_graphs":
            selected_graph1 = request.form.get("selected_graph_merge1")
            selected_graph2 = request.form.get("selected_graph_merge2")
            graph_name = request.form["graph_name_merge"]
            if graph_name_exists_in_database(graph_name):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            merge_graphs(selected_graph1, selected_graph2, graph_name)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "generate_insights":
            use_llama = False
            if request.form.get("UseLlama2"):
                use_llama = True
            selected_graph = request.form.get("selected_graph_insights")
            output = get_insights(selected_graph, use_llama)
            return render_template("home.html", active_tab="insights", graph_names=get_graph_names(), insights=output)

        elif action == "create_flav_to_cancer":
            selected_graph = request.form.get("graph_name_flavonoid1")
            if graph_name_exists_in_database(selected_graph):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            create_flav_to_cancer(selected_graph)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "create_food_to_cancer":
            selected_graph = request.form["graph_name_flavonoid3"]
            if graph_name_exists_in_database(selected_graph):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            create_food_to_cancer(selected_graph)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "new_cancer_relations":
            include_known_relations = False
            if request.form.get("include_known_relations"):
                include_known_relations = True
            num_abstracts = int(request.form["num_abstracts"])
            graph_name = request.form["graph_name_flavonoid2"]
            if graph_name_exists_in_database(graph_name):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            get_new_cancer_relations(num_abstracts, include_known_relations, graph_name)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "new_food_cancer_relations":
            num_abstracts = int(request.form["num_abstracts2"])
            graph_name = request.form["graph_name_flavonoid4"]
            if graph_name_exists_in_database(graph_name):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            get_new_food_cancer_relations(num_abstracts, graph_name)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

        elif action == "extract_from_abstracts":
            num_abstracts = int(request.form["num_abstracts3"])
            query = request.form["search_query"]
            entity_classes = request.form["entity_classes"]
            if entity_classes == "" or entity_classes is None:
                entity_classes = "entities"
            graph_name = request.form["graph_name_scrape"]
            if graph_name_exists_in_database(graph_name):
                error_message = "Graph name already exists. Please choose a different name."
                return render_template("home.html", active_tab="error", graph_names=get_graph_names(), error_message=error_message)
            controller_extract_from_abstracts(query, entity_classes, num_abstracts, graph_name)
            return render_template("home.html", active_tab="visualize", graph_names=get_graph_names())

    return render_template("home.html", active_tab="create", graph_names=get_graph_names())


if __name__ == '__main__':
    # run flask app
    app.run()