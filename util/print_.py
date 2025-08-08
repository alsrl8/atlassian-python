import json


def pretty_json(json_data: dict):
    print(json.dumps(json_data, indent=4, sort_keys=True, ensure_ascii=False))
