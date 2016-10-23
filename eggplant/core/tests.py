from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from eggplant.core.utils import generate_upload_path

from .context_processors import coop_vars


class UtilsTestCase(TestCase):

    def test_generate_upload_path(self):
        actual = generate_upload_path(None, 'some file.jpeg', None)
        self.assertRegex(actual, r'^[a-z0-9]{32}\.jpeg$')

    def test_generate_upload_path_with_dir(self):
        actual = generate_upload_path(None, 'some file.jpeg', 'somedir')
        self.assertRegex(actual, r'^somedir/[a-z0-9]{32}\.jpeg$')

    def test_context_processor(self):
        rf = RequestFactory()
        context = coop_vars(rf.get("/en/"))
        self.assertIn('LANGUAGE_CHOOSER', context)
        for lang_code, __ in settings.LANGUAGES:
            self.assertIn(lang_code, context['LANGUAGE_CHOOSER'])
