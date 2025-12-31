from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile


# =====================
# REGISTER
# =====================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # ✅ Ensure profile exists
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        login(request, user)
        return redirect("home")

    return render(request, "accounts/register.html")


# =====================
# LOGIN
# =====================
def login_view(request):
    if request.method == "POST":
        print("POST DATA:", request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(request, username=username, password=password)
        print("AUTH USER:", user)

        if user is not None:
            login(request, user)

            # ✅ Safe profile access
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": "job_seeker"}
            )

            if profile.role == "job_poster":
                return redirect("my_jobs")
            else:
                return redirect("browse_jobs")

        messages.error(request, "Invalid username or password")
        return redirect("login")

    return render(request, "accounts/login.html")


# =====================
# LOGOUT
# =====================
def logout_view(request):
    logout(request)
    return redirect("home")
