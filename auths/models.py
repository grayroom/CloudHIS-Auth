from django.db import models


class User(models.Model):
    id = models.BigAutoField(help_text="User ID", primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username
