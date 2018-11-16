from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

'''
# Inlineformset_factory() is a small abstraction on top of formsets that simplifies working with related objects
# This function allows us to build a model formset dynamically for the Module object related to a Course object
- field: The fields that will be included in each form of the formset
- extra: Allows us to set up the number of empty extra forms to display in the formset
- can_delete: If it's True, Django will include a Boolean field for each form that will be rendered as a checkbox input
              It allows you to mark the objects you want to delete
'''
ModuleFormSet = inlineformset_factory(Course, Module, fields=['title', 'description'],
                                      extra=2, can_delete=True)



