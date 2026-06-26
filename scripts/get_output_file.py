# scripts/get_output_file.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from spec_parser import parse_spec

spec_file = sys.argv[1]
spec = parse_spec(spec_file)
print(spec["output_file"])
