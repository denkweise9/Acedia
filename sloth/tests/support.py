# This file is part of Sloth.
#
# Sloth is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sloth is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Affero GNU General Public License for more details.
#
# You should have received a copy of the Affero GNU General Public License
# along with Sloth.  If not, see <http://www.gnu.org/licenses/>.
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
