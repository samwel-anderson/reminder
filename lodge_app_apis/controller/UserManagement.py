from lodge_app.models import *
from django.contrib.auth import authenticate


class UserManagement:
    def login(request, userSchema):
        try:
            user = authenticate(username = userSchema.username,
            password = userSchema.password)
            if user:
                content = {
                    "username": user.username,
                    "email" : user.email
                }
                return content
            else:
                return {
                    "message": "Incorrect username or password",
                    "code": 2200
                }
        except Exception as e:
            print(e)
            return {
                "message": "Unknown error occured while rendering your request",
                "code": 2200
            }
