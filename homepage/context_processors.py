from .models import (
    HomePageContent,
    SliderImage,
    AboutSubmenu,
    StudentDeskMenu,
    NAACSubmenu,
    ActivitySection,
)
from django.db.models import Prefetch

# Updated for submenu fix
def basic_info(request):
    parents = ActivitySection.objects.filter(parent__isnull=True).prefetch_related(
    Prefetch('children', queryset=ActivitySection.objects.filter(parent__isnull=False))
    )


    return {
        "college_info" : HomePageContent.objects.first(),
        'slider_images': SliderImage.objects.all(),
        "about_menus": AboutSubmenu.objects.all(),
        "student_desk_menus": StudentDeskMenu.objects.all(),
        "submenus": NAACSubmenu.objects.all(),
        "nav_sections":parents,

    }

from homepage.models import AcademicSubMenu

def academic_menu_processor(request):
    return {
        'academic_submenus': AcademicSubMenu.objects.all().order_by('order')
    }

from .models import Department

def department_list(request):
    departments = Department.objects.all()
    return {
        'departments': departments
    }
