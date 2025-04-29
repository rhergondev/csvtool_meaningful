from django.shortcuts import render

import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.db import IntegrityError


@require_http_methods(["POST"])
@csrf_protect
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not username or not password:
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse(
            {"message": "Login successful", "user": user.username}, status=200
        )
    else:
        return JsonResponse(
            {"error": "Invalid credentials, check your username and password"},
            status=401,
        )


@require_http_methods(["POST"])
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User is not logged in"}, status=401)
    logout(request)
    return JsonResponse({"message": "Logout successful"}, status=200)


@require_http_methods(["POST"])
@csrf_protect
def register_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Username and password are required"}, status=400
            )

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return JsonResponse(
                {"message": "User registered successfully", "user": user.username},
                status=201,
            )
        except IntegrityError:
            return JsonResponse(
                {"error": f"Username {username} already exists"}, status=400
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@require_http_methods(["GET"])
@ensure_csrf_cookie
def status_view(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "isAuthenticated": True,
                "message": "User is logged in",
                "user": request.user.username,
            },
            status=200,
        )
    else:
        return JsonResponse(
            {
                "message": "User is not logged in",
                "isAuthenticated": False,
                "csrfToken": get_token(request),
            },
            status=200,
        )
