"""
Example test file - demonstrates testing framework setup
This file can be used as a template for writing actual tests
"""
import pytest


def test_example_passing():
    """Example of a passing test"""
    assert 1 + 1 == 2


def test_example_with_fixture(tmp_path):
    """Example using pytest fixtures"""
    # tmp_path is a built-in pytest fixture
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, tests!")
    
    assert test_file.read_text() == "Hello, tests!"


@pytest.mark.skip(reason="Example of skipped test")
def test_example_skipped():
    """Example of a test that's intentionally skipped"""
    assert False


class TestExampleClass:
    """Example test class"""
    
    def test_method_one(self):
        """Test methods can be organized in classes"""
        assert True
    
    def test_method_two(self):
        """Another test in the same class"""
        x = "hello"
        assert "h" in x


# Uncomment to test actual game components:
# from game.entities import Planet
# 
# def test_planet_creation():
#     """Test creating a planet"""
#     planet = Planet(100, 100, 20, owner="Player")
#     assert planet.x == 100
#     assert planet.y == 100
#     assert planet.radius == 20
#     assert planet.owner == "Player"

