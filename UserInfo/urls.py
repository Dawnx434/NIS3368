from django.urls import path
from UserInfo import views
from UserAuth import views as auth_model
urlpatterns = [
   path("index/", views.index),
   path("resume/", views.resume),
   path("application/", views.apply),
   path("info/", views.info),
   path("account/",views.account),
   path("logout/",auth_model.logout),
   path("modify/", views.modify),
]
