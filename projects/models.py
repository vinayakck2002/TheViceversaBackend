from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=500, blank=True, null=True) # URL nirbandhamilla engil blank=True kodukkam
    image = models.ImageField(upload_to='projects_images/')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name