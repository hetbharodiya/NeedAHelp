from django.urls import path, include
from . import views
from django.contrib import admin   # ✅ THIS LINE WAS MISSING

urlpatterns = [
    path("", views.home, name="home"),
    path("jobs/", views.browse_jobs, name="browse_jobs"),
    path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),
    path("post-job/", views.post_job, name="post_job"),
    path("jobs/<int:job_id>/apply/", views.apply_job, name="apply_job"),
    path("jobs/<int:job_id>/applicants/", views.view_applicants, name="view_applicants"),
    path("applications/<int:application_id>/hire/", views.hire_applicant, name="hire_applicant"),
    path("admin/", admin.site.urls),
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("my-applications/", views.my_applications, name="my_applications"),


    



]