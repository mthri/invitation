create_payment = \
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "required": ["amount", "description"],
        "amount": {"type": "number"},
        "description": {"type": "string"},
    }