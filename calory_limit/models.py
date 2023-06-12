from django.db import models
from users.models import User

# Create your models here.
class CaloryLimit(models.Model):
    calory_limit = models.FloatField(null=False, blank=False)
    description = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    exceeded_maximum = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    present_calory_amount = models.FloatField(null=True, default=0)

    class Meta:
        ordering = ('created_at',)
        verbose_name_plural = 'Calory Limit'

    def __str__(self) -> str:
        return self.description
    

    def save(self, *args, **kwargs):
        if self.present_calory_amount > self.calory_limit:
            self.exceeded_maximum = True
        else:
            self.exceeded_maximum = False

        super().save(*args, **kwargs)


