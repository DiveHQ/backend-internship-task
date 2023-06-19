
from marshmallow import Schema, fields

class EntrySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    text = fields.Str(required=True)
    is_satisfied = fields.Bool()
    calories = fields.Int()
