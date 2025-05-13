"""stagestools_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
import myproject.urls
import myproject_module1.urls
import myproject_module2.urls
import myproject_customization.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("myproject_customization/", include(myproject_customization.urls.urlpatterns)),
    path("myproject_module2/", include(myproject_module2.urls.urlpatterns)),
    path("myproject_module1/", include(myproject_module1.urls.urlpatterns)),
    path("myproject/", include(myproject.urls.urlpatterns)),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
