from django.urls import path,include
from store import views 
# from .views import ProductDetailView

urlpatterns = [
    path('',views.index,name='home'),
    path('contact/',views.contact,name='contact'),
    path('collections',views.collections,name='collections'),
    path('login',views.loginn,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path("collections/<str:slug>",views.collectionsview,name='collectionsview'),
    path('collections/<str:cate_slug>/<str:prod_slug>',views.productview,name="productview"),
    #  path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    #  path('cart', views.cart, name="cart"),
    #  path('add-to-cat',views.addtocart,name="addtocart"),

     path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
     path('cart/', views.show_cart, name='showcart'),

     path('checkout/', views.checkout.as_view(), name='checkout'),
     path('paymentdone/',views.payment_done, name='paymentdone'),
     path('orders/', views.orders, name='orders'),

    #  path('pluscard/', views.plus_card),
     path('pluscart/', views.plus_card),
    path('minuscart/', views.minus_card),
    path('removecart/', views.remove_card),
     path('check-cart/', views.check_cart, name='check-cart'),


    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path("updateAddress/<int:pk>",views.updateAddress.as_view(),name="updateAddress"),
    path('deleteAddress/<int:pk>/',views.UpdateDelete, name='deleteAddress'),

]