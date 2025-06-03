from django.db import models
from users.models import CustomUser
from courses.models import Course

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)  # مثل "Credit Card" أو "PayPal"
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')

    def __str__(self):
        return f"Payment {self.id} for {self.user} - {self.status}"
