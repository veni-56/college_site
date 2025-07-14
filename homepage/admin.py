from django.contrib import admin
from .models import HomePageContent,StaffProfile,SliderImage,HomepageCounter,HomeQuickLink,AboutSubmenu, AboutContentBlock,AcademicSubMenu,AcademicContentBlock,Department,DepartmentContent,FacultyMember,Programme,StudentDeskMenu,StudentDeskContentBlock,RankHolder,NAACSubmenu,NAACContentBlock,ActivitySection, ActivityContent,ActivityCategory, ActivitySubsection, ActivityContentBlock
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


@admin.register(ActivitySection)
class ActivitySectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ActivityContent)
class ActivityContentAdmin(admin.ModelAdmin):
    list_display = ('section', 'heading')
    search_fields = ('heading', 'content', 'block')


class ActivityContentBlockInline(admin.StackedInline):
    model  = ActivityContentBlock
    extra  = 1
    fields = ['heading', 'content', 'table_html', 'image', 'pdf', 'order']
    ordering = ['order']

class ActivitySubsectionInline(admin.StackedInline):
    model  = ActivitySubsection
    extra  = 1
    fields = ['title', 'slug', 'order']
    ordering = ['order']

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display        = ('name', 'order')
    prepopulated_fields = {'slug': ('name',)}
    inlines            = [ActivitySubsectionInline]

@admin.register(ActivitySubsection)
class ActivitySubsectionAdmin(admin.ModelAdmin):
    list_display        = ('title', 'category', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines            = [ActivityContentBlockInline]
