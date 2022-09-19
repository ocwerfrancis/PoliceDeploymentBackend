from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

from api.models import (
    User,
    Battallion_two,
    Battallion_one,
    Deleted_Employee,
    Battallion_three,
    Battallion_four,
    Battallion_five,
    Battallion_six
)

admin.site.site_header = "VIPPU"

admin.site.register(User)
admin.site.register(Battallion_two)
admin.site.register(Battallion_one)
admin.site.register(Deleted_Employee)
admin.site.register(Battallion_three)
admin.site.register(Battallion_four)
admin.site.register(Battallion_five)
admin.site.register(Battallion_six)