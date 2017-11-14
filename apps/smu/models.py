from __future__ import unicode_literals
import re
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # check users name
        if len(postData['first_name']) < 3:
            errors["first_name"] = "User first name should be more than 3 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "User last name should be more than 3 characters"
        # check email field for valid email
        if not "email" in errors and not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "invalid email"
        # if email is valid check db for existing email
        else:
            if len(self.filter(email=postData['email'])) > 1:
                errors['email'] = "email already in use"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "User: --{}".format(self.first_name)