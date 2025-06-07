from django.db import models
from datetime import datetime   
from django.conf import settings

# Create your models here.


class Pizza(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.PositiveBigIntegerField()
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pizzas/')

    def __str__(self):
        return self.name 

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    count = models.PositiveBigIntegerField(default=0)
    total = models.PositiveBigIntegerField(editable=False)

    def save(self, *args, **kwargs):
        if not self.order_number:
            today = datetime.today().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=today).order_by('-order_number').first()
            next_order = 1001 if not last_order else int(last_order.order_number.split('-')[-1]) + 1
            self.order_number = f"{today}-{next_order}"
            self.total = self.pizza.price * self.count
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.pizza.name}"

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.pizza.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.pizza.name} in {self.user.username}'s Cart"