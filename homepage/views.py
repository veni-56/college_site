from django.shortcuts import render, get_object_or_404,redirect
from .models import HomePageContent,SliderImage,HomeQuickLink,AboutSubmenu, AboutContentBlock,AcademicSubMenu, AcademicContentBlock,Department,Department, DepartmentContent,StudentDeskMenu,NAACSubmenu,NAACContentBlock,ActivitySection,StaffProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms  import StaffProfileForm, LeaveRequestForm   


def staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Invalid credentials.")
    return render(request, 'homepage/staff/staff_login.html')

@login_required(login_url='staff_login')
def staff_logout(request):
    logout(request)
    return redirect('staff_login')

@login_required(login_url='staff_login')
def staff_dashboard(request):
    return render(request, 'homepage/staff/dashboard.html')


@login_required(login_url='staff_login')
def profile_edit(request):
    profile, _ = StaffProfile.objects.get_or_create(user=request.user)

    form = StaffProfileForm(request.POST or None,
                            request.FILES or None,
                            instance=profile,
                            user=request.user)        

    if form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect('profile')         # ←  NOT  'staff:profile'

    return render(request,
                  'homepage/staff/profile_edit.html',
                  {'form': form})

@login_required(login_url='staff_login')
def profile_view(request):
    profile, _ = StaffProfile.objects.get_or_create(user=request.user)
    return render(request, 'homepage/staff/profile_view.html', {'profile': profile})


@login_required(login_url='staff_login')
def leave_apply(request):
    return render(request, 'homepage/staff/leave_apply.html')
#home
def home(request):
    content = HomePageContent.objects.first()
    about_pages = AboutSubmenu.objects.all()
    return render(request, 'homepage/index.html', {
        'content': content,
        'about_pages': about_pages
    })

def home(request):
    slider_images = SliderImage.objects.all()
    return render(request, 'homepage/index.html', {'slider_images': slider_images})

def home_view(request):
    quick_links = HomeQuickLink.objects.all()
    return render(request, 'homepage/index.html', {
        'quick_links': quick_links
    })



#about
def about_detail_view(request, submenu_id):
    submenu = get_object_or_404(AboutSubmenu, id=submenu_id)
    blocks = AboutContentBlock.objects.filter(submenu=submenu)
    return render(request, 'about/about_detail.html', {
        'submenu': submenu,
        'blocks': blocks
    })  
#academic_detail
def academic_detail(request, slug):
    submenu = get_object_or_404(AcademicSubMenu, slug=slug)
    contents = AcademicContentBlock.objects.filter(submenu=submenu)
    return render(request, 'academic/academic_detail.html', {
        'submenu': submenu,
        'contents': contents
    })


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'academic/department_list.html', {'departments': departments})

def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    sections = ['about', 'faculty', 'association', 'syllabus', 'gallery', 'achievements', 'intercollege']
    content = {
        section: DepartmentContent.objects.filter(department=department, section=section)
        for section in sections
    }
    return render(request, 'academic/department_detail.html', {
        'department': department,
        'content': content,
    })


def studentdesk_detail(request, slug):
    menu = get_object_or_404(StudentDeskMenu, slug=slug)
    return render(request, 'studentdesk/studentdesk_detail.html', {
        'menu': menu,
    })

#naac
def naac_detail_view(request, submenu_id):
    submenu = get_object_or_404(NAACSubmenu, id=submenu_id)
    content = NAACContentBlock.objects.filter(submenu=submenu)
    return render(request, 'naac/naac_detail.html', {
        'submenu': submenu,
        'content' : content
    })


#activitys
def activity_detail(request, slug):
    section = get_object_or_404(ActivitySection, slug=slug)
    contents = section.contents.all()
    return render(request, 'activities/activity_detail.html', {
        'section': section,
        'contents': contents
    })