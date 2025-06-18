from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/<int:submenu_id>/', views.about_detail_view, name='about_detail'),
    path('academic/department/', views.department_list, name='department_list'),
    path('academic/department/<slug:slug>/', views.department_detail, name='department_detail'),
    path('academic/<slug:slug>/', views.academic_detail, name='academic_detail'),
    path('students-desk/<slug:slug>/', views.studentdesk_detail, name='student_desk_detail'),
    path('naac/<int:submenu_id>/', views.naac_detail_view, name='naac_detail'),
    path('activities/<slug:slug>/', views.activity_detail, name='activity_detail'),


]


