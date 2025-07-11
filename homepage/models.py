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
    image = models.ImageField(upload_to='academic/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='academic/pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.submenu.title} - {self.heading}"

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
    ]
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES)
    heading = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='departments/images/', blank=True, null=True)
    pdf = models.FileField(upload_to='departments/pdfs/', blank=True, null=True)

    def __str__(self):
        return f"{self.department.name} - {self.section} - {self.heading}"


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