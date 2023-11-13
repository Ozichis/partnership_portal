from django.contrib import admin
from .models import *



admin.site.site_header = 'Christ Embassy Admin'
class ChurchAdmin(admin.ModelAdmin):
    list_display = ('userinfo', 'church_name', 'main_target')

class IndividualAdmin(admin.ModelAdmin):
    list_display = ('user', 'main_target')

class PatnershipAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'date_payed', 'arm',)
    list_filter = ('amount', 'date_payed', 'arm',)

    def armed(self, obj):
        instance = obj.arm
        return instance.name


class IndividualAdmin(admin.ModelAdmin):
    list_display = ('user', 'main_target')


admin.site.register(Church, ChurchAdmin)
admin.site.register(Individual, IndividualAdmin)
admin.site.register(Patnership, PatnershipAdmin)
admin.site.register(TargetIndividual)
admin.site.register(TargetChurch)
admin.site.register(User)
admin.site.register(PatnershipArm)