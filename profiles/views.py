from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Profile, Project
from .serializers import ProfileSerializer, ProjectSerializer


# -------------------------
# Health Check
# -------------------------
class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


# -------------------------
# Profile (SINGLE PROFILE)
# -------------------------
class ProfileView(APIView):
    """
    POST -> Create or update the single profile
    GET  -> Fetch the profile with its projects
    """

    def get(self, request):
        profile = Profile.objects.first()

        if not profile:
            return Response({}, status=status.HTTP_200_OK)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        profile = Profile.objects.first()

        # Update if profile exists, else create
        if profile:
            serializer = ProfileSerializer(profile, data=request.data)
        else:
            serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # 🔴 THIS SAVES TO DB
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# Add Project (linked to profile)
# -------------------------
class ProjectCreateView(APIView):
    """
    POST /api/projects/
    Adds a project to the single profile
    """

    def post(self, request):
        profile = Profile.objects.first()

        if not profile:
            return Response(
                {"error": "Create profile first"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data["profile"] = profile.id  # link project to profile

        serializer = ProjectSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# Search Projects by Skill
# -------------------------
class ProjectSearchView(APIView):
    """
    GET /api/projects/search/?skill=python
    """

    def get(self, request):
        skill = request.query_params.get("skill")

        if not skill:
            return Response([], status=status.HTTP_200_OK)

        projects = Project.objects.filter(
            skills__icontains=skill
        )

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
