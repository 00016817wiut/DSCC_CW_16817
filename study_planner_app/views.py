import time
from django.db import connection
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegisterForm, StudyTaskForm, SubjectForm
from .models import StudyTask, Subject

def health_check(request):
    health = {
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {},
    }

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health["checks"]["database"] = "connected"
        status_code = 200
    except Exception as exc:
        health["status"] = "unhealthy"
        health["checks"]["database"] = str(exc)
        status_code = 503

    return JsonResponse(health, status=status_code)

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "study_planner_app/register.html", {"form": form})


@login_required
def dashboard(request):
    qs = StudyTask.objects.filter(owner=request.user)
    total_tasks = qs.count()
    completed_tasks = qs.filter(status=StudyTask.Status.DONE).count()

    return render(
        request,
        "study_planner_app/dashboard.html",
        {"total_tasks": total_tasks, "completed_tasks": completed_tasks},
    )


@login_required
def task_list(request):
    tasks = StudyTask.objects.filter(owner=request.user).order_by("due_date", "-created_at")
    return render(request, "study_planner_app/task_list.html", {"tasks": tasks})


@login_required
def task_detail(request, pk: int):
    task = get_object_or_404(StudyTask, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden("Not allowed")
    return render(request, "study_planner_app/task_detail.html", {"task": task})


@login_required
def task_create(request):
    if request.method == "POST":
        form = StudyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            form.save_m2m()
            return redirect("task_detail", pk=task.pk)
    else:
        form = StudyTaskForm()

    return render(request, "study_planner_app/task_form.html", {"form": form})


@login_required
def task_update(request, pk: int):
    task = get_object_or_404(StudyTask, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = StudyTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.pk)
    else:
        form = StudyTaskForm(instance=task)

    return render(request, "study_planner_app/task_form.html", {"form": form})


@login_required
def task_delete(request, pk: int):
    task = get_object_or_404(StudyTask, pk=pk)
    if task.owner != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(request, "study_planner_app/task_confirm_delete.html", {"task": task})



@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("subject_list")
    else:
        form = SubjectForm()

    return render(
        request,
        "study_planner_app/subject_list.html",
        {"subjects": subjects, "form": form},
    )

@login_required
def subject_delete(request, pk: int):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
    return redirect("subject_list")