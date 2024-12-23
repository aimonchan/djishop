from django.urls import path
from . import views

urlpatterns = [
    path('update-item/', views.updateItem, name="update-item"),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('cart/',views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('wishlist/',views.wishlist, name="wishlist"),
    path('account/',views.account, name="account"),
    path('ourstory/', views.ourstory, name="ourstory"),
    path('contact/',views.contact, name="contact"),
    path('productdetail/<int:product_id>/', views.productdetail, name="productdetail"),
    path('404/', views.notfound, name="notfound"),
    path('process_order/', views.processOrder, name="process_order"),
    path('test/', views.test, name="test"),
    path('testtwo/', views.testtwo, name="testtwo"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart_html_update/<int:product_id>/', views.cart_html_update, name="cart_html_update"),
    path('searched_product/', views.searched_product, name="searched_product"),
]
