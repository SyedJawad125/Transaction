from django.db import models
from utils.helper import TimeStapms


class Product(TimeStapms):
    name = models.CharField(max_length=200)
    description = models.TextField()
    manufacturing_date = models.DateField()

class Images(TimeStapms):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='images/')


