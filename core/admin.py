from django.contrib import admin
from .models import Blog

admin.site.register(Blog)

from .models import ContactMessage

admin.site.register(ContactMessage)
