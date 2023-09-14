from django.urls import path

from . import views


urlpatterns = [
    path('user/signup',views.RegisterView.as_view(),name="register"),
    path('user/login',views.LoginView.as_view(),name="login-page"),
    path('user/logout',views.logout,name="logout-page"),
    
    path('',views.HomeView.as_view(),name="index"),
    path('search',views.SearchView.as_view(),name="search"),
    
    path('wishlist',views.WishListView.as_view(),name="wishlist"),
    path('wishlist/add',views.AddToWishList.as_view(),name="wishlist-add"),
    path('wishlist/remove',views.RemoveFromWishList.as_view(),name="wishlist-remove"),
    
    
    path('<slug:category_slug>/<slug:product_slug>/',views.ProductView.as_view(),name="getItem"),
]
