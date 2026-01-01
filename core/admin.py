from django.contrib import admin
from .models import Job, JobApplication, JobType, Area,KYCProfile


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "job_type", "area", "pay", "status")
    list_filter = ("status", "job_type", "area")
    search_fields = ("title",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "name", "phone", "status","applied_at")
    list_filter = ("status",)
    ordering = ("-id",)  # safest ordering


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name",)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("area_name",)

@admin.register(KYCProfile)
class KYCProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "document_type", "status", "submitted_at")
    list_filter = ("status", "document_type")
    search_fields = ("user__username",)
