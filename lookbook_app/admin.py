from django.contrib import admin
from .models import Lookbook, Profile, LookbookImage

# Register your models here.

@admin.register(Lookbook)
class LookbookAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'user','orientation','border_width', 'border_color', 'overlay_image')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(LookbookImage)
class LookbookImageAdmin(admin.ModelAdmin):
    list_display = ('id','lookbook','lookbook_id','image','transformed_image')


