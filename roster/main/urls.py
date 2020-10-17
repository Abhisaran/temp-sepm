from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # path('', views.index, name='login'),
    path('<str:login_user>-<str:login_pass>-<str:login_mode>/', views.logon, name='logon_view'),
    path('<str:login_user>-<str:leave_type>*<int:days>/', views.leave, name='leave_view'),
    path('leave/<str:string>/', views.leave_status_manager, name='leave_status'),
]
