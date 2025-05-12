from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=50)  # Prénom
    last_name = models.CharField(max_length=50)   # Nom
    email = models.EmailField(unique=True)        # Email (doit être unique)
    phone = models.CharField(max_length=20)       # Numéro de téléphone

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
