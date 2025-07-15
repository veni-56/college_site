from django.contrib import admin
from .models import HomePageContent,StaffProfile,SliderImage,HomepageCounter,HomeQuickLink,AboutSubmenu, AboutContentBlock,AcademicSubMenu,AcademicContentBlock,Department,DepartmentContent,FacultyMember,Programme,StudentDeskMenu,StudentDeskContentBlock,RankHolder,EndowmentPrize,Form,NAACSubmenu,NAACContentBlock 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(HomePageContent)
admin.site.register(SliderImage)
admin.site.register(HomeQuickLink)

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
from .models import (
    ActivitySubMenu, ActivityContentBlock,
    ExtensionCategory, ExtensionContent,
    SportsSection
)

# Activity Content Inline
class ActivityContentInline(admin.StackedInline):
    model = ActivityContentBlock
    extra = 1

# Activity SubMenu Admin
@admin.register(ActivitySubMenu)
class ActivitySubMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ActivityContentInline]
    ordering = ['title']

# Extension Category Admin
@admin.register(ExtensionCategory)
class ExtensionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

# Extension Content Admin
@admin.register(ExtensionContent)
class ExtensionContentAdmin(admin.ModelAdmin):
    list_display = ('extension', 'section', 'heading')
    list_filter = ('extension', 'section')
    search_fields = ('heading', 'description')

# Sports Section Admin
@admin.register(SportsSection)
class SportsSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['order']
