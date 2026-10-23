"""Run code tests with network blocked. Behavioral grading is deliberately separate."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
SKILL=Path(os.environ.get('TRAFA_SKILL_ROOT',HERE.parent))
sys.path[:0]=[str(SKILL/'scripts'),str(HERE)]
suite=unittest.TestSuite()
suite.addTests(unittest.defaultTestLoader.discover(str(SKILL/'scripts'),pattern='test_*.py'))
suite.addTests(unittest.defaultTestLoader.discover(str(HERE),pattern='test_*.py',top_level_dir=str(HERE)))
# Block Python child processes as well as this process. This is a test guard,
# not an operating-system sandbox for arbitrary native programs.
with tempfile.TemporaryDirectory(prefix='trafa-offline-') as directory:
    Path(directory,'sitecustomize.py').write_text(
        "import socket\n"
        "def _blocked(*args, **kwargs):\n"
        "    raise AssertionError('Offline test: network blocked')\n"
        "socket.socket.connect = _blocked\n"
        "socket.create_connection = _blocked\n"
        "socket.getaddrinfo = _blocked\n", encoding='utf-8')
    pythonpath=directory+os.pathsep+os.environ.get('PYTHONPATH','')
    with patch.dict(os.environ,{'PYTHONPATH':pythonpath}), \
         patch('socket.socket.connect',side_effect=AssertionError('Offline test: network blocked')), \
         patch('socket.create_connection',side_effect=AssertionError('Offline test: network blocked')), \
         patch('socket.getaddrinfo',side_effect=AssertionError('Offline test: DNS blocked')):
        result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
