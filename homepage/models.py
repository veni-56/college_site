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

# models.py
from django.db import models

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
    

class ActivitySection(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']

class ActivityContent(models.Model):
    section = models.ForeignKey(ActivitySection, on_delete=models.CASCADE, related_name='contents')
    heading = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    block = models.TextField(blank=True) 
    table_html = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='activity_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.section.name} - {self.heading}"

class ActivityCategory(models.Model):
    """Top‑level menu inside *Activities* (e.g. Sports, Extension, Gallery, IIC, Achievement)."""
    name  = models.CharField(max_length=120)
    slug  = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ActivitySubsection(models.Model):
    """Second‑level navbar inside a category (e.g. About, Vision, Faculty under Sports)."""
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE, related_name="subsections")
    title    = models.CharField(max_length=150)
    slug     = models.SlugField()
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('category', 'slug')
        ordering        = ['order']

    def __str__(self):
        return f"{self.category.name} – {self.title}"

class ActivityContentBlock(models.Model):
    subsection = models.ForeignKey(ActivitySubsection, on_delete=models.CASCADE, related_name="content_blocks")
    heading    = models.CharField(max_length=255, blank=True)
    content    = models.TextField(blank=True)
    table_html = models.TextField(blank=True, null=True)
    image      = models.ImageField(upload_to='activities/images/', blank=True, null=True)
    pdf        = models.FileField(upload_to='activities/pdfs/', blank=True, null=True)
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subsection.title} – {self.heading}"

