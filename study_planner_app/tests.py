import pytest 
from django.urls import reverse

from study_planner_app.models import Subject, StudyTask


# Basic test to check if dashboard redirects unauthorized users to login
@pytest.mark.django_db
def test_dashboard_requires_login(client):
  response = client.get(reverse("dashboard"))
  assert response.status_code == 302
  assert reverse("login") in response.url


# Test to check if health check endpoint returns healthy status and database check
@pytest.mark.django_db
def test_health_check_returns_healthy(client):
  response = client.get(reverse("health-check"))
  assert response.status_code == 200

  payload = response.json()
  assert payload["status"] == "healthy"
  assert payload["checks"]["database"] == "connected"


# Test if creating a task sets the logged in user correctly
@pytest.mark.django_db
def test_task_create_sets_owner(client, django_user_model):
  user = django_user_model.objects.create_user(username="u1", password="StrongPass123!")
  subject = Subject.objects.create(name="ERP", description="Enterprise Resource Planning")

  client.force_login(user)
  response = client.post(
      reverse("task_create"),
      data={
          "title": "Learn Odoo",
          "description": "Study Odoo Point of Sale module",
          "subject": subject.id,
          "due_date": "2026.03.03", 
          "priority": "medium",
          "status": "todo",
      },
  )
  assert response.status_code == 302
  task = StudyTask.objects.get(title="Learn Odoo")
  assert task.owner == user
  assert task.subject == subject
  assert str(task.due_date) == "2026-03-03"


# Test to check that a user cannot access another user's task detail
@pytest.mark.django_db
def test_other_user_cannot_open_foreign_task(client, django_user_model):
  owner = django_user_model.objects.create_user(username="owner1", password="pass12345")
  stranger = django_user_model.objects.create_user(username="stranger1", password="pass12345")
  subject = Subject.objects.create(name="DSCC", description="Distributed Systems and Cloud Computing")

  task = StudyTask.objects.create(
      title="Master Docker commands",
      owner=owner,
      subject=subject,
  )

  client.force_login(stranger)
  response = client.get(reverse("task_detail", args=[task.pk]))

  assert response.status_code == 403


# Test to check that a user cannot access another user's task list
@pytest.mark.django_db
def test_task_list_shows_only_user_tasks(client, django_user_model):
  user1 = django_user_model.objects.create_user(username="user_a", password="pass12345")
  user2 = django_user_model.objects.create_user(username="user_b", password="pass12345")
  subject = Subject.objects.create(name="Reading, not related to studies", description="How to make friends and influence people")

  StudyTask.objects.create(title="Task of user1", owner=user1, subject=subject)
  StudyTask.objects.create(title="Task of user2", owner=user2, subject=subject)

  client.force_login(user1)
  response = client.get(reverse("task_list"))

  page = response.content.decode()
  assert response.status_code == 200
  assert "Task of user1" in page
  assert "Task of user2" not in page


# Test if authenticated user can delete a subject
@pytest.mark.django_db
def test_subject_can_be_deleted(client, django_user_model):
  user = django_user_model.objects.create_user(username="deleter1", password="pass12345")
  client.force_login(user)

  subject = Subject.objects.create(name="Programming", description="Improve programming skills")
  response = client.post(reverse("subject_delete", args=[subject.pk]))

  assert response.status_code == 302
  assert Subject.objects.filter(pk=subject.pk).exists() is False