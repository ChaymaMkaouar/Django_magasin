from django.shortcuts import redirect
from django.template import loader
from django.shortcuts import render, HttpResponseRedirect
from .models import Product, Commande,UserPayment,Rating,Contact
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from .forms import UserRegistrationForm,EditProfileForm ,ContactForm,UserCreationForm,LoginForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import time
from django.views.generic import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, get_object_or_404
# Create your views here.
def index(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('item-name')
    if item_name !='' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    paginator = Paginator(product_object, 4)
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    return render(request, 'magasin2/index.html', {'product_object': product_object})

def soumettre_rating(request, product_id):
    if request.method == 'POST':
        rating_value = int(request.POST.get('rating'))  # Récupérer la valeur du rating depuis le formulaire
        produit = get_object_or_404(Product, pk=product_id)  # Récupérer le produit associé
        produit.rating = rating_value  # Mettre à jour le rating du produit
        produit.save()  # Sauvegarder le produit avec le nouveau rating
        rating = Rating(product=produit, value=rating_value)  # Créer un nouvel objet Rating
        rating.save()  # Sauvegarder l'objet Rating dans la base de données
        return redirect('shop:home')

def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    return render(request, 'magasin2/detail.html', {'product': product_object}) 

def checkout(request):
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode= request.POST.get('zipcode')
        com = Commande(items=items,total=total, nom=nom, email=email, address=address, ville=ville, pays=pays, zipcode=zipcode)
        com.save()
        # Réinitialiser le panier après confirmation
        localStorage.removeItem('panier')
        return redirect('confirmation')

    return render(request, 'magasin2/checkout.html') 


def confirmation(request):
    info = Commande.objects.all()[:1]
    nom= 'chayma'
    for item in info:
        nom = item.nom
    return render(request, 'magasin2/confirmation.html', {'nom': nom})     

def logout_view(request):
    logout(request)
    # Rediriger vers une page de confirmation de déconnexion ou une autre page
    return render(request,'magasin2/index.html')  # Remplacez 'page_accueil' par le nom de l'URL de la page d'accueil de votre application

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
                return render(request, 'magasin2/index.html')  # Remplacez 'magasin:home' par l'URL de la page à rediriger
            else:
                # Si l'authentification échoue, afficher un message d'erreur
                error_message = "Nom d'utilisateur ou mot de passe incorrect."
                return render(request, 'registration/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def ind(request):
    template=loader.get_template('magasin2/ind.html')
    return render(request,'magasin2/ind.html ' )

@login_required(login_url='login')
def product_page(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	if request.method == 'POST':
		checkout_session = stripe.checkout.Session.create(
			payment_method_types = ['card'],
			line_items = [
				{
					'price': settings.PRODUCT_PRICE,
					'quantity': 1,
				},
			],
			mode = 'payment',
			customer_creation = 'always',
			success_url = settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
			cancel_url = settings.REDIRECT_DOMAIN + '/payment_cancelled',
		)
		return redirect(checkout_session.url, code=303)
	return render(request, 'magasin2/product_page.html')


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	user_id = request.user.user_id
	user_payment = UserPayment.objects.get(app_user=user_id)
	user_payment.stripe_checkout_id = checkout_session_id
	user_payment.save()
	return render(request, 'magasin2/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	return render(request, 'user_payment/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)

def AjoutContact(request):
    if request.method == "POST":
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/shop')
    else:
        form = ContactForm()
        return render(request, 'magasin2/Contact.html', {'form': form})
    
class UserEditView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = "registration/edit_profile.html"
    success_url = '/shop'  # Changer l'URL de redirection vers la page d'accueil

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        # Enregistrement du formulaire et redirection vers la page d'accueil
        form.save()
        return redirect('shop:ind')
    
from django.core.mail import send_mail
from django.conf import settings

def send(request):
    if request.method == 'POST':
        nom = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Enregistrer les données dans la base de données
        contact_obj = Contact.objects.create(
            nom=nom,
            email=email,
            message=message
        )

        # Envoyer un email (en supposant que vous avez les imports nécessaires)
        send_mail(
            'Hey ' + nom,
            'Nous avons reçu votre message!\n\nVotre message: ' + message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

    return render(request, 'base.html')