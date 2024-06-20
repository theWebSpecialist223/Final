from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name=''),
    path('register', views.register, name = "register"),
    path('my_login', views.my_login, name = "my-login"),
    path('dashboard', views.dashboard, name = "dashboard"),
    path('add_coupons', views.add_coupons, name = "add_coupons"),
    path('user_logout', views.user_logout, name = "user_logout"),
    path('issue_coupons', views.issue_coupons, name = "issue_coupons"),
    path('service_issue', views.service_issue, name = "service_issue"),
    path('report_pdf', views.report_pdf, name = 'report-pdf')
]
 