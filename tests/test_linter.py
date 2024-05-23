import unittest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir + '/Scripts')

from Scripts.Linter import Linter
from Scripts.Settings import Settings
from Scripts.exceptions import ErrorInLinterTest


def get_link_to_file(file=None, line=None):
    """ Print a link in PyCharm to a line in file. Defaults to line where this function was called. """
    return f"file:///{file}"


directory_of_tests = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TestFiles\\Linter")

class TestSimple(unittest.TestCase):

    def test_offsets_in_block(self):
        self._test("test_offsets_in_block.cs")

    def _test(self, filename):
        directory = directory_of_tests + f"\\Simple\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings())
        try:
            linter._analyze_file(path)
        except Exception as e:
            raise ErrorInLinterTest(get_link_to_file(directory.replace("\\", "/"), 1)) from e
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


class TestCleanFiles(unittest.TestCase):
    def test_clean_code_1(self):
        self._test("test_clean_1.cs")

    def test_clean_code_2_method_1(self):
        self._test("test_clean_2_method_1.cs")

    def test_clean_code_2_method_2(self):
        self._test("test_clean_2_method_2.cs")

    def test_clean_code_2_method_3(self):
        self._test("test_clean_2_method_3.cs")

    def test_clean_code_2(self):
        self._test("test_clean_2.cs")

    def test_clean_code_3(self):
        self._test("test_clean_3.cs")

    def _test(self, filename):
        directory = directory_of_tests + f"\\CleanFiles\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings())
        try:
            linter._analyze_file(path)
        except Exception as e:
            raise ErrorInLinterTest(get_link_to_file(directory.replace("\\", "/"), 1)) from e
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
        self._test("while.cs")

    def test_try_catch_finally(self):
        self._test("try_catch_finally.cs")

    def test_do_while(self):
        self._test("do_while.cs")

    def test_for(self):
        self._test("for.cs")

    def test_foreach(self):
        self._test("foreach.cs")

    def test_if_else(self):
        self._test("if_else.cs")

    def test_namespace(self):
        self._test("namespace.cs")

    def test_class(self):
        self._test("class.cs")

    def test_switch_case(self):
        self._test("switch_case.cs")

    def test_new(self):
        self._test("new.cs")

    def test_get_set(self):
        self._test("get_set.cs")

    def _test(self, filename):
        directory = directory_of_tests + f"\\Main\\Clean\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings())
        try:
            linter._analyze_file(path)
        except Exception as e:
            raise ErrorInLinterTest(get_link_to_file(directory.replace("\\", "/"), 1)) from e
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
        self._test("while.cs")

    def test_try_catch_finally(self):
        self._test("try_catch_finally.cs")

    def test_do_while(self):
        self._test("do_while.cs")

    def test_for(self):
        self._test("for.cs")

    def test_foreach(self):
        self._test("foreach.cs")

    def test_if_else(self):
        self._test("if_else.cs")

    def test_namespace(self):
        self._test("namespace.cs")

    def test_class(self):
        self._test("class.cs")

    def test_switch_case(self):
        self._test("switch_case.cs")

    def test_get_set(self):
        self._test("get_set.cs")

    def _test(self, filename):
        directory = directory_of_tests + f"\\Main\\WithMistakes\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(Settings())
        try:
            linter._analyze_file(path)
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


class TestTabsAndSpaces(unittest.TestCase):

    def test_space(self):
        settings = Settings()
        settings.indent_style.value = "space"
        self._test("Spaces.cs", settings)


    def test_tab(self):
        settings = Settings()
        settings.indent_style.value = "tab"
        self._test("Tabs.cs", settings)

    def _test(self, filename: str, settings: Settings):
        directory = directory_of_tests + f"\\Whitespaces\\{filename}"
        path = os.path.join(directory, directory)
        linter = Linter(settings)
        try:
            linter._analyze_file(path)
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
