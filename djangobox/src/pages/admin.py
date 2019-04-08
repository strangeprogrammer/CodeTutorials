
# Register your models here.
from django.contrib import admin
from django import forms
# from django_summernote.admin import SummernoteModelAdmin
# from .models import SomeModel
# from CodeTutorials.widgets import HtmlEditor
from .models import *


# class SomeModelAdmin(SummernoteModelAdmin):
# 	summernote_fields = '__all__'

# admin.site.register(SomeModel, SomeModelAdmin)

# class AppAdminForm(forms.ModelForm):
#     model = App
#     class Meta:
#         fields = '__all__'
#         widgets = {
#             'code': HtmlEditor(attrs={'style': 'width: 90%; height: 100%;'}),
#         }

# class AppAdmin(admin.ModelAdmin):
#     form = AppAdminForm
# admin.site.register(App, AppAdmin)