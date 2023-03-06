import pytest

from src.utils import print_hello_world_by_name


class TestHelloWorldByName:
    def test_hello_world(self):
        assert print_hello_world_by_name("Anh") == "Hello World, Anh!"

    def test_hello_world_nullname(self):
        assert print_hello_world_by_name() == "Hello World, SomeOne!"

    def test_hello_world_emptyname(self):
        with pytest.raises(Exception):
            print_hello_world_by_name("")
