from django.urls import path

from . import views

urlpatterns = [
    path('', views.org_list, name='org_list'),
    path('<int:org_id>/', views.org_detail, name='delete_update_org'),
    path('<int:org_id>/suborgs/', views.suborg_list, name='create_suborg'),
    path('<int:org_id>/suborgs/<int:suborg_id>/', views.suborg_detail, name='delete_suborg'),
    path('<int:org_id>/suborgs/<int:suborg_id>/invitees/', views.invitees_list, name='create_invitees'),
    path('<int:org_id>/suborgs/<int:suborg_id>/invitees/<int:invitees_id>/', views.invitees_detail, name='delete_invitees'),
    path('validate_invitee_token/', views.token_verifier, name='token verification'),
]
