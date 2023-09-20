import pytest
import pandas as pd
from unittest.mock import patch
from project import add_core_file
from project import check_column_names
from project import get_general_file
from project import get_file


@patch("builtins.input", side_effect=["1234", "yes", "/workspaces/102768536/project-b/test_files/students.csv"])
def test_add_core_file_good_file(mock_input):
    core_file_name = add_core_file(1234)
    assert core_file_name == "./csv_files/core_csv_file/core.csv"


@patch("builtins.input", side_effect=["1234", "yes", "/workspaces/102768536/project-b/test_files/students_fail.csv", "\n"])
def test_add_core_file_bad_file(mock_input):
   with pytest.raises(SystemExit):
    add_core_file(1234)

@patch("builtins.input", side_effect = "\n")
def test_check_column_names(mock_input):
   good_path = "/workspaces/102768536/project-b/test_files/students.csv"
   bad_path = "/workspaces/102768536/project-b/test_files/students_fail.csv"
   assert check_column_names(good_path) == True
   assert check_column_names(bad_path) == False

def test_get_general_file():
   file_test = pd.read_csv("./csv_files/general_file/general.csv")
   file = get_general_file()
   assert file.equals(file_test)

@patch("builtins.input", side_effect = ["test_files/students.csv"])
def test_get_file(mock_input):
   assert get_file() == "test_files/students.csv"

