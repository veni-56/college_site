from django.contrib import admin
from .models import HomePageContent,AboutSubmenu, AboutContentBlock,AcademicSubMenu, AcademicContentBlock,Department,Department, DepartmentContent,StudentDeskMenu,StudentDeskContentBlock,NAACSubmenu,NAACContent,ActivitySection, ActivityContent

admin.site.register(HomePageContent)


class AboutContentBlockInline(admin.StackedInline):
    model = AboutContentBlock
    extra = 1
    fields = ['heading','image', 'content', 'pdf',]

admin.site.register(AcademicSubMenu)
admin.site.register(AcademicContentBlock)
from django.contrib import admin
from .models import Department, DepartmentContent

class DepartmentContentInline(admin.StackedInline):  # You can change to TabularInline if preferred
    model = DepartmentContent
    extra = 1
    show_change_link = True
    fields = ['section', 'heading', 'content', 'image', 'pdf']
    readonly_fields = []

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order']
    inlines = [DepartmentContentInline]

@admin.register(DepartmentContent)
class DepartmentContentAdmin(admin.ModelAdmin):
    list_display = ['department', 'section', 'heading']
    list_filter = ['department', 'section']
    search_fields = ['heading', 'content']

class StudentDeskContentBlockInline(admin.StackedInline): 
    model = StudentDeskContentBlock
    extra = 1

class StudentDeskMenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    inlines = [StudentDeskContentBlockInline]

admin.site.register(StudentDeskMenu, StudentDeskMenuAdmin)
admin.site.register(NAACSubmenu)
admin.site.register(NAACContent)

@admin.register(ActivitySection)
class ActivitySectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ActivityContent)
class ActivityContentAdmin(admin.ModelAdmin):
    list_display = ('section', 'heading')
    search_fields = ('heading', 'content', 'block')