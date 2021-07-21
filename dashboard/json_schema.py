default_information =  \
    {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "gender": {"enum": ["m", "f", "o"]},
        "required": ["first_name", "last_name", "gender"]
    }

template_field = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "title": {"type": "string"},
                "field_type": {"enum": ["str", "int", "date", "datetime", "location"]},
                "is_required": {"type": "boolean"},
                "max_length": {"type": "number"}
            },
            "required": ["name", "title", "field_type", "is_required"]
        }

    }
