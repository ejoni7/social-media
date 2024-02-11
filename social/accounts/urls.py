from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
                  path('login_costom/', views.login_costom, name='login_costom'),
                  path('logout_/', views.logout_, name='logout_'),
                  path('register/', views.register, name='register'),
                  path('profile/', views.profile, name='profile'),
                  path('rules/', views.Rules.as_view(), name='rules'),
                  path('ends/', views.Ends.as_view(), name='ends'),
                  path('password_check/', views.password_check, name='password_check'),
                  # path('phone_check/', views.phone_check, name='phone_check'),
                  path('forget_password/', views.ForgetPassword.as_view(), name='forget_password'),
                  path('password_reset_done/', views.ResetDone.as_view(), name='password_reset_done'),
                  path('confirm_password/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='confirm_password'),
                  path('confirm_done/', views.ConfirmDone.as_view(), name='confirm_done'),

              ]