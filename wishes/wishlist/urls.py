from django.urls import path
from wishlist import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.UserWishListView.as_view(), name='wishlist'),
    path('<int:pk>/',views.UserWishListDetailView.as_view(),name='detail'),
    path('create/',views.CreateWishListView,name='create'),
    path('update/<int:pk>/',views.WishListUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',views.WishListDeleteView.as_view(),name='delete')

]
