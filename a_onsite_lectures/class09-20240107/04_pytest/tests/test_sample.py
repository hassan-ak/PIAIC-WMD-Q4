import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sample import func, func1


def test_answer():
    assert func(3) == 5


def test_answer1():
    assert func1(3) == 4
