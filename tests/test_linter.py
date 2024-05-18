import unittest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir + '/Scripts')

from Scripts.Linter import Linter
from Scripts.Settings import Settings


def get_link_to_file(file=None, line=None):
    """ Print a link in PyCharm to a line in file. Defaults to line where this function was called. """
    return f"file:///{file}"


directory_of_tests = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TestFiles\\Linter")


class TestCleanFiles(unittest.TestCase):
    def test_clean_code_1(self):
        self.check_clean_by_filename("test_clean_1.cs")

    def test_clean_code_2(self):
        self.check_clean_by_filename("test_clean_2.cs")

    def test_clean_code_3(self):
        self.check_clean_by_filename("test_clean_3.cs")

    def check_clean_by_filename(self, filename):
        directory = directory_of_tests + f"\\CleanFiles\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings([]))
        try:
            linter.analyze_file(path)
        except Exception:
            self.fail(f"Was error in work linter. Filename: {get_link_to_file(directory.replace("\\", "/"), 1)}")
        else:
            msg = f"\n" + "-" * 30 + " FAILED " + "-" * 30 + "\n\nCSharp file: "
            msg += f"{get_link_to_file(directory.replace("\\", "/"), 1)}\n"
            msg += f"Mismatches :\n"
            for mismatch in linter.mismatches:
                msg += str(mismatch) + "\n"
            msg += "-" * 70 + "\n\n"
            self.assertEqual(0, len(linter.mismatches), msg)
        finally:
            linter.mismatches = []


class BaseFunctionalNoMistakes(unittest.TestCase):

    def test_while(self):
        self.check_clean_by_filename("while.cs")

    def test_do_while(self):
        self.check_clean_by_filename("do_while.cs")

    def test_for(self):
        self.check_clean_by_filename("for.cs")

    def test_foreach(self):
        self.check_clean_by_filename("foreach.cs")

    def test_if_else(self):
        self.check_clean_by_filename("if_else.cs")

    def test_namespace(self):
        self.check_clean_by_filename("namespace.cs")

    def test_class(self):
        self.check_clean_by_filename("class.cs")

    def test_switch_case(self):
        self.check_clean_by_filename("switch_case.cs")

    def check_clean_by_filename(self, filename):
        directory = directory_of_tests + f"\\Main\\Clean\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings([]))
        try:
            linter.analyze_file(path)
        except Exception:
            self.fail(f"Was error in work linter. Filename: {get_link_to_file(directory.replace("\\", "/"), 1)}")
        else:
            msg = f"\n" + "-" * 30 + " FAILED " + "-" * 30 + "\n\nCSharp file: "
            msg += f"{get_link_to_file(directory.replace("\\", "/"), 1)}\n"
            msg += f"Mismatches :\n"
            for mismatch in linter.mismatches:
                msg += str(mismatch) + "\n"
            msg += "-" * 70 + "\n\n"
            self.assertEqual(0, len(linter.mismatches), msg)
        finally:
            linter.mismatches = []

class BaseFunctionalWithMistakes(unittest.TestCase):

    def test_while(self):
        self.check_clean_by_filename("while.cs")

    def test_do_while(self):
        self.check_clean_by_filename("do_while.cs")

    def test_for(self):
        self.check_clean_by_filename("for.cs")

    def test_foreach(self):
        self.check_clean_by_filename("foreach.cs")

    def test_if_else(self):
        self.check_clean_by_filename("if_else.cs")

    def test_namespace(self):
        self.check_clean_by_filename("namespace.cs")

    def test_class(self):
        self.check_clean_by_filename("class.cs")

    def test_switch_case(self):
        self.check_clean_by_filename("switch_case.cs")

    def check_clean_by_filename(self, filename):
        directory = directory_of_tests + f"\\Main\\WithMistakes\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings([]))
        try:
            linter.analyze_file(path)
        except Exception:
            self.fail(f"Was error in work linter. Filename: {get_link_to_file(directory.replace("\\", "/"), 1)}")
        else:
            msg = f"\n" + "-" * 30 + " FAILED " + "-" * 30 + "\n\nCSharp file: "
            msg += f"{get_link_to_file(directory.replace("\\", "/"), 1)}\n"
            msg += f"Mismatches :\n"
            for mismatch in linter.mismatches:
                msg += str(mismatch) + "\n"
            msg += "-" * 70 + "\n\n"
            self.assertEqual(5, len(linter.mismatches), msg)
        finally:
            linter.mismatches = []