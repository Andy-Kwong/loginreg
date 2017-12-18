from __future__ import unicode_literals

from django.db import models
from django.contrib import messages

import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class LrManager(models.Manager):
    def validator(self, postData):
        errors = []
        for field, value in postData.iteritems():
            if len(postData["password"]) < 8:
                errors.append("Password must be greater than 8 characters!")

            if postData["cPassword"] != postData["password"]:
                errors.append("Passwords did not match!")

            if not re.match(NAME_REGEX, postData['fName']) or not re.match(NAME_REGEX, postData['lName']):
                errors.append("Name field must only contain letters")

            if len(postData["fName"]) < 2:
                errors.append("First name field must be greater than 2 characters!")

            if len(postData["lName"]) < 2:
                errors.append("Last name field must be greater than 2 characters!")

            if not "email" in errors and not re.match(EMAIL_REGEX, postData['email']):
                errors.append("Email is not valid")

            else:
                if len(self.filter(email=postData["email"])) > 0:
                    errors.append("Email already registered")

            if not errors:
                hashed = bcrypt.hashpw((postData['password']. encode()), bcrypt.gensalt(5))

                new_user = self.create(
                    first_name = postData['fName'],
                    last_name = postData['lName'],
                    email = postData['email'],
                    password = hashed
                )
                return new_user

            return errors

    def login(self, postData):
        errors = []
        if len(self.filter(email = postData["email"])) > 0:
            user = self.filter(email = postData["email"])[0]
            if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
                errors.append("email/password does not match records!")

        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.first_name, self.last_name, self.email, self.password)

    objects = LrManager()
