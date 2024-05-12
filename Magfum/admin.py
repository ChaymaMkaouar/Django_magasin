from django.contrib import admin

from .models import Produit
admin.site.register(Produit)

from .models import Categorie
admin.site.register(Categorie)

from .models import Fournisseur
admin.site.register(Fournisseur)

from .models import Commande
admin.site.register(Commande)

from .models import Rating
admin.site.register(Rating)