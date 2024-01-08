from django.contrib import admin
from django.urls import path

from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', NIRview.as_view()),
    path('nir/', NIRview.as_view()),
    path('nir/<int:pk>', NIRregister.as_view(), name='participateINNIR')
]
