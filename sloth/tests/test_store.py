# Copyright 2015, 2016 Scott King
#
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
#
import os
import json
import unittest
from sloth.tests.support import TempfileTestCase


class StorageInterfaceTestMixin(object):
    def assertVerifyKeysRaisesMissingAndExtra(self, obj, *, missing, extra):
        from sloth.store import ImproperlyConfigured
        from sloth.store import ImproperlyPopulated
        excinfo = (ImproperlyConfigured, ImproperlyPopulated)
        with self.assertRaises(excinfo) as exc_context:
            obj._verify_keys()
        e = exc_context.exception
        self.assertEqual(e.missing_keys, set(missing))
        self.assertEqual(e.extra_keys, set(extra))

    def assertVerifyKeysPasses(self, obj):
        from sloth.store import ImproperlyConfigured
        from sloth.store import ImproperlyPopulated
        try:
            obj._verify_keys()
        except (ImproperlyConfigured, ImproperlyPopulated) as e:
            self.fail(
                "_verify_keys unexpectedly raised {0!r}".format(e)
            )


class SettingsStoreTestCase(TempfileTestCase, StorageInterfaceTestMixin):
    def make_settings(self):
        from sloth.store import SettingsStore
        return SettingsStore(self.tempfile_path)

    def assertAllPropertiesGet(self, obj):
        obj._store = {key: key for key in obj.expected_keys}
        for key in obj.expected_keys:
            self.assertEqual(getattr(obj, key), key)

    def assertAllPropertiesSet(self, obj):
        obj._store = {key: None for key in obj.expected_keys}
        for key in obj.expected_keys:
            setattr(obj, key, key)
        expected = {key: key for key in obj.expected_keys}
        self.assertEqual(getattr(obj, key), expected)

    def test__verify_keys_passes(self):
        settings = self.make_settings()
        settings._store = dict.fromkeys(settings.expected_keys)
        self.assertVerifyKeysPasses(settings)

    def test__verify_keys_fails_missing(self):
        settings = self.make_settings()
        settings._store = dict.fromkeys(settings.expected_keys)
        settings._store.pop('Age')
        self.assertVerifyKeysRaisesMissingAndExtra(
            settings, missing=['Age'], extra=[])

    def test__verify_keys_fails_extra(self):
        settings = self.make_settings()
        settings._store = dict.fromkeys(settings.expected_keys)
        settings._store['UnexpectedKey'] = 'Unexpected'
        self.assertVerifyKeysRaisesMissingAndExtra(
            settings, missing=[], extra=['UnexpectedKey'])


class LogEntryTestCase(unittest.TestCase, StorageInterfaceTestMixin):
    def make_entry(self):
        from sloth.store import LogEntry
        return LogEntry()

    def assertAllPropertiesGet(self, obj):
        obj._store = {key: key for key in obj.expected_keys}
        for key in obj.expected_keys:
            self.assertEqual(getattr(obj, key), key)

    def assertAllPropertiesSet(self, obj):
        obj._store = {key: None for key in obj.expected_keys}
        for key in obj.expected_keys:
            setattr(obj, key, key)
        expected = {key: key for key in obj.expected_keys}
        self.assertEqual(getattr(obj, key), expected)

    def test__verify_keys_passes(self):
        entry = self.make_entry()
        entry._store = dict.fromkeys(entry.expected_keys)
        self.assertVerifyKeysPasses(entry)

    def test__verify_keys_fails_missing(self):
        entry = self.make_entry()
        entry._store = dict.fromkeys(entry.expected_keys)
        entry._store.pop('Type')
        self.assertVerifyKeysRaisesMissingAndExtra(
            entry, missing=['Type'], extra=[])

    def test__verify_keys_fails_extra(self):
        entry = self.make_entry()
        entry._store = dict.fromkeys(entry.expected_keys)
        entry._store['UnexpectedKey'] = 'Unexpected'
        self.assertVerifyKeysRaisesMissingAndExtra(
            entry, missing=[], extra=['UnexpectedKey'])


class LogsStoreTestCase(TempfileTestCase):
    def make_store(self):
        from sloth.store import LogsStore
        return LogsStore(self.tempfile_path)

    def make_populated_entry(self):
        from sloth.store import LogEntry
        return LogEntry(dict.fromkeys(LogEntry.expected_keys))

    def test_append_entry(self):
        store = self.make_store()
        entry = self.make_populated_entry()
        store.append_entry(entry)
        with self.open_tempfile('r') as fp:
            struct = json.load(fp)
        self.assertEqual(entry._store, struct)

    def test_append_entry_appends_not_overwrites(self):
        with self.open_tempfile('w') as fp:
            fp.write('First line\n')
        store = self.make_store()
        entry = self.make_populated_entry()
        store.append_entry(entry)
        with self.open_tempfile('r') as fp:
            line1, line2 = fp
        self.assertEqual(line1, 'First line\n')
        struct = json.loads(line2)
        self.assertEqual(entry._store, struct)

    def test_load_last_entry(self):
        struct = self.make_populated_entry()._store
        serialized = json.dumps(struct)
        with self.open_tempfile('w') as fp:
            fp.write(serialized + '\n')
        store = self.make_store()
        entry = store.load_last_entry()
        self.assertEqual(entry._store, struct)

    def test_load_last_entry_loads_only_last(self):
        struct = self.make_populated_entry()._store
        serialized = json.dumps(struct)
        with self.open_tempfile('w') as fp:
            fp.write('First line\n')
            fp.write(serialized + '\n')
        store = self.make_store()
        entry = store.load_last_entry()
        self.assertEqual(entry._store, struct)

    def test_load_last_entry_returns_none_with_empty_file(self):
        store = self.make_store()
        result = store.load_last_entry()
        self.assertIsNone(result)

    def test_load_last_entry_returns_none_for_nonexistant_file(self):
        store = self.make_store()
        os.remove(self.tempfile_path)
        try:
            result = store.load_last_entry()
            self.assertIsNone(result)
        finally:
            # Create the file again so tearDown doesn't break
            with open(self.tempfile_path, 'w'):
                pass
