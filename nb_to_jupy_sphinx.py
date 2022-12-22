"""Convert a ipynb notebook into a rst file that jupyter-sphink can read.

Functions:
    convert_notebook(input_path:Path, output_path:Path)
"""
import json
from pathlib import Path
from typing import Tuple

def _extract_notebook_cells(path:Path)->dict:
    with open(path, 'r', encoding="utf-8") as nb_file:
        notebook_cells = json.load(nb_file)['cells']
    return notebook_cells

def _get_type_and_content(cell:dict)->Tuple[str, list]:
    return (cell['cell_type'], cell['source'])

def _format_code(source:list)->str:
    formated_source = "\n.. jupyter-execute::\n"
    for line in source:
        formated_source += f"    {line}\n"
    return formated_source

def _convert_line_to_rst(title:str)->str:
    """Convert titles from markdown to rst style

    Conversion is chosen as follows:

    - # -> =
    - ## -> -
    - ### -> ^
    - #### -> "

    Parameters
    ----------
    title : str
        a one-liner string

    Returns
    -------
    str
        a two lined string with rst format
    """
    # if no "#" then just return the line
    if title[0] != "#":
        return title
    # else do the conversion
    else:
        hashtags = title.split(" ")[0]
        len_hashtags = len(hashtags)
        text = title[len_hashtags+1:]
        converter = {1: "=", 2: "-", 3: "^", 4:'"'}
        return f"{text}{converter[len_hashtags]*len(text)}\n"

def _format_markdown(source:list)->str:
    formated_source = ""
    for line in source:
        formated_source += _convert_line_to_rst(line)
    return formated_source

def convert_notebook(input_path:Path, output_path:Path):
    """_summary_

    Parameters
    ----------
    input_path : pathlib.Path
        path to the ipynb notebook to convert
    output_path : pathlib.Path
        path where to save the output rst notebook

    Raises
    ------
    ValueError
        Raised if the notebook contains
        cells that are neither "code" or "markdown"
    ValueError
        Raised if input_path does not point to a
        ipynb or json file
    """
    if str(input_path)[-6:] not in [".ipynb", '.IPYNB', '.json', '.JSON']:
        raise ValueError(
            "input_path should point to an ipynb or json file"
            )
    if str(output_path)[-4:] not in ['.rst', '.RST']:
        output_path += '.rst'
    notebook_cells = _extract_notebook_cells(input_path)
    rst_file = ""
    for cell in notebook_cells:
        cell_type, source = _get_type_and_content(cell)
        if cell_type not in ['code', 'markdown']:
            raise ValueError(
                f"cells type must be 'code' or 'markdown' but we encountered a '{cell_type}' cell."
                )
        if cell_type == "code":
            rst_file += _format_code(source)
        elif cell_type == "markdown":
            rst_file += _format_markdown(source)
    with open(output_path, "w", encoding='utf-8') as output_file:
        output_file.write(rst_file)
    