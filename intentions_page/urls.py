from django.urls import include, path
import views

urlpatterns = [
    path('',views.home, name='home'),
    path("create", views.create, name='create'),
    path("edit/<int:primary_key>", views.edit, name='edit'),
    path("append/<int:primary_key>", views.append, name='append'),
    path("history", views.history, name='history'),
    path("feedback", views.feedback, name='feedback'),
    path("privacy-policy", views.privacy_policy)
]
