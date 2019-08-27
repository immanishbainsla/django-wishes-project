from django.db import models
# from django.contrib.auth import models as authmodels
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

# class CustomerModel(models.Model): # authmodels.User, authmodels.PermissionsMixin
#     customer = models.OneToOneField(User, related_name='customer', on_delete=models.CASCADE)
#     def __str__(self):
#         return self.customer.username


class UserWishListModel(models.Model):
    user = models.ForeignKey(User, related_name='user_wishes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, blank=False)
    description  = models.TextField(blank=True, help_text='Describe your Wish here.')
    date_added = models.DateTimeField(auto_now_add=True)

    # def save(self):
    #     # self.slug = slugify(self.title)
    #     self.pk = pk
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title[:25] + '...'

    def get_absolute_url(self):
        return reverse('wishlist:wishlist')




class ContactModel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(blank=False)
    query = models.TextField(blank=False, help_text='Describe your Query here.')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')
