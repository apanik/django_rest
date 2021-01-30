from django.contrib import admin
from .models import User,Permissons,Role

# Register your models here.
admin.site.register(User)
admin.site.register(Permissons)
admin.site.register(Role)
