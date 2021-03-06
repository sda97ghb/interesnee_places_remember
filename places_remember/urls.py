"""places_remember_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from places_remember import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from places_remember.views import MyView
    2. Add a URL to urlpatterns:  path('', MyView.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from places_remember import views

app_name = "places_remember"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("memories/new/", views.CreateMemoryView.as_view(), name="create_memory"),
    path("memories/<int:pk>/", views.UpdateMemoryView.as_view(), name="update_memory"),
    path("memories/<int:pk>/delete/", views.DeleteMemoryView.as_view(), name="delete_memory"),
]
