"""Library_System URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from libraryapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name="index"),
    path('student_login',student_login,name="student_login"),
    path('admin_login',admin_login,name="admin_login"),
    path('admin_home',admin_home,name="admin_home"),
    path('users_logout',users_logout,name="users_logout"),
    path('student_signup',student_signup,name="student_signup"),
    path('student_home',student_home,name="student_home"),
    path('admin_registerstudents',admin_registerstudents,name="admin_registerstudents"),
    path('admin_managestudents',admin_managestudents,name="admin_managestudents"),
    path('admin_deletestudent/<int:id>',admin_deletestudent,name="admin_deletestudent"),
    path('admin_editstudent/<int:id>',admin_editstudent,name="admin_editstudent"),
    path('admin_addbook',admin_addbook,name="admin_addbook"),
    path('admin_addcategory',admin_addcategory,name="admin_addcategory"),
    path('admin_managecategories',admin_managecategories,name="admin_managecategories"), 
    path('admin_deletecategories/<int:id>',admin_deletecategories,name="admin_deletecategories"),
    path('admin_editcategory/<int:id>',admin_editcategory,name="admin_editcategory"),
    path('admin_managebooks',admin_managebooks,name="admin_managebooks"),
    path('admin_deletebook/<int:id>',admin_deletebook,name="admin_deletebook"),
    path('admin_editbook/<int:id>',admin_editbook,name="admin_editbook"),
    path('admin_issuebook',admin_issuebook,name="admin_issuebook"),
    path('admin_manageissuebook',admin_manageissuebook,name="admin_manageissuebook"),
    path('admin_returnbook/<int:id>',admin_returnbook,name="admin_returnbook"),
    path('admin_issuebookfine/<int:id>',admin_issuebookfine,name="admin_issuebookfine"),
    path('admin_changepassword',admin_changepassword,name="admin_changepassword"),
    path('student_issuedbooks',student_issuedbooks,name="student_issuedbooks"), 
    path('student_issuedbookfine/<int:id>',student_issuedbookfine,name="student_issuedbookfine"),
    path('student_changepassword',student_changepassword,name="student_changepassword"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)