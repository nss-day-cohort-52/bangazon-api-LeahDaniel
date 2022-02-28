from django.db import models
from django.contrib.auth.models import User


class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} liked by {self.user.get_full_name()}'
