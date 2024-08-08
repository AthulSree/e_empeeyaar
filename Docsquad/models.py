from django.db import models

# Create your models here.


class Feedback(models.Model):
    post_ip = models.CharField(max_length=15)
    feedback = models.TextField()
    
    class Meta:
        db_table = 'feedback'
        
    def __str__(self):
        return f"{self.post_ip}-{self.feedback}"