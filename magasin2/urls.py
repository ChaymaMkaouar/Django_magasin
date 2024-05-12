from django.urls import path
from . import views
from .views import UserEditView


app_name = 'shop'

urlpatterns = [
    path('',views.ind,name='ind'),
    path('index/', views.index, name='home'),
    path('<int:myid>', views.detail, name="detail"),
    path('checkout/', views.checkout, name="checkout"),
    path('confirmation/', views.confirmation, name="confirmation" ),
    path('register/',views.register, name = 'register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.user_login, name='login'),
    path('product_page', views.product_page, name='product_page'),
	path('payment_successful', views.payment_successful, name='payment_successful'),
	path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
	path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
    path('soumettre_rating/<int:product_id>/', views.soumettre_rating, name='soumettre_rating'),
    path('contact/',views.AjoutContact , name="contact"),
    path("edit_profile/", UserEditView.as_view(), name="edit_profile"),
    path('send/',views.send , name='send'),

]   
