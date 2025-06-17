from django.contrib import admin
from .models import HomePageContent,AboutSubmenu, AboutContentBlock,AcademicSubMenu,AcademicContentBlock,Department,Department, DepartmentContent,StudentDeskMenu,StudentDeskContentBlock,NAACSubmenu,NAACContentBlock,ActivitySection, ActivityContent

admin.site.register(HomePageContent)

class AboutContentBlockInline(admin.StackedInline):
    model = AboutContentBlock
    extra = 1
    fields = ['heading', 'image', 'content', 'table_html', 'pdf']

class AboutSubmenuAdmin(admin.ModelAdmin):
    inlines = [AboutContentBlockInline]

admin.site.register(AboutSubmenu, AboutSubmenuAdmin)
admin.site.register(AcademicSubMenu)
admin.site.register(AcademicContentBlock)

class DepartmentContentInline(admin.StackedInline):  
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