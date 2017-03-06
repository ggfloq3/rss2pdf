import json
from django.db import models


# Create your models here.
class ArticleCategory(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True
    )

    def __str__(self):
        return self.title


class Article(models.Model):
    category = models.ForeignKey(ArticleCategory)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    guid = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.title
