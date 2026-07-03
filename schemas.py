from marshmallow import Schema, fields,validate 

class URLSchema(Schema):
    url=fields.Str(
        required=True,
        validate=validate.Length(min=1,max=255)
    )

class URLResponseSchema(Schema):
    short_code=fields.Str()
    original_url=fields.Str()
    status=fields.Str()
                        