from django.db import models
from django.utils import timezone
from users.models import CustomUser
# Create your models here.

class Cluster(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    description =  models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    mac_address = models.CharField(max_length=30)
    
    class Meta:
        db_table =  'cluster'

class CaptureImage(models.Model):

    id = models.AutoField(primary_key=True) 
    clusterID = models.ForeignKey(Cluster, related_name="of_cluster_capture", null = False, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=250)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "capture_image"

class Configure(models.Model):

    id = models.AutoField(primary_key=True)
    clusterID = models.ForeignKey(Cluster, related_name="of_cluster", null = False, on_delete=models.CASCADE)
    camera_url = models.CharField(max_length=250)
    
    class Meta:
        db_table = 'configure'

class Lesson(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True)
    clusterID = models.ForeignKey(Cluster, related_name="in_cluster", null = False, on_delete=models.CASCADE)
    start =  models.DateTimeField()
    end =  models.DateTimeField()
    status = models.CharField(default="Not running", max_length=100)

    class Meta:
        db_table = "lesson"

class EmotionLesson(models.Model):

    id = models.AutoField(primary_key=True)
    lessonID = models.ForeignKey(Lesson, related_name="of_lesson", null = False, on_delete=models.CASCADE)
    neutral = models.IntegerField(default=0)
    happiness = models.IntegerField(default=0)
    surprise = models.IntegerField(default=0)
    sadness = models.IntegerField(default=0)
    anger = models.IntegerField(default=0)
    disgust = models.IntegerField(default=0)
    fear = models.IntegerField(default=0)
    contempt = models.IntegerField(default=0)

    latest_neutral = models.IntegerField(default=0)
    latest_happiness = models.IntegerField(default=0)
    latest_surprise = models.IntegerField(default=0)
    latest_sadness = models.IntegerField(default=0)
    latest_anger = models.IntegerField(default=0)
    latest_disgust = models.IntegerField(default=0)
    latest_fear = models.IntegerField(default=0)
    latest_contempt = models.IntegerField(default=0)

    fps = models.IntegerField(default=0)
    student = models.IntegerField(default=0)
    normal_student = models.IntegerField(default=0)
    lesson_quality = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'emotion_lesson'
