from django.db import models
class Categorie(models.Model):
    categorie_name = models.TextField()

    def __str__(self):
        return self.categorie_name

