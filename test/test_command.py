from bot import command
import flask
import os
from unittest import TestCase
from unittest.mock import Mock, patch
from .util import patch_env


class RunTest(TestCase):
    @patch_env({
        'SLACK_VERIFICATION_TOKEN': 'foo'
    })
    def test_missing_token(self):
        with patch.object(flask, 'request', Mock(form={})):
            self.assertEqual(('Forbidden', 403), command.run())

    @patch_env({
        'SLACK_VERIFICATION_TOKEN': 'foo'
    })
    def test_wrong_token(self):
        with patch.object(flask, 'request', Mock(form={'token': 'xxx'})):
            self.assertEqual(('Forbidden', 403), command.run())

    @patch_env({
        'SLACK_VERIFICATION_TOKEN': 'foo'
    })
    def test_missing_text(self):
        with patch.object(flask, 'request', Mock(form={'token': 'foo'})):
            self.assertEqual(('Bad request', 400), command.run())


class ParseTest(TestCase):
    def test_trimmed(self):
        with patch.object(flask, 'request', Mock(form={'text': '  foo bar '})):
            self.assertEqual(('foo', ['bar']), command.parse())

    def test_lowercase(self):
        with patch.object(flask, 'request', Mock(form={'text': '  FOO BAR '})):
            self.assertEqual(('foo', ['BAR']), command.parse())
