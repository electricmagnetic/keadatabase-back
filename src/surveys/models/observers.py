from django.db import models

class Observer(models.Model):
    """ Observer details for a particular survey """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name
