from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    education = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)

    skills = models.JSONField(blank=True, null=True)
    links = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    profile = models.ForeignKey(
        Profile,
        related_name="projects",
        on_delete=models.CASCADE,
        null=True,  # Temporarily nullable
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.JSONField()
    project_link = models.URLField(blank=True)

    def __str__(self):
        return self.title
