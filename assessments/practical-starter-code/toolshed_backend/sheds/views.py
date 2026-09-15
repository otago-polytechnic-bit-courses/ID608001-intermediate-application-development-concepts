from django.contrib.auth import authenticate
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Shed, Tool


@api_view(["GET", "POST"])
def sheds(request):
    if request.method == "GET":
        city = request.GET.get("city")

        if city:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, suburb, city FROM sheds_shed WHERE city = '"
                    + city
                    + "' ORDER BY id"
                )
                rows = cursor.fetchall()
            d = []
            for r in rows:
                d.append({
                    "id": r[0],
                    "name": r[1],
                    "suburb": r[2],
                    "city": r[3],
                    "tool_count": Tool.objects.filter(shed_id=r[0]).count(),
                })
            return Response(d)

        d = []
        for s in Shed.objects.all().order_by("id"):
            d.append({
                "id": s.id,
                "name": s.name,
                "suburb": s.suburb,
                "city": s.city,
                "tool_count": s.tools.count(),
            })
        return Response(d)

    if request.user.is_authenticated == False:
        return Response(
            {"detail": "Authentication credentials were not provided."}, status=401
        )

    body = request.data
    if "name" in body and body["name"] != "":
        s = Shed()
        s.name = body["name"]
        s.suburb = body["suburb"]
        s.city = body["city"]
        s.owner = request.user
        s.save()
        return Response({
            "id": s.id,
            "name": s.name,
            "suburb": s.suburb,
            "city": s.city,
            "tool_count": 0,
        }, status=201)
    else:
        return Response({"detail": "Invalid data."}, status=400)


@api_view(["GET", "PUT", "DELETE"])
def shed_detail(request, id):
    try:
        s = Shed.objects.get(id=id)
    except:
        return Response({"detail": "Not found."}, status=404)

    if request.method == "GET":
        tools = []
        for t in s.tools.all().order_by("id"):
            tools.append({
                "id": t.id,
                "name": t.name,
                "description": t.description,
            })
        return Response({
            "id": s.id,
            "name": s.name,
            "suburb": s.suburb,
            "city": s.city,
            "created_at": s.created_at.isoformat(),
            "tools": tools,
        })

    if request.method == "PUT":
        if request.user.is_authenticated == False:
            return Response(
                {"detail": "Authentication credentials were not provided."}, status=401
            )
        if s.owner.id != request.user.id and request.user.is_staff == False:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )

        body = request.data
        if "name" in body and body["name"] != "":
            s.name = body["name"]
        else:
            return Response({"detail": "Invalid data."}, status=400)
        if "suburb" in body:
            s.suburb = body["suburb"]
        if "city" in body:
            s.city = body["city"]
        s.save()
        return Response({
            "id": s.id,
            "name": s.name,
            "suburb": s.suburb,
            "city": s.city,
            "tool_count": s.tools.count(),
        })

    if request.method == "DELETE":
        if request.user.is_authenticated == False:
            return Response(
                {"detail": "Authentication credentials were not provided."}, status=401
            )
        if s.owner.id != request.user.id and request.user.is_staff == False:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=403,
            )
        s.delete()
        return Response(status=204)


@api_view(["GET"])
def tools(request, id):
    try:
        s = Shed.objects.get(id=id)
    except:
        return Response({"detail": "Not found."}, status=404)

    d = []
    for t in s.tools.all().order_by("id"):
        d.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
        })
    return Response(d)


@api_view(["POST"])
def login(request):
    body = request.data
    print("login attempt: " + str(body))

    user = authenticate(username=body["username"], password=body["password"])

    if user is None:
        return Response(
            {"detail": "No active account found with the given credentials"}, status=401
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })