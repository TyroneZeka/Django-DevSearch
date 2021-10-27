from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required 
from .models import Project
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from .utils import searchProjects,paginateProjects

# Create your views here.
from django.http import HttpResponse

def projects(request):
    projects,search_query = searchProjects(request)
    
    custom_range,projects = paginateProjects(request,projects,6)
    
    context = {'projects': projects,'search_query':search_query,'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    form = ReviewForm()
    projectObj = Project.objects.get(id= pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit= False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
         # Update project vote and vote count
        projectObj.getVoteCount
        
        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=projectObj.id)
        


    return render(request, 'projects/single-project.html', {'project': projectObj,'form':form})

@login_required(login_url = "login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method =='POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile
            project.save()
            messages.success(request,"New Project Created Successfully!")
            return redirect('account')

    context = {'form':form}
    return render(request,'projects/project_form.html', context)

@login_required(login_url = "login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method =='POST':
        form = ProjectForm(request.POST,request.FILES,instance = project)
        if form.is_valid():
            form.save()
            messages.success(request,"Project Updated Successfully!")
            return redirect('account')

    context = {'form':form}
    return render(request,'projects/project_form.html', context)

@login_required(login_url = "login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method =='POST':
        project.delete()
        messages.success(request,"Project Deleted Successfully!")
        return redirect('account')

    context = {'object':project}
    return render(request, 'delete_template.html', context)