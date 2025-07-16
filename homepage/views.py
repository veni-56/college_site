from django.shortcuts import render, get_object_or_404,redirect
from .models import HomePageContent,SliderImage,HomeQuickLink,HomepageCounter,Form,SportsSection,AboutSubmenu,AcademicSubMenu,Programme,Department,Department, DepartmentContent,FacultyMember,StudentDeskMenu,RankHolder,EndowmentPrize,NAACSubmenu,NAACContentBlock,StaffProfile
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


from django.shortcuts import render, get_object_or_404
from .models import ActivitySubmenu

def activity_detail(request, submenu_id):
    submenu = get_object_or_404(ActivitySubmenu, id=submenu_id)
    return render(request, 'activities/activity_detail.html', {'submenu': submenu})


from .models import Event
from django.shortcuts import render, get_object_or_404

def event_list(request):
    events = Event.objects.order_by('-date_from')
    return render(request, 'activities/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'activities/event_detail.html', {'event': event})

# activities/views.py
from .models import ExtensionUnit, ExtensionSection
from django.shortcuts import render, get_object_or_404

def extension_list(request):
    units = ExtensionUnit.objects.order_by('order')
    return render(request, 'activities/extension_list.html', {'units': units})


def extension_detail(request, unit_id, section_id=None):
    unit = get_object_or_404(ExtensionUnit, id=unit_id)
    sections = unit.sections.order_by('order')
    if section_id:
        active_section = get_object_or_404(ExtensionSection, id=section_id, unit=unit)
    else:
        active_section = sections.first()
    
    context = {
        'unit': unit,
        'sections': sections,
        'active_section': active_section,
    }
    return render(request, 'activities/extension_detail.html', context)
# activities/views.py

from .models import ICCInfo
from .forms import ICCForm
from django.shortcuts import render, redirect

def icc_view(request):
    iccinfo = ICCInfo.objects.first()
    form = ICCForm(request.POST or None)
    submitted = False

    if request.method == 'POST' and form.is_valid():
        form.save()
        submitted = True
        form = ICCForm()  # reset form

    return render(request, 'activities/icc.html', {
        'iccinfo': iccinfo,
        'form': form,
        'submitted': submitted,
    })
from .models import IICSection

def iic_view(request):
    iic_sections = IICSection.objects.all()
    return render(request, 'activities/iic.html', {'iic_sections': iic_sections})

from .models import Magazine

def magazines_view(request):
    magazines = Magazine.objects.all().order_by('-year')
    return render(request, 'about/magazines.html', {'magazines': magazines})
from django.shortcuts import render
from .models import Administrative

def administrative_view(request):
    admin_staff = Administrative.objects.filter(category='administrative')
    menials = Administrative.objects.filter(category='menial')
    return render(request, 'about/administrative.html', {
        'admin_staff': admin_staff,
        'menials': menials,
    })
# activities/views.py
from .models import SportsSection

def sports_home(request):
    """Default to first tab (About)."""
    first_section = SportsSection.objects.order_by('order').first()
    return sports_section(request, first_section.id if first_section else None)

def sports_section(request, section_id):
    sections = SportsSection.objects.order_by('order')
    section  = get_object_or_404(SportsSection, id=section_id)
    context = {
        'sections': sections,      # for tab bar
        'active_section': section, # which tab is open
    }
    return render(request, 'activities/sports_detail.html', context)
