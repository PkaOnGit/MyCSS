"""
URL configuration for CSSmerge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Login.views import RegisterUserAPIView, LoginAPIView, UserProfileAPIView, ListUsersAPIView#, CustomAuthToken  # Adjust import as necessary
from Login.views import RoleDetailAPIView, RoleListCreateAPIView, UserRoleAPIView
from Ticket.views import TicketCreateAPIView, TicketEditAPIView, ListTicketsAPIView
from Notification.views import ListNotificationsAPIView
from django.urls import path, re_path
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    # ----------------User module--------------------
    path('registeration/login/', LoginAPIView.as_view(), name='login'),  # Use as_view() for class-based views
    path('registeration/register/', RegisterUserAPIView.as_view(), name='register'),
    # path('registeration/delete-user/<int:user_id>/', DeleteUserAPIView.as_view(), name='delete-user'),
    path('registeration/users/', ListUsersAPIView.as_view(), name='list-users'),
    path('registeration/profile/<int:user_id>/', UserProfileAPIView.as_view(), name='update-users'),
    # -----------------role management-------------------
    path('roles/', RoleListCreateAPIView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleDetailAPIView.as_view(), name='role-detail'),
    path('users/<int:user_id>/roles/', UserRoleAPIView.as_view(), name='user-role'),
    # ----------------Ticket module----------------
    path('tickets/', ListTicketsAPIView.as_view(), name='ticket-create'),
    path('tickets/create/', TicketCreateAPIView.as_view(), name='ticket-create'),
    path('tickets/<int:ticket_id>/', TicketEditAPIView.as_view(), name='ticket-edit'),
    # ------------------Notification Module--------
    path('notification/', ListNotificationsAPIView.as_view(), name='list-notifications'),
    # ------------------swagger---------------------
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

