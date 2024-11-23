from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class CustomTagManager(models.Manager):
    def get_tags_for_model(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return  TagItem.objects.select_related('tag').filter(
            content_type=content_type,
            object_id=obj_id
        )


class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label


class TagItem(models.Model):
    objects = CustomTagManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # to declare genric relation ship
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    # to read the object 
    content_object = GenericForeignKey()
