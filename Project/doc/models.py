from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class LoggedUser(models.Model):
    user = models.ForeignKey(User, primary_key=True,on_delete=models.CASCADE,)

    def __unicode__(self):
        return self.user.username

    def login_user(sender, request, user, **kwargs):
        LoggedUser(user=user).save()

    def logout_user(sender, request, user, **kwargs):
        try:
            u = LoggedUser.objects.get(user=user)
            u.delete()
        except LoggedUser.DoesNotExist:
            pass

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)

class Post(models.Model):
    Document = models.TextField(max_length=8000)
    Title = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE,)