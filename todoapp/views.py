from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Show all tasks + add new task
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

    

        if User.objects.filter(username=username).exists():

            return render(request, "todoapp/signup.html", {
            "error": "Username already exists"
        })
    
        user = User.objects.create_user(username=username, email=email, password=password)

        login(request, user)

        return redirect("todo_list")

    return render(request, "todoapp/signup.html")  

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("todo_list")

    return render(request, "todoapp/login.html") 

def logout_view(request):

    logout(request)

    return redirect("login")

@login_required
def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'on'

        if title:  # only save if title is not empty
            Task.objects.create(
                title=title,
                description=description,
                completed=completed,
                user=request.user if request.user.is_authenticated else None
            )

        return redirect('todo_list')  # redirect so form resubmission doesn’t happen

    # Fetch all tasks (newest first)
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'todoapp/todo_list.html', 
                  {
                      "tasks": tasks,
                      "completed_count": tasks.filter(completed=True).count(),
                      "pending_count": tasks.filter(completed=False).count()
                  })
    
@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title:
            Task.objects.create(title=title, description=description,user=request.user )
    return redirect("todo_list")

# Delete a task
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('todo_list')


# (Optional) Mark a task as completed
@login_required     
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('todo_list')


# (Optional) Edit a task – if you want later
@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        return redirect('todo_list')

    return render(request, 'todoapp/edit_task.html', {'task': task})
