"""invitation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from dashboard.admin import admin_site
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from dashboard.views import show_invite_card

urlpatterns = [
    path('', RedirectView.as_view(url='panel/', permanent=False), name='index'),
    path('admin/', admin_site.urls),
    path('panel/', include('dashboard.urls')),
    path('auth/', include('authentication.urls')),
    path('payment/', include('payment.urls')),
    path('invite/<uuid:card_id>', show_invite_card, name='show_invite_card'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)