from django.db import models

class Ferme(models.Model):
    name = models.CharField(max_length=56, unique=True)
    address = models.CharField(max_length=1024)
    capital = models.DecimalField(max_digits=16,decimal_places=2)

    def __str__(self) -> str:
        return self.name
