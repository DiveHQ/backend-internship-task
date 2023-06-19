

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    calorie_perday = fields.Int(required=True)
