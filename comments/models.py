from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey

# Imported models
from post.models import Post

# 3rd Party Imports
from ckeditor_uploader.fields import RichTextUploadingField


class CommentManager(models.Manager):

    def all(self):
        """
            Overriding all() manager.
        """
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_post(self, instance=None):
        """
            Created a new manager filter_by_post()
        """
        if instance is not None:
            content_type = ContentType.objects.get_for_model(instance.__class__)
            obj_id = instance.id
            # qs = QuerySet
            qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        else:
            # If no instance is provided. by default Post class will be the
            # content type(for now).
            content_type = ContentType.objects.get_for_model(Post)
            qs = super(CommentManager, self).filter(content_type=content_type)
        return qs


class Comment(models.Model):

    # Author of comment
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # Post in which comment is made
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None, null=True)

    # Parent of comment (if nested commnet)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    # Content of comment
    comment_text = RichTextUploadingField(blank=False, null=False, verbose_name='Comment Text')

    # Time at which comment was created
    timestamp = models.DateTimeField(auto_now_add=True)

    # To apply overriding of managers
    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp', ]

    def __str__(self):
        return str(self.user.username)

    def children(self):  # replies
        return Comment.objects.filter(parent=self)

    # To check if a comment is parent or not
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    # Tried earlier
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    # comment_text = models.TextField()
