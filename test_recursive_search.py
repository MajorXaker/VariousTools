from recursive_search import SearchedDict

sample = {
    "level1-key1": "sample string",
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
            {"key": "sub-dict-5-key12", "of_type": dict},
        ],
    },
    {
        "lookup_value": "mihailovna",
        "expected": [
            {"key": "level1-key8", "of_type": dict},
            {"key": "underlying_dict_key156", "of_type": dict},
        ],
    },
    {
        "lookup_value": "phobos",
        "expected": [],
    },
]

if __name__ == "__main__":
    for test_case in tests:
        data = SearchedDict.initiate_search(sample, test_case["lookup_value"])
        path = [dict(ph) for ph in data.extract()]
        assert test_case["expected"] == path
