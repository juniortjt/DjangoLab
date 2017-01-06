from django.db import models
from django.utils import timezone
from PIL import Image
import datetime, os
from markdown import markdown
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    document = models.FileField(upload_to='documents/')
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def file_link(self):
        if self.document:
            return "<a href='%s'>download</a>" % (self.document.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True

    def filename(self):
        if self.document:
            return os.path.basename(self.document.name)
        else:
            return ""


class Comment(models.Model):
    post = models.ForeignKey('swiftbook.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.description

