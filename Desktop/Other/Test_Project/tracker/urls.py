# tracker/urls.py
from django.urls import path
from . import views # Impor views dari folder yang sama

urlpatterns = [
    # Jika user mengakses URL kosong (''), panggil fungsi views.index
    # `name='index'` adalah nama untuk URL ini, berguna untuk redirect.
    path('', views.index, name='index'),
]