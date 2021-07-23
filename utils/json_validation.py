
def _get_field_type(field_type) -> dict:

    if field_type == 'int':
        return {"type": "number"}
    else:
        return {"type": "string"}

def generate_validator_darft7(template_fields: list) -> dict:

    required_field = []
    fields = dict()

    for field in template_fields:

        if field['is_required']:
            required_field.append(field['name'])

        fields[field['name']] = _get_field_type(field['field_type'])

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            **fields
        },
        "required": required_field
    }
    
    return schema
