from django.contrib import admin
from .models import PullRequest, Review

admin.site.register(PullRequest)
admin.site.register(Review)