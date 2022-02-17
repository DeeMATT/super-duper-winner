from django.db import models
import string, random
from django.utils.text import slugify
from django.urls import reverse


STATUS_CHOICES = (
   ('draft', 'Draft'),
   ('published', 'Published'),
)

def random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Pages(models.Model):
    title = models.CharField(max_length=254, blank=False, null=False)
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    body = models.JSONField(default=dict, null=False)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-published_at', )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(random_string() + "-" + self.title)

        super(Pages, self).save(*args, **kwargs)
