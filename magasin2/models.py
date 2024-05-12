from django.db import models
from django.db.models.fields.related import ForeignKey
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return self.name    


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE) 
    image=models.ImageField(blank=True)
    date_added = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date_added']  

    def __str__(self):
        return self.title           

class Commande(models.Model):
    items = models.CharField(max_length=300)
    total = models.CharField(max_length=200)
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=300)
    zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']


    def __str__(self):
        return self.nom   
    


class UserPayment(models.Model):
	app_user = models.ForeignKey(User, on_delete=models.CASCADE)
	payment_bool = models.BooleanField(default=False)
	stripe_checkout_id = models.CharField(max_length=500)


@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
	if created:
		UserPayment.objects.create(app_user=instance)

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for {self.product.title}: {self.value}"
    

class Contact(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=70)
    message = models.TextField()

    def __str__(self):
        return f"Nom: {self.nom}, Email: {self.email}, Message: {self.message}"

