from django.db import models
from django.contrib.auth.models import User
from tools import DeletedStatuses


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    size = models.BigIntegerField(null=False)
    path = models.FileField(upload_to='uploads/', null=False)
    extension = models.CharField(max_length=5, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.CharField(
        max_length=20,
        choices=[(tag.name, tag.value) for tag in DeletedStatuses],
        default=DeletedStatuses.NOT_DELETED.name
    )

    class Meta:
        db_table = 'files'
        ordering = ['user', 'created_at']
        app_label = 'uploader'
