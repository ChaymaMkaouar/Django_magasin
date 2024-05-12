from django.db import models
from datetime import date
# Create your models here.
class Categorie (models.Model):
    TYPE_CHOICES=[
        ('hs','Hespéridés'),
        ('fl','Fleuris'),
        ('bs','boisés'),
        ('fg','fougères'),
        ('chyp','chyprés'),
        ('or','oriental'),
        ('ar','aromatiques')]
    name=models.CharField(max_length=50,default='Alimentaire',choices=TYPE_CHOICES)
    def __str__(self) :
        return 'name : '+self.name
class Fournisseur (models.Model):
    nom=models.CharField(max_length=100)
    adresse=models.TextField()
    email=models.EmailField()
    telephone=models.CharField(max_length=8)
    def __str__(self):
        return 'nom : '+self.nom+', adresse: '+self.adresse+', email: '+self.email+', telephone: '+self.telephone
class Produit (models.Model):
    libellé=models.CharField(max_length=100)
    description=models.TextField(default='Non définie')
    prix=models.DecimalField(max_digits=10,decimal_places=3)
    TYPE_CHOICES=[
        ('hs','Hespéridés'),
        ('fl','Fleuris'),
        ('bs','boisés'),
        ('fg','fougères'),
        ('chyp','chyprés'),
        ('or','oriental'),
        ('ar','aromatiques')]
    type=models.CharField(max_length=9,choices=TYPE_CHOICES,default='hs')
    img=models.ImageField(blank=True)
    categorie=models.ForeignKey(Categorie ,on_delete=models.CASCADE,null=True) 
    Fournisseur=models.ForeignKey(Fournisseur,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return 'Libellé: ' + self.libellé + ', Description: ' + self.description + ', Prix: ' + str(self.prix) + ', Type: ' + self.type+', image: '+str(self.img)

class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    produits = models.ManyToManyField('Produit')

    def __str__(self):
        return "date de commande :" + str(self.dateCde) + ",TotalCde :" + str(self.totalCde)

    def calculate_total_price(self):
        total = sum(produit.prix for produit in self.produits.all())
        self.totalCde = total
        self.save()

class Rating(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    valeur = models.IntegerField()  # La valeur de la note, de 1 à 5
    date = models.DateTimeField(auto_now_add=True)  # Date de création du rating

    def __str__(self):
        return f"Rating for {self.produit} - Value: {self.valeur}"
    