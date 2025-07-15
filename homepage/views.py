from django.shortcuts import render, get_object_or_404,redirect
from .models import HomePageContent,SliderImage,HomeQuickLink,HomepageCounter,Form,AboutSubmenu,AcademicSubMenu,Programme,Department,Department, DepartmentContent,FacultyMember,StudentDeskMenu,RankHolder,EndowmentPrize,NAACSubmenu,NAACContentBlock,ActivitySubMenu,AlumniSubMenu,ActivityContentBlock,ExtensionCategory, ExtensionContent, SportsSection,ExtensionCategory, ExtensionContent,StaffProfile
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
    print("Total prizes:", prizes.count())  # check in terminal
    return render(request, 'studentdesk/endowment_prizes.html', {'prizes': prizes})


def student_forms(request):
    forms = Form.objects.all().order_by('sno')
    return render(request, 'studentdesk/student_forms.html', {'forms': forms})

#naac
def naac_detail_view(request, submenu_id):
    submenu = get_object_or_404(NAACSubmenu, id=submenu_id)
    content = NAACContentBlock.objects.filter(submenu=submenu)
    return render(request, 'naac/naac_detail.html', {
        'submenu': submenu,
        'content' : content
    })


def activity_detail(request, slug):
    submenu = get_object_or_404(ActivitySubMenu, slug=slug)
    content_blocks = submenu.content_blocks.all().order_by('id')
    return render(request, 'activities/activity_detail.html', {
        'submenu': submenu,
        'content_blocks': content_blocks,
    })
from django.shortcuts import render, get_object_or_404
from .models import (
    ActivitySubMenu, ActivityContentBlock,
    ExtensionCategory, ExtensionContent,
    SportsSection
)

# Activities: detail view
def activity_detail(request, slug):
    submenu = get_object_or_404(ActivitySubMenu, slug=slug)
    content_blocks = submenu.content_blocks.all()
    return render(request, "homepage/activity_detail.html", {
        'submenu': submenu,
        'content_blocks': content_blocks
    })


# Alumni: detail view
def alumni_detail(request, slug):
    submenu = get_object_or_404(AlumniSubMenu, slug=slug)
    content_blocks = submenu.content_blocks.all()
    return render(request, "homepage/alumni_detail.html", {
        'submenu': submenu,
        'content_blocks': content_blocks
    })


# Extension: tabbed detail view
def extension_detail(request, slug):
    extension = get_object_or_404(ExtensionCategory, slug=slug)
    blocks = ExtensionContent.objects.filter(extension=extension)

    # Organize blocks by 'section' field for tabs
    content = {}
    for block in blocks:
        content.setdefault(block.section, []).append(block)

    return render(request, "homepage/extension_detail.html", {
        'extension': extension,
        'content': content
    })


# Sports: tabbed view by section
def sports_section(request, section):
    section_title = section.replace("-", " ").title()
    section_blocks = ExtensionContent.objects.filter(
        extension__slug="sports", section=section
    )

    return render(request, "homepage/sports_section.html", {
        'section': section,
        'section_title': section_title,
        'blocks': section_blocks
    })

