from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login
from datetime import date, datetime
from django.contrib.auth import authenticate, login as auth_login
import random
from django.contrib.auth.models import User


@login_required
def task_list(request):

    create_default_user()
    
    # ⏰ Get current hour
    current_hour = datetime.now().hour

    # 👋 Greeting
    if current_hour < 12:
        greeting = "Good Morning ☀️"
    elif current_hour < 18:
        greeting = "Good Afternoon 🌤️"
    else:
        greeting = "Good Evening 🌙"

    # 📚 Quotes by category
    quotes = {
        "morning": [
            "Start your day with focus 💪",
            "Win the morning, win the day 🌅",
            "Discipline starts early 🔥",
        ],
        "afternoon": [
            "Keep pushing, you're halfway there 🚀",
            "Stay consistent, no excuses 💯",
            "Focus beats distraction 🎯",
        ],
        "evening": [
            "Reflect and improve 📈",
            "Small wins matter 🧠",
            "Plan for tomorrow today ✨",
        ]
    }

    # 🎯 Select category
    if current_hour < 12:
        selected_quotes = quotes["morning"]
    elif current_hour < 18:
        selected_quotes = quotes["afternoon"]
    else:
        selected_quotes = quotes["evening"]

    # 📅 Quote of the Day
    today_str = str(date.today())
    random.seed(today_str)
    quote = random.choice(selected_quotes)

    # ================== POST REQUEST ==================
    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        tasks = Task.objects.filter(user=request.user)
        today = date.today()

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        pending_tasks = tasks.filter(completed=False).count()
        progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        # ❗ Error case
        if not due_date:
            return render(request, "tasks/task_list.html", {
                "tasks": tasks,
                "today_tasks": tasks.filter(due_date=today),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "progress": progress,
                "today": today,
                "error": "Please select a due date",
                "quote": quote,
                "greeting": greeting,
            })

        # ✅ Create task
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )

        return redirect("task_list")

    # ================== GET REQUEST ==================

    tasks = Task.objects.filter(user=request.user)
    today = date.today()

    today_tasks = tasks.filter(due_date=today)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    context = {
        "tasks": tasks,
        "today_tasks": today_tasks,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress": progress,
        "today": today,
        "quote": quote,
        "greeting": greeting,
    }

    return render(request, "tasks/task_list.html", context)


@login_required
def complete_task(request, id):

    task = get_object_or_404(Task, id=id, user=request.user)

    if not task.completed:
        task.completed = True
        task.save()

    return JsonResponse({"success": True})


@login_required
def delete_task(request, id):

    task = get_object_or_404(Task, id=id, user=request.user)
    task.delete()

    return redirect("task_list")


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")

    else:
        form = RegisterForm()

    return render(request, "tasks/register.html", {"form": form})


def update_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect("task_list")

    return render(request, 'update_task.html', {'task': task})



def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("task_list")
        else:
            return render(request, "tasks/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "tasks/login.html")