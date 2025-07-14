from django.shortcuts import render, get_object_or_404,redirect
from .models import HomePageContent,SliderImage,HomeQuickLink,HomepageCounter,AboutSubmenu,AcademicSubMenu,Programme, AcademicContentBlock,Department,Department, DepartmentContent,FacultyMember,StudentDeskMenu,RankHolder,EndowmentPrize,NAACSubmenu,NAACContentBlock,ActivitySection,StaffProfile
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
        return redirect('profile')        

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

def home(request):
    counters = HomepageCounter.objects.all().order_by('order')
    return render(request, 'homepage/index.html', {'homepage_counters': counters})

#about

def about_submenu_detail(request, submenu_id):
    submenu = get_object_or_404(AboutSubmenu, id=submenu_id)
    content_blocks = submenu.content_blocks.all()
    return render(request, 'about/about_detail.html', {
        'submenu': submenu,
        'content_blocks': content_blocks,
    })
#academic_detail
def academic_detail(request, slug):
    submenu = get_object_or_404(AcademicSubMenu, slug=slug)
    content_blocks = submenu.academiccontentblock_set.all().order_by('order')

    return render(request, 'academic/academic_detail.html', {
        'submenu': submenu,
        'content_blocks': content_blocks,
    })

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'academic/department_list.html', {'departments': departments})

def department_detail(request, slug):
    department = get_object_or_404(Department, slug=slug)
    sections = ['about','vision  mission', 'faculty', 'association', 'syllabus', 'gallery', 'achievements', 'intercollege']
    content = {
        section: DepartmentContent.objects.filter(department=department, section=section)
        for section in sections
    }
    return render(request, 'academic/department_detail.html', {
        'department': department,
        'content': content,
    })


def faculty_view(request, dept_slug=None):
    departments = Department.objects.all()
    faculty_members = FacultyMember.objects.all()
    selected_dept = None

    if dept_slug:
        selected_dept = get_object_or_404(Department, slug=dept_slug)
        faculty_members = faculty_members.filter(department=selected_dept)

    return render(request, 'academic/faculty_view.html', {
        'departments': departments,
        'faculty_members': faculty_members,
        'selected_dept': selected_dept,
    })


def programmes_offered(request):
    ug_programmes = Programme.objects.filter(level='UG')
    pg_programmes = Programme.objects.filter(level='PG')
    return render(request, 'academic/programmes_offered.html', {
        'ug_programmes': ug_programmes,
        'pg_programmes': pg_programmes,
    })

def studentdesk_detail(request, slug):
    menu = get_object_or_404(StudentDeskMenu, slug=slug)
    return render(request, 'studentdesk/studentdesk_detail.html', {
        'menu': menu,
    })
def rank_holders(request):
    years = RankHolder.objects.values_list('academic_year', flat=True).distinct()
    grouped_data = {year: RankHolder.objects.filter(academic_year=year) for year in years}
    return render(request, 'studentdesk/rank_holders.html', {'grouped_data': grouped_data})

def endowment_prizes(request):
    prizes = EndowmentPrize.objects.all().order_by('sno')
    return render(request, 'studentdesk/endowment_prizes.html', {'prizes': prizes})

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

#  activities/views.py
from django.shortcuts import render, get_object_or_404
from .models import ActivityCategory, ActivitySubsection

# list all subsections of a category (e.g. /activities/sports/)
def activity_subsection_list(request, cat_slug):
    category     = get_object_or_404(ActivityCategory, slug=cat_slug)
    subsections  = category.subsections.all()
    return render(request, 'activities/activity_subsection_list.html', {
        'category': category,
        'subsections': subsections,
    })

# detail view (with tabs inside) e.g. /activities/sports/about/
def activity_detail(request, cat_slug, sub_slug):
    category    = get_object_or_404(ActivityCategory, slug=cat_slug)
    subsection  = get_object_or_404(ActivitySubsection, category=category, slug=sub_slug)
    blocks      = subsection.content_blocks.all()
    # for side‑tabs we also need all subsections of this category
    side_tabs   = category.subsections.all()
    return render(request, 'activities/activity_detail.html', {
        'category': category,
        'subsection': subsection,
        'blocks': blocks,
        'side_tabs': side_tabs,
    })

