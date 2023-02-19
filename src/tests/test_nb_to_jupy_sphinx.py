from .. import nb_to_jupy_sphinx
from pathlib import Path
import pytest


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
            "source": ["1 + 1"],
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
        "source": ["1 + 1"],
    }
    assert nb_to_jupy_sphinx._get_type_and_content(code_cell) == ("code", ["1 + 1"])
    markdown_cell = {"cell_type": "markdown", "metadata": {}, "source": ["love u"]}
    assert nb_to_jupy_sphinx._get_type_and_content(markdown_cell) == (
        "markdown",
        ["love u"],
    )
    strange_notebook = Path.cwd() / Path(
        "src/tests/example_notebooks/strange_notebook.json"
    )
    with pytest.raises(
        ValueError,
        match="cells type must be 'code' or 'markdown' but we encountered a 'strange' cell.",
    ):
        nb_to_jupy_sphinx.convert_notebook(strange_notebook, "output.rst")


def test_format_code():
    """Test of format code."""
    assert (
        nb_to_jupy_sphinx._format_code(["1 + 1"])
        == "\n.. jupyter-execute::\n    1 + 1\n"
    )


def test_format_markdown():
    """Test fro format markdown."""
    complicated_cell = [
        "# Title\n",
        "\n",
        "## 1\n",
        "\n",
        "## 2\n",
        "\n",
        "### 4\n",
        "\n",
        "### 5\n",
        "\n",
        "- list1\n",
        "- list2\n",
        "- list3\n",
        "  - sublist1\n",
        "  - sublist2\n",
        "  - sublist3\n",
        "\n",
        "#### 6\n",
        "\n",
        "##### 7",
    ]
    expected_output = 'Title\n======\n\n1\n--\n\n2\n--\n\n4\n^^\n\n5\n^^\n\n- list1\n- list2\n- list3\n  - sublist1\n  - sublist2\n  - sublist3\n\n6\n""\n\n**7**'
    assert nb_to_jupy_sphinx._format_markdown(complicated_cell) == expected_output


def test_input_and_output_format():
    """Test files extensions for convert_notebook."""
    with pytest.raises(
        ValueError, match="input_path should point to an ipynb or json file"
    ):
        nb_to_jupy_sphinx.convert_notebook(Path("test.file"), Path("test.rst"))
