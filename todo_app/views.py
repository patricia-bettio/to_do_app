from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Todo

# Create your views here.
def index(request):
    if request.method == "POST":
        text = request.POST["text"]
        todo = Todo()
        todo.text = text
        todo.save()

    todos = Todo.objects.filter(status=False)
   # todos = Todo.objects.all()
    context = {
            'todos': todos
            }

    return render(request, 'todo_app/index.html', context)

def change_status(request):
    pk = request.POST["pk"]
    todo = get_object_or_404(Todo, pk=pk)
    if "checked" in request.POST:
        todo.status = True
    else:
        todo.status = False
    todo.save()
    return HttpResponseRedirect(reverse('todo_app:index'))

def completed_todos(request):
    todos = Todo.objects.filter(status=True)
    context = {
            'todos' : todos
    }
    return render(request, 'todo_app/completed_todos.html', context)

def delete_todo(request):
    print(request.META['HTTP_REFERER'])
    ##get the primary key:
    pk = request.POST["pk"]
    ##if we get a key that doesnt exist, throw a 404:
    todo = get_object_or_404(Todo, pk=pk)
    ##delete from db:
    todo.delete()
    ##
    if request.META['HTTP_REFERER'].split('/')[-2] == 'todo':
        return HttpResponseRedirect(reverse('todo_app:index'))
    else:
        return HttpResponseRedirect(reverse('todo_app:completed_todos'))
