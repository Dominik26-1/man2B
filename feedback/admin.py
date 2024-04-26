from django.contrib import admin

from common.admin import BasicAdmin
from .models import *

# Register your models here.
admin.site.register(Company, BasicAdmin)
admin.site.register(Team, BasicAdmin)
admin.site.register(Department, BasicAdmin)
admin.site.register(Position, BasicAdmin)
admin.site.register(EmployeeManagement, BasicAdmin)
admin.site.register(Employee, BasicAdmin)
admin.site.register(Project, BasicAdmin)
admin.site.register(Feedback, BasicAdmin)
admin.site.register(Rating, BasicAdmin)
admin.site.register(Skill, BasicAdmin)
