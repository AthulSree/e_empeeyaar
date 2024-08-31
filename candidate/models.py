# ===> candidate\models.py

from django.db import models  # type: ignore

class Candidate(models.Model):
    c_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    gender = models.CharField(max_length=1)
    designation = models.CharField(max_length = 200)
    joining_date = models.DateField()
    project_no = models.CharField(max_length = 20)
    workorder_no = models.CharField(max_length = 20)
    image = models.ImageField(upload_to='photos/')
    entered_time = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'candidates'



class LeaveRecords(models.Model):
    c_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, db_column='c_id')
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    paid_leave_days = models.CharField(max_length=50,null=False)
    non_paid_leave_days = models.CharField(max_length=50,null=False,default='')
    no_of_leaves = models.IntegerField(null=False)
    att_graph = models.ImageField(upload_to='photos/')
    att_details = models.ImageField(upload_to='photos/')

    def __str__(self) -> str:
        return f"{self.no_of_leaves} - {self.Candidate.name}"
    
    class Meta:
        db_table = 'leave_records'

class CandidateHistory(models.Model):
    c_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, db_column='c_id', null=False)
    name = models.CharField(max_length = 50)
    designation = models.CharField(max_length = 200)
    joining_date = models.DateField()
    project_no = models.CharField(max_length = 20)
    workorder_no = models.CharField(max_length = 20)
    data_till = models.DateTimeField()

    class Meta:
        db_table = 'candidate_history'


class Wallpost(models.Model):
    subject = models.TextField(max_length=100,null=True,default=None)
    content = models.TextField(null=True)
    files = models.FileField(upload_to="photos/")
    posted_ip = models.CharField(max_length=15)
    posted_by = models.CharField(max_length=30)
    send_to = models.CharField(max_length=20)
    posted_time = models.DateTimeField(null=False) 
    seen = models.CharField(max_length=1)
    
    reply_content = models.TextField(null=True)
    reply_ip = models.CharField(max_length=15, null=True)
    reply_by = models.CharField(max_length=30, null=True)
    reply_time = models.DateTimeField(null=True) 
    
    disabled = models.CharField(max_length=1,null=False, default='N')

    class Meta:
        db_table = 'wall_post'
        
    def __str__(self):
        # Return a descriptive string for the admin interface
        return f"{self.subject} - {self.posted_by} ({self.posted_time})"

class wallpostIPs(models.Model):
    ip = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'wall_post_ip'
        
    def __str__(self) -> str:
        return f"{self.ip}-{self.name}"
    
class wallpostAccessRecords(models.Model):
    user = models.ForeignKey(wallpostIPs, on_delete=models.CASCADE)
    last_active_time = models.DateTimeField()

    class Meta:
        db_table = 'wallpost_access_records'

    def __str__(self) -> str:
        return f"{self.user} was last active @ {self.last_active_time}"