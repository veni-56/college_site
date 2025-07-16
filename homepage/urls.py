from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Staff
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/dashboard/', views.staff_dashboard, name='dashboard'),
    path('staff/profile/', views.profile_view, name='profile'),
    path('staff/profile/edit/', views.profile_edit, name='profile_edit'),
    path('staff/leave/apply/', views.leave_apply, name='leave_apply'),

    # About
    path('about/magazine/', views.magazines_view, name='magazine'),  
    path('about/administrative-staff/', views.administrative_staff_view, name='administrative_staff'),
    path('about/<int:submenu_id>/', views.about_submenu_detail, name='about_detail'),

    # Academic
    path('academic/programmes-offered/', views.programmes_offered, name='programmes_offered'),
    path('academic/faculty/', views.faculty_view, name='faculty_all'),  
    path('academic/faculty/<slug:dept_slug>/', views.faculty_view, name='faculty_by_dept'),
    path('academic/department/', views.department_list, name='department_list'),  
    path('academic/department/<slug:slug>/', views.department_detail, name='department_detail'),  
    path('academic/<slug:slug>/', views.academic_detail, name='academic_detail'),  

#studentdesk
    path('students-desk/rank-holders/', views.rank_holders, name='rank_holders'),
    path('students-desk/endowment-prizes/', views.endowment_prizes, name='endowment_prizes'),
    path('students-desk/forms/', views.student_forms, name='student_forms'),
    path('students-desk/<slug:slug>/', views.studentdesk_detail, name='student_desk_detail'),

    # NAAC
    path('naac/<int:submenu_id>/', views.naac_detail_view, name='naac_detail'),
#Activity
path('sports/', views.sports_home, name='sports_home'),
path('sports/<int:section_id>/', views.sports_section, name='sports_section'),

path('events/', views.event_list, name='event_list'),
path('events/<int:pk>/', views.event_detail, name='event_detail'),

path('extension/', views.extension_list, name='extension_list'),
path('extension/<int:unit_id>/', views.extension_detail, name='extension_detail'),
path('extension/<int:unit_id>/<int:section_id>/', views.extension_detail, name='extension_section'),

path('icc/', views.icc_view, name='icc_view'),
path('iic/', views.iic_view, name='iic_view'), 

path('activities/<int:submenu_id>/', views.activity_detail, name='activity_detail'),  # updated generic path
]
