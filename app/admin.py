from django.contrib import admin
from django.forms import EmailField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *


class UserCreateForm2(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        field_classes = {"email": EmailField}

    # placeholders = ['example@email.com', 'Username', ]
    
    
class AccountAdmin(UserAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_staff', )
    search_fields = ('email', )
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("username","first_name", "last_name", "surename","user_type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
                },
            ),
        )


admin.site.register(CustomUser, AccountAdmin)
admin.site.register(Fakultety)
admin.site.register(Kafedry)
admin.site.register(spetsialnosti)
admin.site.register(gruppy)
admin.site.register(studenty)
admin.site.register(sotrudnikyiOnKafedra)
admin.site.register(NIR)
admin.site.register(orgkomitety)
admin.site.register(uchastnikyOnNIR)
