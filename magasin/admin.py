from django.contrib import admin

# Register your models here.
from .models import Produit
from .models import Categorie
from .models import Fournisseur
from .models import ProduitNC
from .models import Commande
from .models import Rating

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Fournisseur)
admin.site.register(ProduitNC)
admin.site.register(Commande)
admin.site.register(Rating)
