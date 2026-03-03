from django.contrib import admin
from django.urls import path, include
from study_planner_app.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path("health/", health_check, name="health-check"),
    path('', include('study_planner_app.urls')),
]
