from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path('profile', views.profile, name='profile'),
    
    path('update_profile', views.update_profile, name='update_profile'),
    path('api/validate-emp-id/', views.validate_emp_id, name='validate-emp-id'),
    path('api/get-json-data/', views.get_json_data, name='get-json-data'),
    path('emp_id/', views.sample_api ),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name="password_reset_complete"),
]
