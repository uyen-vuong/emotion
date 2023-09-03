from django.contrib import messages
# from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from manager.models import *
from manager.serializers import *
from datetime import datetime
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
import os
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Q
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .mqtt_helper import MQTT_Connection

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {}) 

@login_required
def classview(request):
    return render(request, "manager/manager_class.html", {}) 

@login_required
def lesson_show(request, *args, **kwargs):

    lessonID = kwargs['lesson']
    lesson = Lesson.objects.get(id = int(lessonID))
    context = {'lesson': lesson}
    return render(request, "manager/lesson_detail.html", context=context) 

@login_required
def supervise(request):
    clusters = Cluster.objects.all()
    context = {"clusters": clusters}
    return render(request, "manager/supervise_class.html", context=context) 

@login_required
@api_view(['POST'])
def upload_file(request):

    data = request.FILES.get('file')
    if data is not None:
        file_save = data
        fss = FileSystemStorage()
        filename =  fss.save(file_save.name, file_save)
        uploaded_file_url = fss.url(filename)
        return Response({"status": True, "url": uploaded_file_url }, status=status.HTTP_201_CREATED)
    else:
        return Response({"status" : False}, status = status.HTTP_406_NOT_ACCEPTABLE)

class ClusterList(generics.ListCreateAPIView):
    
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer 
    permission_classes = [permissions.IsAuthenticated]

class ClusterDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer 
    permission_classes = [permissions.IsAuthenticated]
#----------------------------------------------------------
class CaptureImageList(generics.ListCreateAPIView):
    
    queryset = CaptureImage.objects.all()
    serializer_class = CaptureImageSerializer 
    permission_classes = [permissions.IsAuthenticated]

class CaptureImageDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer 
    permission_classes = [permissions.IsAuthenticated]

#----------------------------------------------------------
class ConfigureList(generics.ListCreateAPIView):
    
    queryset = Configure.objects.all()
    serializer_class = ConfigureSerializer 
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data 
        cluster = data['clusterID']
        old_config = Configure.objects.filter(clusterID=int(cluster))
        # remove all old config
        if len(old_config) > 0:
            old_config.delete()
        save_records = []
        for i, url in enumerate(data['urls']):
            if url == "":
                url = "rtsp://"
            new_record = {"camera_url": url, "clusterID": int(cluster)}
            save_records.append(new_record)

        serializer = self.get_serializer(data=save_records, many=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfigureDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Configure.objects.all()
    serializer_class = ConfigureSerializer 
    permission_classes = [permissions.IsAuthenticated]

#----------------------------------------------------------
class LessonList(generics.ListCreateAPIView):
    
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer 
    permission_classes = [permissions.IsAuthenticated]

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer 
    permission_classes = [permissions.IsAuthenticated]

#----------------------------------------------------------
class EmotionLessonList(generics.ListCreateAPIView):
    
    queryset = EmotionLesson.objects.all()
    serializer_class = EmotionLessonSerializer 
    permission_classes = [permissions.IsAuthenticated]

class EmotionLessonDetail(APIView):

    # permission_classes = [permissions.IsAuthenticated]
    # http_method_names = ['get', 'patch']
    def get(self, request, *args, **kwargs):

        list_output = EmotionLesson.objects.filter(lessonID =  int(kwargs['lesson'])).order_by('-id')[:1]
        serializer_data = EmotionLessonSerializer(list_output, many = True).data 
        return Response(serializer_data, status = status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):

        """
        Sample: {"neutral" : 10,  "happiness" : 15,  "surprise" : 5,  "sadness" : 7,  "anger" : 10,  "disgust" : 2,  "fear" : 0,  "contempt": 30}
        """
        lessonID = kwargs['lesson']
        list_output = EmotionLesson.objects.filter(lessonID =  int(kwargs['lesson'])).order_by('-id')[:1]
        data = request.data 
        if len(list_output) == 0:
            # first update so need create new record
            emotion_lesson =  data 
            emotion_lesson['lessonID'] = lessonID
            serializer = EmotionLessonSerializer(data=emotion_lesson)
            if serializer.is_valid():
                serializer.save()
            serializer_data = serializer.data 
        else:
            serializer_data = EmotionLessonSerializer(list_output, many = True).data[0]
        labels = ['neutral', 'happiness', 'surprise', 'sadness', 'anger', 'disgust', 'fear', 'contempt']
        for label in labels:
            serializer_data[label] += data[label]
            serializer_data[f'latest_{label}'] = data[label]
        serializer = EmotionLessonSerializer(data=serializer_data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # remove all old record 
            list_output = EmotionLesson.objects.filter(lessonID =  int(kwargs['lesson'])).delete()
            serializer.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'progress_{lessonID}', {"type": "text_message",
                                        "text": serializer.data}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class LessonData(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(request, *args, **kwargs):
        list_output = Lesson.objects.filter(clusterID =  int(kwargs['cluster']))
        serializer_data = LessonSerializer(list_output, many = True).data 
        return Response(serializer_data, status = status.HTTP_200_OK)

class ControlDevice(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        signal = {"command" : data['command']}
        if signal['command'] == "START":
            # ATTACHT URLS
            signal['urls'] = []
        lessonID = data['lesson']
        lesson = Lesson.objects.get(id=int(lessonID))
        clusterID = lesson.clusterID.id
        cluster = Cluster.objects.get(id=clusterID)
        cfgs = Configure.objects.filter(clusterID=clusterID)
        for cfg in cfgs:
            signal['urls'].append(cfg.camera_url)
        signal['lesson'] = lessonID
        # send to local device
        mqtt_client = MQTT_Connection.getInstance()
        mqtt_client.send(signal, cluster.mac_address)
        return Response(signal, status = status.HTTP_200_OK)