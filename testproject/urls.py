"""testproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url, include, re_path
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from mobile_app_api import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    # re_path(r'^getuser/(?P<email>\w+)/?$', views.getUser),
    path('getuser/<email>/<password>/', views.getUser, name="validate_email"),
    path('adduser/', views.addUser, name="customer_add"),
    path('addadminuser/', views.addAdminUser),
    path('getadminuser/', views.getAdminUser),
    path('getUserMobile/<user_name>/<password>/', views.getUserMobile, name="validate_email"),
    path('getadminusers/', views.getAdminUsers),
    # CRUD user
    path('createUser/', views.createUser),
    path('getUser/<id>', views.editUser),
    path('updateUser/<id>', views.updateUser),

    path('admin/', admin.site.urls),
    path('', views.home),
    path('deleteadminuser/<id>', views.deleteAdminUser),
    path('deletecustomer/<id>', views.deleteCustomerUser),

    # meta main data routing
    path('createMetaMainData/', views.createMetaMainData),
    path('getMetaMainDatas/', views.getMetaMaindatas),
    path('getMetaMainDataTag/<id>', views.getMetaMainDataTag),
    path('editMetaMainData/<id>', views.getMetaMainData),
    path('updateMetaMainData/<id>', views.updateMetaMainData),
    path('updateMetaMainDataLocation/', views.updateMetaMainDataLocation),
    path('deleteMetaMainData/<id>', views.deleteMetaMainData),
    
    path('getUserByID/<id>', views.getUserByID),

    path('getMetaActivity/<id>', views.getMetaActivity),
    path('getMetaActivityService/<id>', views.getMetaActivityService),
    path('getMetaArchiveDatas/', views.getMetaArchiveDatas),
    path('addMataArchive/', views.addMataArchive),

    # maintenance data routing
    path('getMaintenance/', views.getMaintenance),
   
    # technical_category routing
    path('getTechnicalCatergory/', views.getTechnicalCategory),

    # mobile routing
    path('sendmail', views.sendmail, name='sendmail'),

     # Email reset
    path('resetEmail/', views.resetEmail),
    path('checkResetID/', views.checkResetID),
    path('resetPassword/', views.resetPassword),
    path('resetEmailMobile/', views.resetEmailMobile),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

