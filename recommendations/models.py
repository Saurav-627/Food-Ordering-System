from django.db import models
from django.conf import settings

class RecommendationCache(models.Model):
    key = models.CharField(max_length=100, unique=True) # e.g., 'item_similarity', 'co_occurrence'
    data = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
