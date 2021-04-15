from django.contrib import admin
from .models import Poll, Question, Answer,Participant,Option


# Register your models here.
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['start_date']
        return self.readonly_fields


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Participant)
admin.site.register(Option)
