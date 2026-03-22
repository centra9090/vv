import sys
import os

# Ensure src/ is discoverable as python package root for tests
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
