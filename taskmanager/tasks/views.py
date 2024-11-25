from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Task
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

@method_decorator(csrf_exempt, name='dispatch')
class TaskListCreateView(View):
    def get(self, request):
        tasks = Task.objects.all().values()
        return JsonResponse(list(tasks), safe=False)

    def post(self, request):
        data = json.loads(request.body)
        task = Task.objects.create(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'New')
        )
        return JsonResponse({'id': task.id, 'message': 'Task created successfully'}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_at': task.created_at
        })

    def put(self, request, pk):
        data = json.loads(request.body)
        task = get_object_or_404(Task, pk=pk)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.save()
        return JsonResponse({'message': 'Task updated successfully'})

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'})
