from ninja import ModelSchema, Schema
from django.contrib.auth.models import User

class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['username','password']


class BookingSchema(Schema):
    class Config:
        model = User
        model_fields = ['username','password']
