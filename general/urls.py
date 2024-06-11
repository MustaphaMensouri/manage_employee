from django.urls import path


from . import views

urlpatterns = [
    path("", views.view_ferme, name="view_ferme"),
]
