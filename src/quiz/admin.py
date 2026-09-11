from django.contrib import admin

from .models import Choice, Exam, Question


admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Choice)

admin.site.site_header = "Quiz Studio Administration"
admin.site.site_title = "Quiz Studio Admin"
admin.site.index_title = "Content management"
