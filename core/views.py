from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from .models import Job, Area, JobType, JobApplication
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden





# =========================
# HOME
# =========================
def home(request):
    if request.user.is_authenticated:
        if request.user.profile.role == "job_poster":
            return redirect("my_jobs")
        else:
            return redirect("browse_jobs")

    return render(request, "home.html")


# =========================
# BROWSE JOBS
# =========================
def browse_jobs(request):
    jobs = Job.objects.filter(status="open").select_related("area", "job_type")

    selected_area = request.GET.get("area")
    selected_job_type = request.GET.get("job_type")

    if selected_area:
        jobs = jobs.filter(area__area_name=selected_area)

    if selected_job_type:
        jobs = jobs.filter(job_type__type_name=selected_job_type)

    return render(
        request,
        "browse_jobs.html",
        {
            "jobs": jobs,
            "areas": Area.objects.all(),
            "job_types": JobType.objects.all(),
            "selected_area": selected_area,
            "selected_job_type": selected_job_type,
        }
    )


# =========================
# POST JOB
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Job, JobType, Area

@login_required
def post_job(request):
    if request.user.profile.role != "job_poster":
        return HttpResponseForbidden("You are not allowed to post jobs")

    job_types = JobType.objects.all()
    areas = Area.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        job_type_id = request.POST.get("job_type")
        area_id = request.POST.get("area")
        duration = request.POST.get("duration")
        pay = request.POST.get("pay")
        job_details = request.POST.get("job_details")

        Job.objects.create(
            title=title,
            job_type_id=job_type_id,
            area_id=area_id,
            duration=duration,
            pay=pay,
            job_details=job_details,
            owner=request.user,   # IMPORTANT
            status="open",
        )

        messages.success(request, "Job posted successfully!")
        return redirect("my_jobs")

    return render(request, "post_job.html", {
        "job_types": job_types,
        "areas": areas,
    })


# =========================
# JOB DETAIL
# =========================
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    role = request.GET.get("role", "helper")

    if job.status != "open":
        raise Http404("Job closed")

    return render(
        request,
        "job_detail.html",
        {
            "job": job,
            "role": role,
        }
    )


# =========================
# APPLY JOB (PLACEHOLDER)
# =========================
@login_required
def apply_job(request, job_id):
    if request.user.profile.role != "job_seeker":
        return HttpResponseForbidden("You are not allowed to apply")

    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        JobApplication.objects.create(
            job=job,
            name=request.user.username,
            phone=request.POST.get("phone"),
            status="pending"
        )

        messages.success(request, "Application submitted!")
        return redirect("browse_jobs")


# =========================
# VIEW APPLICANTS (PLACEHOLDER)
# =========================
@login_required
def view_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user != job.owner:
        raise Http404("Not allowed")

    applications = job.applications.all()

    return render(request, "view_applicants.html", {
        "job": job,
        "applications": applications,
    })





# =========================
# HIRE APPLICANT (PLACEHOLDER)
# =========================
@login_required
def hire_applicant(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    job = application.job

    # 🔒 OWNER CHECK
    if job.owner != request.user:
        raise Http404("You are not allowed to hire for this job")

    JobApplication.objects.filter(job=job).exclude(id=application.id).update(
        status="rejected"
    )

    application.status = "hired"
    application.save()

    job.status = "closed"
    job.save()

    messages.success(request, "Applicant hired successfully.")
    return redirect("view_applicants", job_id=job.id)

@login_required
def my_jobs(request):
    if request.user.profile.role != "job_poster":
        return HttpResponseForbidden("Access denied")

    jobs = Job.objects.filter(owner=request.user)

    total_jobs = jobs.count()
    open_jobs = jobs.filter(status="open").count()
    closed_jobs = jobs.filter(status="closed").count()

    total_applicants = JobApplication.objects.filter(
        job__owner=request.user
    ).count()

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "open_jobs": open_jobs,
        "closed_jobs": closed_jobs,
        "total_applicants": total_applicants,
    }

    return render(request, "dashboard/poster_dashboard.html", context)


@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        name=request.user.username
    ).select_related("job").order_by("-applied_at")

    total_applied = applications.count()
    hired = applications.filter(status="hired").count()
    pending = applications.filter(status="pending").count()
    rejected = applications.filter(status="rejected").count()

    context = {
        "applications": applications,
        "total_applied": total_applied,
        "hired": hired,
        "pending": pending,
        "rejected": rejected,
    }

    return render(request, "dashboard/finder_dashboard.html", context)
