"""
URL configuration for askme_kisil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.conf import settings
from app.views import custom_404_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name='index'),
    path("hot/", views.hot, name='hot'),
    path("ask/", views.ask, name='ask'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='signup'),
    path("register/", views.register, name='register'),
    path("question/<int:question_id>", views.question, name='question'),
    path("tag/<int:tag_id>", views.tag, name='tag'),
    path('logout/', views.logout, name='logout'),
    path('tag-autocomplete/', views.tag_autocomplete, name='tag_autocomplete'), 
    path('like_question/<int:question_id>/', views.like_question, name='like_question'),
    path('get_like_status/<int:question_id>/', views.get_like_status, name='get_like_status'),
    path('like_answer/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('get_answer_like_status/<int:answer_id>/', views.get_answer_like_status, name='get_answer_like_status')
    #path('set_correct_answer/<int:question_id>/', views.set_correct_answer, name='set_correct_answer')
]

handler404 = custom_404_view

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
