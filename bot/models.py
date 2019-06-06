from django.db import models

class Sentence(models.Model):

    sentence = models.CharField(max_length=500, null=False)

    tag = models.CharField(max_length=50)



    def __str__(self):

        return self.sentence
