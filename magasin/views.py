from django.shortcuts import render
from django.template import loader
from .models import Produit
from .models import Commande,Rating
from .models import Fournisseur
from .models import ProduitNC , Categorie
from django.http import HttpResponse
from .forms import ProduitForm
from django.shortcuts import redirect
from .forms import CommandeForm
from .forms import FournisseurForm
from django.shortcuts import render, HttpResponseRedirect
from .forms import ProduitForm, FournisseurForm,UserRegistrationForm ,UserCreationForm,LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from magasin.serializers import CategorySerializer
from magasin.serializers import ProductSerializer
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .forms import ProduitForm
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Rediriger vers une page après la connexion réussie
                return render(request, 'magasin/index.html')  # Remplacez 'magasin:home' par l'URL de la page à rediriger
            else:
                # Si l'authentification échoue, afficher un message d'erreur
                error_message = "Nom d'utilisateur ou mot de passe incorrect."
                return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

class CategoryAPIView(APIView):
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# def index(request):
#     if request.method == "POST" : 
#         form = ProduitForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/magasin')
#     else :
#         form = ProduitForm() #créer formulaire vide
#         return render(request,'magasin/majProduits.html',{'form':form})

def AjoutProd(request):
    if request.method == "POST" : 
        form = ProduitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else :
        form = ProduitForm() #créer formulaire vide
        return render(request,'magasin/majProduits.html',{'form':form}) 
    
def mesProduits(request):
    template=loader.get_template('magasin/mesProduits.html')
    products=Produit.objects.all()
    context={'products':products}
    return render(request,'magasin/mesProduits.html ',context )

def mesP(request):
    template=loader.get_template('magasin/adprod.html')
    products=Produit.objects.all()
    context={'products':products}
    return render(request,'magasin/adprod.html ',context )

def index(request):
    template=loader.get_template('magasin/index.html')
    products=Produit.objects.all()
    context={'products':products}
    return render(request,'magasin/index.html ',context )

def admain(request):
    template=loader.get_template('magasin/Admain.html')
    products=Produit.objects.all()
    context={'products':products}
    return render(request,'magasin/Admain.html ',context )

def pub(request):
    template=loader.get_template('magasin/pub.html')
    products=Produit.objects.all()
    context={'products':products}
    return render(request,'magasin/pub.html ',context )

def PC(request):
    template=loader.get_template('magasin/PC.html')
    products=ProduitNC.objects.all()
    context={'products':products}
    return render(request,'magasin/PC.html ',context )

def mesprod(request):
    if request.method == "POST" : 
        form = ProduitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        list=Produit.objects.all()
        return render(request,'magasin/vitrine.html',{'list':list})

def ajoutCommande(request):
    if request.method == "POST" : 
        form = CommandeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else :
        form = CommandeForm() #créer formulaire vide
        list=Commande.objects.all()
    return render(request,'magasin/commande.html',{'form':form })




def nouveauFournisseur(request):
    if request.method == "POST" : 
        form = FournisseurForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        form = FournisseurForm() #créer formulaire vide
        list=Fournisseur.objects.all()
    return render(request,'magasin/fournisseur.html',{'form':form })

def mesfour(request):
    if request.method == "POST" : 
        form = FournisseurForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        list=Fournisseur.objects.all()
        return render(request,'magasin/mesFournisseur.html',{'list':list})
    
def mesCommande(request):
    if request.method == "POST" : 
        form = CommandeForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        list=Commande.objects.all()
        return render(request,'magasin/mesCommande.html',{'list':list})
    
def mesf(request):
    if request.method == "POST" : 
        form = FournisseurForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        list=Fournisseur.objects.all()
        return render(request,'magasin/mesFournisseur.',{'list':list})


def admins(request):
    return render(request,'magasin/admin.html')

def produits_par_categorie(request):
    if request.method == 'GET':
        lib = request.GET.get('choix')
        products = Produit.objects.filter(libellé=lib)
        context={'products':products}
    else:
        products = Produit.objects.all()
        context={'products':products}
    return render(request, 'magasin/product.html',context)

def search_produits(request):
    query = request.GET.get('query')
    if query:
        results = Produit.objects.filter(description__icontains=query)
    else:
        results = Produit.objects.all()
    context = {'results': results} 
    return render(request, 'magasin/search_results.html', context)



def logout_view(request):
    logout(request)
    # Rediriger vers une page de confirmation de déconnexion ou une autre page
    return render(request,'magasin/index.html')  # Remplacez 'page_accueil' par le nom de l'URL de la page d'accueil de votre application

def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return render(request,'registration/register.html')
    else :
        form = UserCreationForm()
    return render(request,'registration/register.html',{'form' : form})

class ModifierProduit(UpdateView):
    model = Produit
    template_name = 'magasin/edit_prod.html'
    form_class = ProduitForm  
    success_url = reverse_lazy('magasin:mesP')


class SupprimerProduit(DeleteView):
    model = Produit
    template_name = 'magasin/del_prod.html'
    success_url = reverse_lazy('magasin:mesP')


def valStar(request):
    template=loader.get_template('magasin/mesProduits.html')
    ratings=Rating.objects.all()
    context={'ratings':ratings}
    return render(request,'magasin/mesProduits.html ',context )


def soumettre_rating(request, product_id):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        produit = get_object_or_404(Produit, pk=product_id)
        produit.rating = rating
        produit.save()
        return redirect('magasin:catalogue') 
    
class ProductAPIView(APIView):
    def get(self, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProductSerializer(produits, many=True)
        return Response(serializer.data)

class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Produit.objects.all()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset  # Return the queryset without filtering by 'active'
