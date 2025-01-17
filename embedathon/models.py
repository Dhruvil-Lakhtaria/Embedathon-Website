from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    '''
    User Class, stores info on each candidate
    '''
    phone = models.CharField(max_length=20, verbose_name="Phone Number", unique=True)

class Team(models.Model):
    '''
    Stores Team info
    '''
    teamname = models.CharField(max_length=30, verbose_name="Team Name", unique=True)
    passcode = models.CharField(max_length=6, verbose_name="Team Passcode", unique=True)
    leader = models.OneToOneField('User', on_delete=models.CASCADE, related_name="team_leader")
    member = models.OneToOneField('User', on_delete=models.CASCADE, blank=True, null=True, related_name="team_member")

    disqualified = models.BooleanField(default=False, verbose_name="Disqualified")
    points = models.IntegerField(default=0, verbose_name="Points")
    max_task_visible = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)

    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")

    def __str__(self):
        return str(self.teamname)

class Address(models.Model):
    '''
    Stores Address info, only required for certain teams so defining as a separate model
    '''
    STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chandigarh', 'Chandigarh'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
        ('Daman and Diu', 'Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Puducherry', 'Puducherry'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    ]

    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name="team_address")
    line1 = models.CharField(max_length=100, verbose_name="Address Line 1")
    line2 = models.CharField(max_length=100, verbose_name="Address Line 2", blank=True)
    line3 = models.CharField(max_length=100, verbose_name="Address Line 3", blank=True)
    city = models.CharField(max_length=50, verbose_name="City")
    state = models.CharField(max_length=50, verbose_name="State", choices=STATE_CHOICES)
    pincode = models.CharField(max_length=6, verbose_name="Pincode")

    class Meta:
        verbose_name_plural = "Addresses"

class Task(models.Model):
    '''
    Stores information about Tasks
    '''
    title = models.CharField(max_length=50, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    points = models.IntegerField(verbose_name="Points")
    deadline = models.DateTimeField(verbose_name="Deadline")
    submission_link = models.URLField(verbose_name="Submission Link")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date Created")

    def __str__(self):
        return f"{self.id} - {self.title}"

class Score(models.Model):
    '''
    Stores information about scores
    '''
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        '''
        Overriding save method to update points
        '''
        super(Score, self).save(*args, **kwargs)
        self.team.points = Score.objects.filter(team=self.team).aggregate(models.Sum('score'))['score__sum']
        self.team.save()

    def __str__(self):
        return f"{self.task.id} - {self.team.teamname}"
