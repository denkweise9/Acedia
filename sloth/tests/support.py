import os
import tempfile
import unittest


class TempfileTestCase(unittest.TestCase):
    def setUp(self):
        ignored, file_path = tempfile.mkstemp(prefix='sloth-unittest-tmp.')
        self.tempfile_path = file_path
        super(TempfileTestCase, self).setUp()

    def tearDown(self):
        super(TempfileTestCase, self).tearDown()
        os.remove(self.tempfile_path)

    def open_tempfile(self, mode):
        return open(self.tempfile_path, mode, encoding='utf-8')
