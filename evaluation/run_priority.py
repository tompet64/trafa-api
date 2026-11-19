"""Run priority deterministic checks offline and emit JSON/JUnit/Markdown reports."""
import argparse
import json
import os
from pathlib import Path
import socket
import time
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from test_shipping_priority import ShippingPriorityTests


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def startTest(self, test):
        self.started = time.monotonic()
        super().startTest(test)

    def stopTest(self, test):
        failures = [(str(t), text) for t, text in self.failures + self.errors if str(t).startswith(str(test).split(' (')[0])]
        skipped = any(t is test for t, _ in self.skipped)
        self.records.append({'id': test.id(), 'status': 'failed' if failures else 'skipped' if skipped else 'passed',
                             'seconds': round(time.monotonic() - self.started, 6),
                             'failures': [text for _, text in failures]})
        super().stopTest(test)


def write_reports(result, directory):
    directory.mkdir(parents=True, exist_ok=True)
    report = {'kind': 'deterministic_code_checks_not_llm_behavior', 'tests': result.records,
              'passed': result.wasSuccessful(), 'count': result.testsRun}
    (directory / 'priority.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    root = ET.Element('testsuite', name='shipping-priority', tests=str(result.testsRun),
                      failures=str(len(result.failures)), errors=str(len(result.errors)), skipped=str(len(result.skipped)))
    for record in result.records:
        case = ET.SubElement(root, 'testcase', name=record['id'], time=str(record['seconds']))
        if record['status'] == 'failed':
            ET.SubElement(case, 'failure').text = '\n'.join(record['failures'])
        elif record['status'] == 'skipped':
            ET.SubElement(case, 'skipped')
    ET.ElementTree(root).write(directory / 'priority.xml', encoding='utf-8', xml_declaration=True)
    text = '## Prioriterade statistikkontroller\n\nKodtester; modellbeteende och levande API har inte verifierats.\n\n| Test | Resultat |\n|---|---|\n'
    text += ''.join(f"| {r['id'].split('.')[-1]} | {r['status']} |\n" for r in result.records)
    (directory / 'priority.md').write_text(text, encoding='utf-8')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a', encoding='utf-8') as handle:
            handle.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path, required=True)
    args = parser.parse_args()
    with patch.object(socket.socket, 'connect', side_effect=AssertionError('Offline test')), \
         patch('socket.create_connection', side_effect=AssertionError('Offline test')), \
         patch('socket.getaddrinfo', side_effect=AssertionError('Offline test')):
        result = unittest.TextTestRunner(verbosity=2, resultclass=RecordedResult).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(ShippingPriorityTests))
    write_reports(result, args.report_dir)
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
