import sys

import pytest
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from blockNode import main


class TestSuite:

    @pytest.mark.args
    def test_1(self):
        try:
            main()
        except Exception as e:
            assert str(e) == '3 Args should be provided'

    @pytest.mark.args
    def test_2(self):
        try:
            sys.argv = [1, 2, 3, 4, 5]
            main()
        except Exception as e:
            assert str(e) == '3 Args should be provided'

    @pytest.mark.values
    def test_3(self):
        try:
            sys.argv = [None, "ftp://", 2, 3]
            main()
        except Exception as e:
            assert str(e) == 'Invalid URL'

    @pytest.mark.values
    def test_4(self):
        try:
            sys.argv = [None, "https://google.com", "https://google.com", 3]
            main()
        except Exception as e:
            assert str(e) == 'PostgreSQL is the supported DB. Use the provided connection string'

    @pytest.mark.values
    def test_5(self):
        try:
            sys.argv = [None, "https://google.com", "postgresql://user:password@localhost:5432/database", 3]
            main()
        except Exception as e:
            assert str(e) == "'int' object has no attribute 'split'"

    @pytest.mark.values
    def test_6(self):
        try:
            sys.argv = [None, "https://google.com", "postgresql://user:password@localhost:5432/database", {5:5}]
            main()
        except Exception as e:
            assert str(e) == "'dict' object has no attribute 'split'"


    @pytest.mark.values
    def test_7(self):
        try:
            sys.argv = [None, "https://google.com", "postgresql://user:password@localhost:5432/database", []]
            main()
        except Exception as e:
            assert str(e) == "'list' object has no attribute 'split'"

    @pytest.mark.values
    def test_7(self):
        try:
            sys.argv = [None, "https://google.com", "postgresql://user:password@localhost:5432/database", "https://google.com"]
            main()
        except Exception as e:
            assert str(e) == "invalid literal for int() with base 10: 'https://google.com'"
