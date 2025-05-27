from django.db import models
from core.base import BaseModel

# 6
class ContactUsModel(BaseModel):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13)
    message = models.TextField()
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

