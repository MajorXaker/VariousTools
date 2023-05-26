from typing import List, Iterable

from pydantic import BaseModel

# the task is to find string which contains "substring" in complex parsed json

sample = {
    "level1-key1": 'sample string',
    "level1-key0": None,
    "level1-key3": [
        {
            "sub-dict-5-key1": "aaa",
            "sub-dict-5-key9": False,
            "sub-dict-5-key22": "string",
            221: "string_in_int_key",
            "sub-dict-5-key12": "not_the_droids_you_re_looking_for",

        },
        {
            "sub-dict-5-key1": "aaa",
            "sub-dict-5-key9": False,
            "sub-dict-5-key22": "string",
            221: "string_in_int_key",
            "sub-dict-5-key12": "substring",

        },
    ],
    "level1-key8": {
        "underlying_dict_key1": 5,
        "underlying_dict_key71": "chubby",
        "underlying_dict_key156": "eleonor mihailovna",

    },
}

tests = [
    {
        "lookup_value": "substring",
        "expected": [
            {"key": "level1-key3", "of_type": dict},
            {"key": "1", "of_type": list},
            {"key": "sub-dict-5-key12", "of_type": dict}
        ],
    },
    {
        "lookup_value": "mihailovna",
        "expected": [
            {"key": "level1-key8", "of_type": dict},
            {"key": "underlying_dict_key156", "of_type": dict}
        ],
    },
    {
        "lookup_value": "phobos",
        "expected": [],
    },
]



class PathEntry(BaseModel):
    key: str | float | int
    of_type: type


class SearchedItem(BaseModel):
    path_to_self: List[PathEntry]
    lookup: str
    data: Iterable
    self_type: type
    resulting_path: List[PathEntry] | None

    @classmethod
    def initiate_search(cls, data):
        raise NotImplementedError

    def check_string(self, string):
        return self.lookup in string

    def generate(self):
        raise NotImplementedError

    def extract(self):
        resulting_path = []

        for key, val in self.generate():
            path_to_item = self.path_to_self.copy()
            path_to_item.append(PathEntry(key=key, of_type=self.self_type))

            entry_type = type(val)
            if entry_type == str:
                is_found = self.check_string(val)
                if is_found:
                    resulting_path = path_to_item
            elif entry_type in (list, tuple):
                resulting_path = SearchedList(
                    path_to_self=path_to_item,
                    lookup=self.lookup,
                    data=val,
                    self_type=list,
                ).extract()
            elif entry_type == dict:
                resulting_path = SearchedDict(
                    path_to_self=path_to_item,
                    lookup=self.lookup,
                    data=val,
                    self_type=dict,
                ).extract()
            elif entry_type == set:
                raise ValueError("Sets are not indexable!")

            if resulting_path:
                break

        return resulting_path


class SearchedList(SearchedItem):
    data: list
    self_type = list

    def generate(self):
        return enumerate(self.data)

    @classmethod
    def initiate_search(cls, data: list, lookup: str):
        return cls(
            path_to_self=[],
            lookup=lookup,
            data=data,
            self_type=list,
        )


class SearchedDict(SearchedItem):
    data: dict
    self_type = dict

    def generate(self):
        for key, value in self.data.items():
            yield key, value

    @classmethod
    def initiate_search(cls, data: dict, lookup: str):
        return cls(
            path_to_self=[],
            lookup=lookup,
            data=data,
            self_type=dict,
        )


for test_case in tests:
    data = SearchedDict.initiate_search(sample, test_case['lookup_value'])
    path = [dict(ph) for ph in data.extract()]
    assert test_case["expected"] == path
