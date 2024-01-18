from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
# from django.conf.urls import url

from app.views import *


urlpatterns = [
    path('logout/',logout_view, name='logout'),
    path('login/', user_login, name='login'),
    path('accounts/login/', user_login, name='login'),
    path('admin/', admin.site.urls),
    path('', login_required(NIRview.as_view()), name='index'),
    path('nir/', login_required(NIRview.as_view()), name='index'),
    path('nirh/', login_required(NIRviewHead.as_view()), name='forhead'),
    path('nir/<int:pk>', login_required(NIRregister.as_view()), name='participateINNIR')
]
