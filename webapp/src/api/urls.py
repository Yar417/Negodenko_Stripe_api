from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('item/<int:pk>/', views.ItemView.as_view(), name='item-detail'),
    path('config/', views.stripe_config),
    path('buy/<int:id>', views.create_checkout_session, name='checkout-session'),

    path('cancel/', views.CancelView.as_view(), name='cancel'),
    path('success/', views.SuccessView.as_view(), name='success'),
]
