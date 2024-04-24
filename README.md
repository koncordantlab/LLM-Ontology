# OLIVE (Ontology Learning with Integrated Vector Embedding) 🍃

## Project Overview

The Flavonoid Knowledge Graph is a comprehensive system that integrates various data sources to provide a deep understanding of flavonoids and their relationships. This project leverages natural language processing, machine learning, and graph databases to create a powerful knowledge base for researchers, scientists, and enthusiasts. 🔍🧪

## Key Features

1. **Flavonoid Data Extraction**: Automatically extract and curate flavonoid data from scientific literature and online sources. 🔍📚
2. **Semantic Enrichment**: Enhance the flavonoid data with semantic annotations and relationships using natural language processing techniques. 🌐🤖
3. **Knowledge Graph Construction**: Build a Neo4j graph database to store the flavonoid data and their interconnections. 🗃️🔗
4. **Intelligent Querying**: Develop advanced querying capabilities to explore the flavonoid knowledge graph and uncover insights. 🔍💡
5. **Visualization and Exploration**: Provide intuitive visualizations and interactive interfaces for users to explore the flavonoid knowledge graph. 🖥️🔍

## Project Setup Guide 🚀

To set up the project and get it running, follow these steps:

1. **Clone the Repository:**
   - Clone the repository from GitHub:
     ```bash
     git clone https://github.com/koncordantlab/LLM-Ontology
     ```

2. **Verify Python Version:**
   - Ensure you have Python version 3.9 installed. While the project currently runs on Python 3.9, it should work on any version more recent than that. 🐍

3. **Install Python Packages:**
   - Install the required Python packages listed in the `requirements.txt` file. You can do this using pip:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configure API Keys:**
   - Place the appropriate API keys into a `config.json` file at the root of the project, right next to `main.py`. These keys are required to connect to all the APIs used in the project. 🔑🔒
   - You need the following API keys for full project functionality:
     ```json
     {
         "CHATGPT_API_KEY": "",
         "LLAMA_API_KEY": "",
         "SCHOLAR_API_KEY": "",
         "NEO4J_URI": "",
         "NEO4J_USERNAME": "",
         "NEO4J_PASSWORD": ""
     }
     ```

5. **Acquire Flavonoid Data:**
   - If you intend to work with flavonoids, obtain the `flav.csv` file from someone within the project team. 📁💾
   - Place the `flav.csv` file in the `input_data_files` folder.

6. **Run the Project:**
   - Once everything is set up, run the project and explore its functionality! 🚀🌟

Now you're all set to dive into the project and start exploring its features and capabilities. Happy coding! 🎉
