from django.contrib import admin
from .models import HomePageContent,StaffProfile,SliderImage,HomepageCounter,HomeQuickLink,AboutSubmenu, AboutContentBlock,AcademicSubMenu,AcademicContentBlock,Department,DepartmentContent,FacultyMember,Programme,StudentDeskMenu,StudentDeskContentBlock,RankHolder,EndowmentPrize,Form,NAACSubmenu,NAACContentBlock 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(HomePageContent)
admin.site.register(SliderImage)
from django.contrib import admin
from .models import HomeQuickLink, CollegeVideo

@admin.register(HomeQuickLink)
class HomeQuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'link')


@admin.register(CollegeVideo)
class CollegeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'has_file', 'has_link')
    search_fields = ('title',)

    def has_file(self, obj):
        return bool(obj.video_file)
    has_file.boolean = True
    has_file.short_description = 'File?'

    def has_link(self, obj):
        return bool(obj.video_link)
    has_link.boolean = True
    has_link.short_description = 'YouTube Link?'
@admin.register(HomepageCounter)
class HomepageCounterAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order')
    ordering = ['order']
class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    can_delete = False
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = (StaffProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class AboutContentBlockInline(admin.StackedInline):
    model = AboutContentBlock
    extra = 1
    fields = ['heading', 'image', 'content', 'table_html', 'pdf']

class AboutSubmenuAdmin(admin.ModelAdmin):
    inlines = [AboutContentBlockInline]

admin.site.register(AboutSubmenu, AboutSubmenuAdmin)
class AcademicContentBlockInline(admin.StackedInline):
    model = AcademicContentBlock
    extra = 1  
    fields = ['heading', 'content', 'table_html', 'image', 'pdf', 'order']
    ordering = ['order']  

class AcademicSubMenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order']
    prepopulated_fields = {'slug': ('title',)}  
    inlines = [AcademicContentBlockInline]

admin.site.register(AcademicSubMenu, AcademicSubMenuAdmin)
from django.contrib import admin
from .models import News, Achievement

admin.site.register(News)
admin.site.register(Achievement)

class DepartmentContentInline(admin.StackedInline):
    model = DepartmentContent
    extra = 1
    fields = ['section', 'heading', 'content', 'image', 'pdf']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [DepartmentContentInline]
    list_display = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department')
    list_filter = ('department',)

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'department', 'eligibility', 'order')
    list_filter  = ('level', 'department')
    ordering     = ('level', 'order')

@admin.register(EndowmentPrize)
class EndowmentPrizeAdmin(admin.ModelAdmin):
    list_display = ('sno', 'title', 'founder', 'amount')


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('sno', 'name', 'file')
    search_fields = ('name',)
    ordering = ('sno',)



class StudentDeskContentBlockInline(admin.StackedInline): 
    model = StudentDeskContentBlock
    extra = 1

class StudentDeskMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [StudentDeskContentBlockInline]

admin.site.register(StudentDeskMenu, StudentDeskMenuAdmin)

@admin.register(RankHolder)
class RankHolderAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'department', 'name', 'rank']

class NAACContentBlockInline(admin.StackedInline):
    model = NAACContentBlock
    extra = 1
    fields = ['heading', 'image', 'content', 'table_html', 'pdf']

class NAACSubmenuAdmin(admin.ModelAdmin):
    inlines = [NAACContentBlockInline]

admin.site.register(NAACSubmenu, NAACSubmenuAdmin)

from django.contrib import admin
from .models import ActivitySubmenu, ActivityContentBlock

class ActivityContentBlockInline(admin.TabularInline):
    model = ActivityContentBlock
    extra = 1

@admin.register(ActivitySubmenu)
class ActivitySubmenuAdmin(admin.ModelAdmin):
    inlines = [ActivityContentBlockInline]

admin.site.register(ActivityContentBlock)
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_from', 'venue']

# activities/admin.py
from .models import SportsSection, SportsContentBlock

class SportsContentInline(admin.TabularInline):
    model = SportsContentBlock
    extra = 1

@admin.register(SportsSection)
class SportsSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    ordering = ['order']
    inlines = [SportsContentInline]
from .models import ExtensionUnit, ExtensionSection, ExtensionContentBlock

class ExtensionContentInline(admin.TabularInline):
    model = ExtensionContentBlock
    extra = 1

class ExtensionSectionInline(admin.TabularInline):
    model = ExtensionSection
    extra = 1

@admin.register(ExtensionUnit)
class ExtensionUnitAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    inlines = [ExtensionSectionInline]
    ordering = ['order']

@admin.register(ExtensionSection)
class ExtensionSectionAdmin(admin.ModelAdmin):
    list_display = ['unit', 'title', 'order']
    ordering = ['unit', 'order']
    inlines = [ExtensionContentInline]
# activities/admin.py
from .models import ICCInfo, ICCFormSubmission

@admin.register(ICCInfo)
class ICCInfoAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(ICCFormSubmission)
class ICCFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_or_dept', 'roll_or_designation', 'submitted_at']
from .models import IICSection

@admin.register(IICSection)
class IICSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle']

from django.contrib import admin
from .models import Administrative

@admin.register(Administrative)
class AdministrativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'category')
    list_filter = ('category',)
from .models import Magazine

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('year', 'title')
