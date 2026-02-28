import time
from django.db import connection
from django.http import JsonResponse


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
