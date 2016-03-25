import os
import json


class ImproperlyConfigured(Exception):

    def __init__(self, file_path, missing_keys, extra_keys):
        self.file_path = file_path
        self.missing_keys = missing_keys
        self.extra_keys = extra_keys

    def __repr__(self):
        fmt = (
            '<ImproperlyConfigured(file_path={file_path}, '
            'missing_keys={missing_keys}, extra_keys={extra_keys})>'
        )
        return fmt.format(
            file_path=self.file_path,
            missing_keys=self.missing_keys,
            extra_keys=self.extra_keys
        )
    __str__ = __repr__


class ImproperlyPopulated(Exception):

    def __init__(self, missing_keys, extra_keys):
        self.missing_keys = missing_keys
        self.extra_keys = extra_keys

    def __repr__(self):
        fmt = (
            '<ImproperlyPopulated(missing_keys={missing_keys}, '
            'extra_keys={extra_keys})>'
        )
        return fmt.format(
            missing_keys=self.missing_keys,
            extra_keys=self.extra_keys
        )
    __str__ = __repr__


def _storage_property(key):

    def getter(self):
        return self._store[key]

    def setter(self, value):
        self._store[key] = value
    return property(getter, setter)


class SettingsStore(object):
    """
    Manage the settings file.

    Provide the full file path to the settings file in the constructor.
    Load settings from the file with the load method.
    Use the attributes to get and set settings options.
    Save the updated settings with the commit() method.
    """
    age = _storage_property("Age")
    agility = _storage_property("Agility")
    charisma = _storage_property("Charisma")
    defense = _storage_property("Defense")
    endurance = _storage_property("Endurance")
    goal = _storage_property("Goal")
    height = _storage_property("Height")
    intelligence = _storage_property("Intelligence")
    name = _storage_property("Name")
    strength = _storage_property("Strength")
    sex = _storage_property("Sex")
    measuring_type = _storage_property("Type")
    weight = _storage_property("Weight")
    xp = _storage_property("XP")

    expected_keys = frozenset([
        "Age", "Agility", "Charisma", "Defense", "Endurance", "Goal",
        "Height", "Intelligence", "Name", "Strength", "Sex", "Type",
        "Weight", "XP"
    ])

    def __init__(self, file_path):
        self._file_path = file_path
        self._store = {}

    def load(self):
        """
        Load the settings file at ``file_path`` and populate the
        instance.
        """
        with open(self._file_path, encoding='utf-8') as infile:
            self._store = json.load(infile)
        self._verify_keys()

    def commit(self):
        """
        Save the settings in the file if the stored keys match the
        expected keys, or raise `ImproperlyConfigured`.
        """
        self._verify_keys()
        # Convert before trunacting the file to avoid wiping data
        # if the serialization fails.
        tosave = json.dumps(self._store, sort_keys=True)
        with open(self._file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(tosave)

    def _verify_keys(self):
        missing_keys = self.expected_keys.difference(self._store.keys())
        extra_keys = set(self._store.keys()).difference(self.expected_keys)
        if missing_keys or extra_keys:
            raise ImproperlyConfigured(
                file_path=self._file_path,
                missing_keys=missing_keys,
                extra_keys=extra_keys
            )


class LogsStore(object):
    """
    Manage the log file.

    Provide the full file path to the log file in the constructor.
    """
    def __init__(self, file_path):
        self._file_path = file_path

    def load_last_entry(self):
        """
        Load the last log entry in the log file and return the
        associated `LogEntry` object, or None if there are no entries.
        """
        line = None
        if not os.path.exists(self._file_path):
            return None
        with open(self._file_path, "r", encoding="utf-8") as infile:
            for line in infile:
                pass
        if line is None:
            return None
        else:
            return LogEntry(json.loads(line))

    def check_log(self):
        total_points = []
        losing_points = []
        each = None
        if not os.path.exists(self._file_path):
            return
        with open(self._file_path, "r", encoding="utf-8") as infile:
            for each in infile:
                each_line = json.loads(each)
                total_points.append(each_line["Points"])
                if each_line["Exercise"] == "DETERIORATE":
                    losing_points.append(each_line["Total"])
        if each is None:
            return
        else:
            return (total_points, losing_points)

    def append_entry(self, entry):
        """
        Serialize the `LogEntry` object and append it to the log.
        """
        entry._verify_keys()
        serialized = json.dumps(entry._store, sort_keys=True)
        with open(self._file_path, "a", encoding="utf-8") as outfile:
            outfile.write(serialized + "\n")


class LogEntry(object):
    average = _storage_property("Average")
    date = _storage_property("Date")
    distance = _storage_property("Distance")
    exercise = _storage_property("Exercise")
    measuring = _storage_property("Measuring")
    points = _storage_property("Points")
    total = _storage_property("Total")
    utc = _storage_property("UTC")

    expected_keys = frozenset([
        "Average", "Date", "Distance", "Exercise",
        "Measuring", "Points", "Total", "UTC"
    ])

    def __init__(self, _store=None):
        self._store = _store or {}

    def _verify_keys(self):
        missing_keys = self.expected_keys.difference(self._store.keys())
        extra_keys = set(self._store.keys()).difference(self.expected_keys)
        if missing_keys or extra_keys:
            raise ImproperlyPopulated(
                missing_keys=missing_keys,
                extra_keys=extra_keys
            )
