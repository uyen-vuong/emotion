from django.urls import path
from manager import views

app_name = 'manager'

urlpatterns = [
    path('dashboard', views.dashboard, name = "dashboard"),
    path('class', views.classview, name = "class"),
    path('supervise', views.supervise, name = "supervise"),
    path('classes', views.ClusterList.as_view(), name = "classes-list"),
    path('class/<int:pk>', views.ClusterDetail.as_view(), name = "classes-detail"),
    path('capture/images', views.CaptureImageList.as_view(), name = "capture-image-list"),
    path('capture/images/<int:pk>', views.CaptureImageDetail.as_view(), name = "capture-image-detail"),
    path('configures', views.ConfigureList.as_view(), name = "configure-list"),
    path('configure/<int:pk>', views.ConfigureDetail.as_view(), name = "configure-detail"),
    path('lessons', views.LessonList.as_view(), name = "lesson-list"),
    path('lesson/<int:pk>', views.LessonDetail.as_view(), name = "lesson-detail"),
    path('emotions', views.EmotionLessonList.as_view(), name = "emotion-list"),
    path('emotion/<int:lesson>', views.EmotionLessonDetail.as_view(), name = "emotion-detail"),
    path('lesson_all/<int:cluster>', views.LessonData.as_view(), name = "lesson-depend-cluster"),
    path('monitor/<int:lesson>', views.lesson_show, name = "lesson-detail"),
    path('control', views.ControlDevice.as_view(), name = "control-device"),

]