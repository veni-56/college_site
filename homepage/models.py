from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class StaffProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    department  = models.CharField(max_length=120)
    phone       = models.CharField(max_length=15, blank=True)
    photo       = models.ImageField(upload_to='staff_photos/', blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class LeaveRequest(models.Model):
    staff       = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    start_date  = models.DateField()
    end_date    = models.DateField()
    reason      = models.TextField()
    status      = models.CharField(max_length=20,
                                   choices=[('Pending','Pending'),
                                            ('Approved','Approved'),
                                            ('Rejected','Rejected')],
                                   default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff.user.username} ({self.start_date}–{self.end_date})"


class HomePageContent(models.Model):
    college_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logos/')

    def __str__(self):
        return self.college_name

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.caption or f"Slider Image {self.id}"


class HomeQuickLink(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Use Bootstrap icon class (e.g., 'bi-bank')")
    link = models.CharField(max_length=200, blank=True, help_text="Enter internal (e.g., /placement/) or full URL")

    def __str__(self):
        return self.title


class HomepageCounter(models.Model):
    label = models.CharField(max_length=100)  
    value = models.PositiveIntegerField()      
    order = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.label} - {self.value}"

class AboutSubmenu(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
class AboutContentBlock(models.Model):
    submenu = models.ForeignKey(AboutSubmenu, on_delete=models.CASCADE, related_name='content_blocks')
    heading = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    table_html = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='about/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='about/pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.submenu.title} - {self.heading}"

class AcademicSubMenu(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class AcademicContentBlock(models.Model):
    submenu = models.ForeignKey(AcademicSubMenu, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    table_html = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='academic/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='academic/pdfs/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

class Department(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="department_images/", blank=True, null=True) 
    order = models.PositiveIntegerField(default=0)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DepartmentContent(models.Model):
    SECTION_CHOICES = [
        ('about', 'About'),
        ('faculty', 'Faculty'),
        ('association', 'Association'),
        ('syllabus', 'Syllabus'),
        ('gallery', 'Gallery'),
        ('achievements', 'Achievements'),
        ('intercollege', 'Intercollege Meet'),
        ('vision', 'Vision Mission'),
        
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    heading = models.CharField(max_length=255, blank=True)
    table_html = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='departments/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='departments/pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.department.name} - {self.section} - {self.heading}"

class FacultyMember(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    photo = models.ImageField(upload_to="faculty/photos/")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    cv_pdf = models.FileField(upload_to="faculty/cv/", blank=True, null=True)
    position = models.CharField(max_length=200, blank=True)
    qualifications = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} - {self.department.name}"

class Programme(models.Model):
    """College-ல் Offered ஆகும் Courses (UG / PG)."""
    LEVEL_CHOICES = [
        ('UG', 'UG'),
        ('PG', 'PG'),
    ]
    level        = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='UG')
    name         = models.CharField(max_length=200)          # B.A. Tamil Literature …
    eligibility  = models.CharField(max_length=200)          # H.S.C. …
    department   = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     help_text="Which department takes care of this course?")
    order        = models.PositiveIntegerField(default=0)    # row order inside table

    class Meta:
        ordering = ['level', 'order']

    def __str__(self):
        return self.name


class StudentDeskMenu(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class StudentDeskContentBlock(models.Model):
    menu = models.ForeignKey(StudentDeskMenu, on_delete=models.CASCADE, related_name='blocks')
    heading = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    table_html = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='studentdesk/files/', blank=True, null=True)
    image = models.ImageField(upload_to='studentdesk/images/', blank=True, null=True)
    video = models.FileField(upload_to='studentdesk/videos/', blank=True, null=True)

    def __str__(self):
        return f"{self.menu.title} - {self.heading}"


class RankHolder(models.Model):
    academic_year = models.CharField(max_length=20)  # Example: "2019-2020"
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    paper = models.CharField(max_length=100, default="Part III (Major)")
    rank = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='rankholders/')

    def __str__(self):
        return f"{self.name} - {self.department}"

class EndowmentPrize(models.Model):
    sno = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    founder = models.CharField(max_length=255)
    memory_of = models.CharField(max_length=255)
    awarded_to = models.TextField()
    amount = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.sno}. {self.title}"

class Form(models.Model):
    sno = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='studentdesk/forms/')

    def __str__(self):
        return f"{self.sno}. {self.name}"


class NAACSubmenu(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
class NAACContentBlock(models.Model):
    submenu = models.ForeignKey(NAACSubmenu, on_delete=models.CASCADE)
    heading = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='naac/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='naac/pdfs/', blank=True, null=True)
    table_html = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.submenu.title} - {self.heading}"
    
# activities/models.py
from django.db import models

class ActivitySubmenu(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class ActivityContentBlock(models.Model):
    submenu = models.ForeignKey(ActivitySubmenu, on_delete=models.CASCADE, related_name='content_blocks')
    heading = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='activities/', blank=True, null=True)
    pdf = models.FileField(upload_to='activities_pdfs/', blank=True, null=True)
    table_html = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.heading or "Content Block"
# activities/models.py

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    venue = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.title
# activities/models.py
class SportsSection(models.Model):
    """Second-level tab headings for Sports page"""
    title = models.CharField(max_length=120)          # e.g. About, Vision & Mission …
    order = models.PositiveIntegerField(default=0)    # manual ordering
    def __str__(self):
        return self.title

class SportsContentBlock(models.Model):
    """Content under each tab (multiple blocks allowed)"""
    section = models.ForeignKey(
        SportsSection, on_delete=models.CASCADE, related_name='content_blocks'
    )
    heading = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='sports/', blank=True, null=True)
    pdf   = models.FileField(upload_to='sports_pdfs/', blank=True, null=True)
    table_html = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
# activities/models.py

class ExtensionUnit(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="extension_units/")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class ExtensionSection(models.Model):
    unit = models.ForeignKey(ExtensionUnit, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200)  # About, Vision & Mission etc.
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.unit.title} - {self.title}"


class ExtensionContentBlock(models.Model):
    section = models.ForeignKey(ExtensionSection, on_delete=models.CASCADE, related_name='content_blocks')
    heading = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='extension_content/', blank=True, null=True)
    pdf = models.FileField(upload_to='extension_pdfs/', blank=True, null=True)
    table_html = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.heading or "Content Block"
# activities/models.py

class ICCInfo(models.Model):
    title = models.CharField(max_length=200, default="ICC - click here")
    content = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to="icc_pdfs/", blank=True, null=True)
    
    def __str__(self):
        return self.title


class ICCFormSubmission(models.Model):
    name = models.CharField(max_length=100)
    class_or_dept = models.CharField(max_length=100)
    roll_or_designation = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# activities/models.py

class IICSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='iic_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='iic_pdfs/', blank=True, null=True)
    button_text = models.CharField(max_length=100, default="Download")

    def __str__(self):
        return self.title
