from django.db import models
from django.contrib.auth.models import User
from .file_model import File
from tools import DeletedStatuses


class Recognizer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in DeletedStatuses],
        default=DeletedStatuses.NOT_DELETED.name
    )

    class Meta:
        db_table = 'recognize'
        app_label = 'recognizer'
