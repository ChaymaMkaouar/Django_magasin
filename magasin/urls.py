from django.urls import path ,include
#from django.conf.urls import url
from . import views
from .views import CategoryAPIView,ProductAPIView
from .views import ModifierProduit
from .views import SupprimerProduit




app_name = 'magasin'

urlpatterns = [
  path('produits/', views.AjoutProd, name='AjoutProd'),
  path('catalogue/', views.mesProduits, name='catalogue'),
  path('', views.index, name='ind'),
  path('pc/',views.PC,name='PC'),
  path('commande/', views.ajoutCommande, name='Ajoutcommande'),
  path('fournisseur/',views.nouveauFournisseur,name='fournisseur'),
  path('mesfournisseur/',views.mesfour,name='mesfour'),
  path('admins/',views.admins,name='admins'),
  path('mesCommande/',views.mesCommande,name='mesCommande'),
  path('admain/',views.admain,name='admain'),
  path('publicité/',views.pub,name='pub'),
  path('pp/',views.produits_par_categorie,name='pp'),
  path('search/', views.search_produits, name='search'),
  path('register/',views.register, name = 'register'),
  path('ProduitList/', views.mesP, name='mesP'),
  path('logout/', views.logout_view, name='logout'),
  path('login/', views.user_login, name='login'),
  path('api-auth/', include('rest_framework.urls')),
  path('api/category/', CategoryAPIView.as_view()),
  # path('ajouter/', CreerProduit.as_view(), name='creer_produit'),  
  path('<int:pk>/modifier/',ModifierProduit.as_view(), name='modifier_produit'),  
  path('<int:pk>/supprimer/',SupprimerProduit.as_view(), name='supprimer_produit'),
  path('soumettre_rating/<int:product_id>/', views.soumettre_rating, name='soumettre_rating'),
  path('api/produits/', ProductAPIView.as_view()),
  

 ]

