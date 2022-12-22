import json

with open('example_notebook.ipynb', 'r', encoding="utf-8") as nb_file:
    notebook = json.load(nb_file)

print(notebook)
