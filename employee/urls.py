from django.urls import path


from . import views

urlpatterns = [
    path("", views.view_employee, name="view_employee"),
    path("team/", views.viewTeam, name="viewTeam"),
    path("presence/", views.viewPresence, name="view presence")
]
