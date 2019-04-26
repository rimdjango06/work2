from django.db import models

# Create your models here.
from django.db import models

class Item(models.Model):
	name = models.CharField(max_length=20)
	desc = models.TextField(blank=True)
	photo = models.ImageField()  # blank=True 지정하지 않은 경우
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
	return self.title
