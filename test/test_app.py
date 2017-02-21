from bot import app
from unittest import TestCase
from unittest.mock import Mock, patch
from .util import patch_env


class CanonicalRedirectTest(TestCase):
    @patch_env({})
    def test_not_configured(self):
        self.assertIsNone(app.redirect_canonical_host())

    @patch_env({ 'CANONICAL_HOST': 'https://foo.com' })
    def test_wrong_host(self):
        with patch.object(app, 'request', Mock(url='https://bar.com/thing?x=1')):
            r = app.redirect_canonical_host()
            self.assertEqual(r.location, 'https://foo.com/thing?x=1')
            self.assertEqual(r.status_code, 303)

    @patch_env({ 'CANONICAL_HOST': 'https://foo.com' })
    def test_wrong_proto(self):
        with patch.object(app, 'request', Mock(url='http://foo.com/thing?x=1')):
            r = app.redirect_canonical_host()
            self.assertEqual(r.location, 'https://foo.com/thing?x=1')
            self.assertEqual(r.status_code, 303)

    @patch_env({ 'CANONICAL_HOST': 'https://www.foo.com' })
    def test_missing_www(self):
        with patch.object(app, 'request', Mock(url='https://foo.com/thing?x=1')):
            r = app.redirect_canonical_host()
            self.assertEqual(r.location, 'https://www.foo.com/thing?x=1')
            self.assertEqual(r.status_code, 303)

    @patch_env({ 'CANONICAL_HOST': 'https://www.foo.com' })
    def test_exempt_health(self):
        with patch.object(app, 'request', Mock(url='https://foo.com/health')):
            self.assertIsNone(app.redirect_canonical_host())
