from .. import nb_to_jupy_sphinx
from pathlib import Path


def test_file_regression(file_regression):
    """Test wether applying the function again changes the output file."""
    input_path = Path.cwd() / Path("src/tests/example_notebooks/example_notebook.ipynb")
    output_path = Path.cwd() / Path("src/tests/example_notebooks/example_notebook.rst")
    nb_to_jupy_sphinx.convert_notebook(input_path, output_path)
    with open(output_path) as example_notebook:
        file_regression.check(example_notebook.read(), extension=".rst")


def test_extract_notebook_cells():
    """Extract the cells of one example notebook."""
    input_path = Path.cwd() / Path(
        "src/tests/example_notebooks/one_code_cell_one_markdown.ipynb"
    )
    extracted_cells = nb_to_jupy_sphinx._extract_notebook_cells(input_path)
    expected = [
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [
                {
                    "data": {"text/plain": ["2"]},
                    "execution_count": 1,
                    "metadata": {},
                    "output_type": "execute_result",
                }
            ],
            "source": ["1+1"],
        },
        {"cell_type": "markdown", "metadata": {}, "source": ["Markdown here"]},
    ]
    assert extracted_cells == expected


def test_get_type_and_content():
    """Test type and content extraction for cells."""
    code_cell = {
        "cell_type": "code",
        "execution_count": 1,
        "metadata": {},
        "outputs": [
            {
                "data": {"text/plain": ["2"]},
                "execution_count": 1,
                "metadata": {},
                "output_type": "execute_result",
            }
        ],
        "source": ["1+1"],
    }
    assert nb_to_jupy_sphinx._get_type_and_content(code_cell) == ("code", ["1+1"])
