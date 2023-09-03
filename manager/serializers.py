from rest_framework import serializers
from .models import *

class ClusterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cluster
        fields = ['id', 'name', 'mac_address', 'description', 'created', 'updated', 'status']

class CaptureImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaptureImage
        fields = ['id', 'name', 'image_path', 'created', 'updated']

class ConfigureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configure
        fields = ['id', 'camera_url', 'clusterID']
   
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', "name", 'start', 'end', 'clusterID', 'status']

class EmotionLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmotionLesson 
        fields = ['id', 'lessonID', 'neutral', 'happiness', 'surprise', 
                'sadness', 'anger', 'disgust', 'fear', 'contempt',
                'latest_neutral', 'latest_happiness', 'latest_surprise', 
                'latest_sadness', 'latest_anger', 'latest_disgust', 
                'latest_fear', 'latest_contempt',
                'fps', 'student', 'normal_student',
                'lesson_quality'
            ]

