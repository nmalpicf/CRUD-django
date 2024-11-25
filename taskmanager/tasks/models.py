from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'Nueva'),
        ('In Progress', 'En Proceso'),
        ('Completed', 'Completada'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
