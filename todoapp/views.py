from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

# Show all tasks + add new task
def todo_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'on'

        if title:  # only save if title is not empty
            Task.objects.create(
                title=title,
                description=description,
                completed=completed
            )

        return redirect('todo_list')  # redirect so form resubmission doesn’t happen

    # Fetch all tasks (newest first)
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'todoapp/todo_list.html', 
                  {
                      "tasks": tasks,
                      "completed_count": tasks.filter(completed=True).count(),
                      "pending_count": tasks.filter(completed=False).count()
                  })

def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title:
            Task.objects.create(title=title, description=description)
    return redirect("todo_list")

# Delete a task
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('todo_list')


# (Optional) Mark a task as completed
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('todo_list')


# (Optional) Edit a task – if you want later
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = request.POST.get('completed') == 'on'
        task.save()
        return redirect('todo_list')

    return render(request, 'todoapp/edit_task.html', {'task': task})
