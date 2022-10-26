def jsonise(data):
    import json
    json_object = json.dumps(data)
    return json.loads(json_object)
