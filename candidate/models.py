# ===> candidate\models.py

from django.db import models  # type: ignore

class Candidate(models.Model):
    c_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    designation = models.CharField(max_length = 200)
    joining_date = models.DateField()
    project_no = models.CharField(max_length = 20)
    workorder_no = models.CharField(max_length = 20)
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
