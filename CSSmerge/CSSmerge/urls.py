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
from Login.views import RegisterAPIView, LoginAPIView, DeleteUserAPIView, UserProfileAPIView, ListUsersAPIView#, CustomAuthToken  # Adjust import as necessary
from Login.views import RoleDetailAPIView, RoleListCreateAPIView, UserRoleAPIView
from Ticket.views import TicketListCreateAPIView, TicketRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    # ----------------User module--------------------
    # path('api-token-auth/', CustomAuthToken.as_view(), name='get-token'),
    path('registeration/login/', LoginAPIView.as_view(), name='login'),  # Use as_view() for class-based views
    path('registeration/register/', RegisterAPIView.as_view(), name='register'),
    path('registeration/delete-user/<int:user_id>/', DeleteUserAPIView.as_view(), name='delete-user'),
    path('registeration/users/', ListUsersAPIView.as_view(), name='list-users'),
    path('registeration/profile/<int:user_id>/', UserProfileAPIView.as_view(), name='list-users'),
    # -----------------role management-------------------
    path('roles/', RoleListCreateAPIView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleDetailAPIView.as_view(), name='role-detail'),
    path('users/<int:user_id>/roles/', UserRoleAPIView.as_view(), name='user-role'),
    # ----------------Ticket module----------------
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
]

