from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from core.models import KYCProfile

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

        # Profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        # 🔑 CREATE KYC PROFILE (IMPORTANT)
        KYCProfile.objects.create(
            user=user,
            status="pending"
        )

        messages.success(request, "Account created. Please wait for KYC approval.")
        return redirect("login")

    return render(request, "accounts/register.html")

# =====================
# LOGIN
# =====================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        # 🔐 KYC CHECK
        try:
            kyc = KYCProfile.objects.get(user=user)
        except KYCProfile.DoesNotExist:
            messages.error(request, "KYC not submitted. Please complete verification.")
            return redirect("login")

        if kyc.status != "verified":
            messages.error(request, "Your account is under verification.")
            return redirect("login")

        # ✅ LOGIN ONLY IF VERIFIED
        login(request, user)
        return redirect("home")

    return render(request, "accounts/login.html")

# =====================
# LOGOUT
# =====================
def logout_view(request):
    logout(request)
    return redirect("home")
