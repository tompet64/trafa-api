"""Reporting must preserve failures, including failed subtests."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import run_priority


class ReportingTests(unittest.TestCase):
    def test_failed_subtest_is_not_reported_as_passed(self):
        class Example(unittest.TestCase):
            def runTest(self):
                with self.subTest(year=2025):
                    self.assertEqual(1, 2)
        result = unittest.TextTestRunner(stream=io.StringIO(), resultclass=run_priority.RecordedResult).run(Example())
        self.assertFalse(result.wasSuccessful())
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ', {}, clear=True):
            run_priority.write_reports(result, Path(directory))
            report = json.loads(Path(directory, 'priority.json').read_text(encoding='utf-8'))
            self.assertFalse(report['passed'])
            self.assertEqual(report['tests'][0]['status'], 'failed')
            self.assertIsNotNone(ET.parse(Path(directory, 'priority.xml')).find('.//failure'))

    def test_empty_scope_does_not_look_like_behavior_verification(self):
        result = unittest.TextTestRunner(stream=io.StringIO(), resultclass=run_priority.RecordedResult).run(unittest.TestSuite())
        with tempfile.TemporaryDirectory() as directory, patch.dict('os.environ', {}, clear=True):
            run_priority.write_reports(result, Path(directory))
            report = json.loads(Path(directory, 'priority.json').read_text(encoding='utf-8'))
            self.assertEqual(report['kind'], 'deterministic_code_checks_not_llm_behavior')
            self.assertEqual(report['count'], 0)
