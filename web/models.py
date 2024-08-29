from django.db import models
from django.utils import timezone

# Moderated jobs obly queryset manager
class ModeratedJobManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(moderated=True)

# Create your models here.
class City(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Tag(models.Model):
    title = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.title}"

class Job(models.Model):
    title = models.CharField(max_length=64, null=False)
    company = models.CharField(max_length=64, blank=True)
    description = models.TextField(null=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name="jobs")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="jobs")
    contacts = models.CharField(max_length=256, blank=True, null=False)
    net_salary_from = models.IntegerField(blank=True, null=True, default=None)
    net_salary_to = models.IntegerField(blank=True, null=True, default=None)

    moderated = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)

    objects = models.Manager()
    moderated_objects = ModeratedJobManager()

    def is_valid_job(self):
        if self.net_salary_from and self.net_salary_to:
            if self.net_salary_from > self.net_salary_to:
                return False

        if self.net_salary_from:
            if self.net_salary_from <= 0:
                return False
        
        if self.net_salary_to:
            if self.net_salary_to <= 0:
                return False

        return self.title and self.city and self.contacts and self.description

    def __str__(self):
        return f"Title: {self.title}, city: {self.city}"
