from django.db import models


class ShortLink(models.Model):
    original_url = models.URLField(max_length=2000, unique=True)
    code = models.CharField(max_length=8, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code + ' -> ' + self.original_url