from cProfile import label
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .models import Job, City, Tag
from django.db import IntegrityError
from django.urls import reverse
from django.db.models import Q
from .forms import NewJobForm

# Create your views here.
def index(request):
    jobs = Job.moderated_objects.order_by('-update_date')[:10]
    return render(request, "web/index.html", {
        "jobs": jobs
    })

def jobs_list(request):
    query = request.GET.get('q', '')
    jobs = Job.moderated_objects
    if query:
        jobs = jobs.filter(Q(title__contains=query) | Q(description__contains=query) | Q(tags__title__contains=query))
    
    jobs = jobs.order_by('-update_date').distinct()[:10]
    return render(request, "web/jobs.html", {
        "jobs": jobs
    })

def job(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        raise Http404("404")
    
    if not job.moderated:
        return render(request, "web/moderation.html", status=404)

    return render(request, "web/job.html", {
        "job": job
    })

def job_add(request):
    if request.method == "POST":
        form = NewJobForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            company = form.cleaned_data['company']
            description = form.cleaned_data['description']
            contacts = form.cleaned_data['contacts']
            city = form.cleaned_data['city']
            net_salary_from = form.cleaned_data['net_salary_from']
            net_salary_to = form.cleaned_data['net_salary_to']

            job = Job(title=title, description=description, city=city, company=company, contacts=contacts, net_salary_from=net_salary_from, net_salary_to=net_salary_to)
            job.save()

            if form.cleaned_data['tags']:
                tags = []
                for tag in form.cleaned_data['tags'].split(','):
                    tags.append(tag.strip())
                
                for tag in tags:
                    try:
                        db_tag = Tag.objects.get(title__iexact=tag)
                    except Tag.DoesNotExist:
                        db_tag = Tag(title=tag)
                        db_tag.save()

                    job.tags.add(db_tag)
            
            return HttpResponseRedirect(reverse('job', args=(job.id,)))
            
        else:
            return render(request, "web/job_add.html", {
                "form": form
            })

    return render(request, "web/job_add.html", {
        "cities": City.objects.all(),
        "form": NewJobForm()
    })

