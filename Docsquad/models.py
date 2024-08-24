from django.db import models #type: ignore
from candidate.models import wallpostIPs

# Create your models here.


class Feedback(models.Model):
    post_ip = models.CharField(max_length=15)
    feedback = models.TextField()
    
    class Meta:
        db_table = 'feedback'
        
    def __str__(self):
        return f"{self.post_ip}-{self.feedback}"
    

class Docsquad(models.Model):
    userId = models.ForeignKey(wallpostIPs, on_delete=models.DO_NOTHING)
    file_type = models.CharField(max_length=1,db_comment="D for Directory and F for File")
    name = models.CharField(max_length=60)
    parent_id = models.ForeignKey('self',null=True,on_delete=models.DO_NOTHING)
    privacy = models.CharField(max_length=1,default='A',db_comment="A for public and O for private")
    file_path = models.FileField(upload_to="docsquad/",null=True)
    disabled = models.CharField(max_length=1,default='N')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'docsquad'

    def __str__(self):
        return f"{self.userId}-{self.name}"
