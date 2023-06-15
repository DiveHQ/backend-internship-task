from django.db import models

class User(models.Model):

    username=models.CharField(max_length=200)
    email=models.EmailField( max_length=254)
    password = models.CharField(max_length=50)
    daily_Cola = models.IntegerField()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})
