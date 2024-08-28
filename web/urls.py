from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("jobs/add", views.job_add, name="add"),
    path("jobs/<int:job_id>", views.job, name="job"),
    path("jobs/", views.jobs_list, name="jobs")
]