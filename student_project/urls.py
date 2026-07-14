"""
URL configuration for student_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # register and login urls
    path('homepage/' , homepage , name = 'homepage'),
    path('insert_course/' , insert_course , name = 'insert_course'),
    path('view_course/' , view_course , name = 'view_course'),
    path('insert_trainer/' , insert_trainer , name = 'insert_trainer'),
    path('insert_student/' , insert_student , name = 'insert_student'),
    path('signin_student/' , signin_student , name = 'signin_student'),
    path('signin_trainer/' , signin_trainer , name = 'signin_trainer'),
    path('get_trainers/<int:id>/' , get_trainers , name = 'get_trainers'),
    path('course/<int:id>/' , course_detail , name = 'course_detail'),

    # student urls
    path('student_dashboard/' , student_dashboard , name = 'student_dashboard'),
    path('student_edit_profile/' , student_edit_profile , name = 'student_edit_profile'),
    path('student_change_pw/' , student_change_pw , name = 'student_change_pw'),
    path('otp_sent/' , otp_sent , name = 'otp_sent'),
    path('otp_verify/' , otp_verify , name = 'otp_verify'),
    path('password_validate/' , password_validate , name = 'password_validate'),
    path('student_browse_course/' , student_browse_course , name = 'student_browse_course'),
    path('student_logout/' , student_logout , name = 'student_logout'),
    path('send_otp/' , send_otp , name = 'send_otp'),
    path('verify_otp/' , verify_otp , name = 'verify_otp'),
    path('validate_password/' , validate_password , name = 'validate_password'),
    path('enroll_courses/' , enroll_courses , name = 'enroll_courses'),
    path('my_courses/' , my_courses , name = 'my_courses'),
    path('my_course_content/<int:id>/' , my_course_content , name = 'my_course_content'),
    path('save_progress/' , save_progress , name = 'save_progress'),
    path('certificate/<int:id>/' , certificate , name = 'certificate'),
    path('download_certificate/<int:id>' , download_certificate , name = 'download_certificate'),
    path('payment/<int:id>' , payment , name = 'payment'),
    path('payment_success/' , payment_success , name = 'payment_success'),
    # trainer urls
    path('trainer_dashboard/' , trainer_dashboard , name = 'trainer_dashboard'),
    path('edit_trainer_profile/' , edit_trainer_profile , name = 'edit_trainer_profile'),
    path('trainer_change_pw/' , trainer_change_pw , name = 'trainer_change_pw'),
    path('trainer_logout/' , trainer_logout , name = 'trainer_logout'),
    path('add_course_content/' , add_course_content , name = 'add_course_content'),
    path('display_course_content/' , display_course_content , name = 'display_course_content'),
    path('view_video/<id>/' , view_video , name = 'view_video'),
    path('socket_test/' , socket_test , name = 'socket_test')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
