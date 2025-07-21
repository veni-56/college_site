from .models import (
    HomePageContent,
    SliderImage,
    HomeQuickLink,
    AboutSubmenu,
    StudentDeskMenu,
    IQACSubmenu,
    HomepageCounter,
    AcademicSubMenu,
    Department,ActivitySubmenu,NAACSubmenu

)
from django.db.models import Prefetch

def basic_info(request):
    return {
        "college_info": HomePageContent.objects.first(),
        'slider_images': SliderImage.objects.all(),
        'quick_links': HomeQuickLink.objects.all(),
        "about_menus": AboutSubmenu.objects.all(),
        "student_desk_menus": StudentDeskMenu.objects.all(),
        "submenus": IQACSubmenu.objects.all(),
        'activity_menus': ActivitySubmenu.objects.all(),
        'naac_submenus': NAACSubmenu.objects.all(),

    }

    

def academic_menu_processor(request):
    return {
        'academic_submenus': AcademicSubMenu.objects.all().order_by('order')
    }

def department_list(request):
    return {
        'departments': Department.objects.all()
    }

def homepage_counters(request):
    return {
        'homepage_counters': HomepageCounter.objects.all().order_by('order')
    }

