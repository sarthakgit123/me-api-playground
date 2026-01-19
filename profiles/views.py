from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Project
from .serializers import ProfileSerializer, ProjectSerializer

# ---------------- PROFILE ----------------
@api_view(['GET', 'POST'])
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(id=1)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# ---------------- PROJECTS ----------------
@api_view(['GET', 'POST'])
def projects_view(request):
    profile = Profile.objects.first()

    if request.method == 'GET':
        projects = Project.objects.filter(profile=profile)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['profile'] = profile.id

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ---------------- SEARCH ----------------
@api_view(['GET'])
def project_search(request):
    skill = request.GET.get('skill')
    projects = Project.objects.filter(skills__icontains=skill)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
