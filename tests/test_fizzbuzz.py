# tests/test_fizzbuzz.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'output'))

from fizzbuzz import fizzbuzz

def test_fizz():
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(6) == "Fizz"

def test_buzz():
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(10) == "Buzz"

def test_fizzbuzz():
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(30) == "FizzBuzz"

def test_other():
    assert fizzbuzz(1) == "1"
    assert fizzbuzz(7) == "7"
