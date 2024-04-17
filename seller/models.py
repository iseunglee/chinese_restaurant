from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user = 상품 판매자, 어떤 판매자가 어떤 상품을 올렸는지 적용
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField()
    image_url = models.URLField()
    