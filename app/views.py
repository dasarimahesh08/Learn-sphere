from django.shortcuts import render , get_object_or_404 , redirect
from app.models import *
from django.http import HttpResponse , HttpResponseRedirect , JsonResponse , FileResponse
from django.urls import reverse
from django.contrib.auth import login , logout
from django.views.decorators.cache import cache_control , never_cache
from django.contrib.auth.decorators import login_required
import random 
import json
import socket
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password , check_password
from django.contrib import messages
from django.utils import timezone
from datetime import date
from PIL import Image , ImageDraw , ImageFont
from django.core.files import File
import uuid
import razorpay 
from django.conf import settings
from app.google_drive import upload_file_to_drive , get_drive_file_url
import traceback
import requests
import os
from app.google_drive import delete_file_from_drive
# Create your views here.

def send_brevo_email(subject, html_content, to_email, to_name=""):
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        print("BREVO_API_KEY is not set — cannot send email")
        return False
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }
    payload = {
        "sender": {"name": "LearnSphere", "email": "maheshdasarimahesh30@gmail.com"},
        "to": [{"email": to_email, "name": to_name or to_email}],
        "subject": subject,
        "htmlContent": html_content,
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print("BREVO MAIL ERROR:", repr(e))
        return False

def homepage(request):
    QSLCO = Course.objects.all()
    d = {'QSLCO':QSLCO , }
    return render(request , 'homepage.html' , d)

def insert_course(request):
    msg = {}
    if request.method == 'POST':
        title = request.POST['ct']
        desc = request.POST['des']
        rps = request.POST['rs']
        duration = request.POST['duration']
        
        if title =="":
            msg['title'] = "Please enter the title"
        if desc == "":
            msg['des'] = "please enter the description"
        
        if duration == "":
            msg["duration"] = "Please enter the duration"
        if rps == "":
            msg["rs"] = "Please enter the price"
        else:
            rs = int(rps)

            CO = Course.objects.get_or_create(cname = title , description = desc , price = rs , duration = duration)
            if CO[1]:
                msg['login'] = "Login successfully completed"
                return HttpResponseRedirect(reverse('trainer_dashboard'))
            else:
                msg['exist'] = "This course is already exist"
                
        
    return render(request , 'insert_course.html' , {'msg':msg})

def view_course(request):
    QSCO = Course.objects.all()
    d = {'QSCO':QSCO}
    return render(request , 'view_course.html' , d)

def course_detail(request , id):
    course = get_object_or_404(Course , cid = id)

    qslto = Trainer.objects.filter(cid = course)

    d = {'course':course , 'qslto': qslto}
    return render(request , 'course_detail.html' , d )

def insert_trainer(request):
    showmsg = {}
    CO = Course.objects.all()
    if request.method == 'POST':
        name = request.POST['tfn']
        mail = request.POST['eml']
        sal = request.POST['sal']
        exp = request.POST['exp']
        spe = request.POST['spe']
        tpw = request.POST['pw']
        courses = request.POST.getlist('courses')
        pic = request.FILES.get('pic')
        enctpw = make_password(tpw)
        if courses:
            getcourse = [int(crs) for crs in courses]
        else:
            showmsg['courseerror'] = "Please select atleast one course"

        if sal =="":
            showmsg['emptysal'] = "Please enter the salary"
        else:
            int(sal)
            TTO = Trainer.objects.get_or_create(tname = name , temail = mail , tsal = sal , experience = exp ,
            specializtion = spe , tpassword = enctpw , profile_pic = pic)
            addcourse = TTO[0].cid.set(getcourse)
        
            if TTO[1]:
                showmsg['success'] = "Registarion is successfully completed"
                try:
                   send_brevo_email(
                        subject="Registration",
                        html_content=f"Hey {name}, your registration is successfully completed. Thanks for choosing our website.",
                        to_email=mail,
                    )
                except Exception as e:
                    traceback.print_exc()

                return HttpResponseRedirect(reverse('homepage'))
            else:
                showmsg['unsuccess'] = "Already registerd"
                

    d = {'CO':CO , 'showmsg':showmsg}
        
    return render(request , 'insert_trainer.html' , d)


def insert_student(request):
    error = {}
    QSCO = Course.objects.all()
    d = {'QSCO':QSCO , 'error':error}
    image = request.session['crop_image'] = True
    if request.method == 'POST':
        fullname = request.POST['sfn']
        email = request.POST['se']
        mobile = request.POST['smbn']
        dob = request.POST['dob']
        gender = request.POST['gn']
        age = request.POST['age']
        address = request.POST['ad']
        username = request.POST['un']
        password = request.POST['pw']
        confirmpw = request.POST['cpw']
        course = request.POST.get('course')
        trainer = request.POST.get('tnrs')
        profile = request.FILES.get('profile')
        CO = Course.objects.get(cid = course)
        TO = Trainer.objects.get(tid = trainer)
        encspw = make_password(password)
        print(CO)
        TSO = Student.objects.get_or_create(fullname = fullname , semail = email , phoneno = mobile , 
        dateofbirth = dob , gender = gender , sage = age , address = address , username = username , 
        spassword = encspw , profile_pic = profile )
        TSO[0].cid.add(CO)
        TSO[0].tid.add(TO)
        if TSO[1]:
            error['success'] = "Registration successfully completed"
            try:
                send_brevo_email(
                    subject="Registration",
                    html_content=f"Hey {username}, Your registration is successfully completed. Thank you for choosing our website.",
                    to_email=email,
                )
            except Exception as e:
                print("MAIL ERROR : " , repr(e))

            return HttpResponseRedirect(reverse('homepage'))
        else:
            error['fail'] = "Entered details already exist"
    
    return render (request , 'insert_student.html' , d )


def get_trainers(request , id):
    TO = Trainer.objects.filter(cid = id)
    print(TO)
    trainer_list = []
    for tnrs in TO:
        trainer_list.append({'tid':tnrs.tid , 'tname':tnrs.tname})

    return JsonResponse({"trainer":trainer_list})

def signin_student(request):
    error = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pw']
        
        SO = Student.objects.filter(semail = email).first()
        if not SO:
            error['emailmatch'] = "Email doesnot match"
        else:
            if not check_password(password , SO.spassword):
                error['pwmatch'] = "Password doesnot match"
        if error:
            return render(request , "signin_student.html" , {'error':error} )
        
        if SO:
            request.session['sid'] = SO.sid
            return HttpResponseRedirect(reverse("student_dashboard"))
        else:
            return render(request , "signin_student.html")
    
    return render(request , 'signin_student.html')

@cache_control(no_cache = True , must_revalidate = True , no_store = True)
@never_cache
def student_dashboard(request):
    std = request.session.get('sid')
    
    if std:
        so = Student.objects.get(sid = std)
        crslen = so.cid.count()
        tnrlen = so.tid.count()
        so.profile_pic
    else:
        return HttpResponseRedirect(reverse('homepage'))

    d = {'so':so , 'crslen':crslen , 'tnrlen':tnrlen}
    return render(request , 'student_dashboard.html' , d)

def student_edit_profile(request):
    errorshow = {}
    sid = request.session.get('sid')
    if sid:
        so = Student.objects.get(sid = sid)
    else:
        return redirect('student_dashboard')

    if request.method == "POST":
        sfn = request.POST['sfn']
        un = request.POST['un']
        se = request.POST['se']
        phno = request.POST['phno']
        add = request.POST['add']
        dob = request.POST['dob']
        pic = request.FILES.get('profile')
        age = request.POST['age']
        if age:
            sAge = int(age)
        if phno:
            phoneno = int(phno)

            SUO = Student.objects.filter(sid = sid).update(fullname = sfn , username = un , semail = se , 
            phoneno = phoneno , address = add , sage = sAge , dateofbirth = dob , profile_pic = pic)
            if pic:
                if so.profile_pic:
                    so.profile_pic.delete(save = False)
                so.profile_pic = pic
                so.save()
            if SUO:
                errorshow['success'] = "Your details are updated successfully"
            else:
                errorshow['fail'] = "Your details are not updated"
    
    return render(request , 'student_edit_profile.html' , {'so':so , 'errorshow':errorshow})

def student_change_pw(request):
    dismsg = {}
    sid = request.session.get('sid')
    if sid:
        so = Student.objects.filter(sid = sid)
    else:
        return redirect('student_dashboard')
    
    if request.method == "POST":
        oldpw = request.POST['ctpw']
        newpw = request.POST['npw']
        confirmpw = request.POST['cmpw']
        encnewpw = make_password(newpw)
        SPUO = Student.objects.filter(sid = sid).update(spassword = encnewpw)
        if SPUO:
            dismsg['success'] = "Password is updated successfully"
        else:
            dismsg['fail'] = "Password is not updated please try again"

    return render(request , 'student_change_pw.html' , {'dismsg':dismsg})

def otp_sent(request):
    error = {}
    if request.method == "POST":
        email = request.POST['mail']
        if email:
            so = Student.objects.filter(semail = email )
            if so:
                otp = ""
                for n in range(6):
                    otp += str(random.randint(0,9))
                request.session['otp'] = otp
                request.session['email'] = email
                error['email'] = email
                error['showotp'] = True
                try:
                    send_brevo_email(
                    subject="Your OTP for forgot password",
                        html_content=otp,
                        to_email=email,
                    )
                except Exception as e:
                    print("MAIL ERROR : " , repr(e))
            else:
                error['mailerror'] = "Email does not match"

    return render(request , 'student_forgot_pw.html' , {'error':error})

def otp_verify(request):
    display = {}
    
    if request.method == "POST":
        enteredOTP = request.POST['otp']
        mainotp = request.session.get('otp')
        display['showotp'] = True
        if mainotp == enteredOTP:
            display['verified'] = "OTP verification completed"
            display['showpw'] = True
            display['otp'] = enteredOTP
        else:
            display['notverified'] = "Invalid OTP entered"
    
    return render(request , 'student_forgot_pw.html' , {'display':display})

def password_validate(request):
    msg = {}
    
    if request.method == "POST":
        newpw = request.POST['newpw']
        mail = request.session.get('email')
        encnewpw = make_password(newpw)
        spuo = Student.objects.filter(semail = mail).update(spassword = encnewpw)
        if spuo:
            msg['updated'] = "Your password is updated"
            request.session.flush()
            return redirect('signin_student')
        else: 
            msg['notupdated'] = "Password updation failed"

    return render(request , 'student_forgot_pw.html' , {'msg':msg})

def student_browse_course(request):
    std = request.session.get('sid')
    if std:
        lco = Course.objects.all()
        d = {'lco':lco}
    else:
        return redirect('homepage')

    return render(request , 'student_browse_course.html' , d)

def enroll_courses(request):
    co = Course.objects.all()
    std = request.session.get("sid")
    if std:
        so = Student.objects.get(sid = std)

    else:
        return redirect('homepage')
    d = {'co' : co , 'std':std}
    return render(request , 'enroll_courses.html' , d)

def payment(request , id):
    sid = request.session.get('sid')
    if sid:
        so = Student.objects.get(sid = sid)
        co = Course.objects.get(cid = id)
        if request.method != "POST":
            return redirect('enroll_courses')
        tnr = request.POST.get('tnr')
        to = Trainer.objects.get(tid = tnr)
        request.session['cid'] = id
        request.session['tid'] = to.tid
        client = razorpay.Client( auth = (settings.RAZORPAY_KEY_ID , settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            "amount":int(co.price * 100) , 
            "currency":'INR'
        })
        print(order)
    else:
        return redirect('signin_student')

    return render(request , 'payment.html' , {'so':so , 'co':co , 'to':to , 'order_id':order['id'] , 
    'amount':order['amount'] , 'key':settings.RAZORPAY_KEY_ID})

def payment_success(request):
    std = request.session.get('sid')
    if std:
        so = Student.objects.get(sid = std)
        cid = request.session.get('cid')
        tid = request.session.get('tid')
        co = Course.objects.get(cid = cid)
        to = Trainer.objects.get(tid = tid)
        if request.method == "POST":
            payment_id = request.POST.get("payment_id")
            order_id = request.POST.get("order_id")
            signature = request.POST.get("signature")

            client = razorpay.Client( auth = (settings.RAZORPAY_KEY_ID , settings.RAZORPAY_KEY_SECRET))

            try:
                client.utility.verify_payment_signature({
                    'razorpay_order_id': order_id , 
                    'razorpay_payment_id':payment_id , 
                    'razorpay_signature':signature
                })
                so.cid.add(co)
                so.tid.add(to)

                po = Payment.objects.create(course = co , student = so , amount = co.price , order_id = order_id ,
                payment_id = payment_id , status = "success")

                messages.success(request , "Enrollment successfully completed")
                return HttpResponseRedirect(reverse('student_dashboard'))
            except Exception as e:
                print(e)
                messages.error(request , "payment verification failed")
                return HttpResponseRedirect(reverse('student_dashboard'))

    return HttpResponseRedirect(reverse('student_dashboard'))
            
def my_courses(request):
    sid = request.session.get('sid')
    if sid:
        so = Student.objects.get(sid = sid)
    else:
        return redirect('student_dashboard')
    scl = so.cid.all()
    d = {'scl':scl}
    return render(request , 'my_courses.html' , d)

def my_course_content(request , id):
    std = request.session.get('sid')
    if std:
        so = Student.objects.get(sid = std)
        sco = Course.objects.get(cid = id )
        cvo = CourseContent.objects.filter(course = sco).exclude(video = "")
        cpo = CourseContent.objects.filter(course = sco).exclude(pdf = '')
        vc = cvo.count() #total videos count
        pco = Progress.objects.filter(student = so , content__course = sco ,
         completed = True).values_list('content_id' , flat = True)
        cc = pco.count() #watched videos count
        print(cc)
        pro_cal = cc/vc*100
        print(pro_cal)
        progress_bar = int(pro_cal)
        for cv in cvo:
            cv.video_url = get_drive_file_url(cv.video)
        
    else:
        return redirect('homepage')

    d = {'sco':sco , 'cvo':cvo , 'cpo':cpo , 'vc':vc , 'pco':pco , 'cc':cc ,  'progress_bar':progress_bar}
    return render(request , 'my_course_content.html' , d)

def save_progress(request):
    std = request.session.get('sid')
    if std:
        so = Student.objects.get(sid = std)
        data = json.loads(request.body)
        id = data['content_id']
        contentID = id
        print(contentID)
        cco = CourseContent.objects.get(id = contentID)
        po = Progress.objects.get_or_create(student = so , content = cco)
        if po:
            po[0].completed = True
            po[0].completed_at = timezone.now()
            po[0].save()

    print("request received")
    print(request.method)
    print(request.body)
    return JsonResponse({"status":"progress saved"})

def certificate(request , id):
    sid = request.session.get('sid')
    if sid:
        so = Student.objects.get(sid = sid)
        co = Course.objects.get(cid = id)
        issuedate = date.today
        print(date)
        print(co)
        print(so)
    d = {'so':so , 'co':co , 'issuedate':issuedate}
    return render(request , 'certificate.html' , d)

def download_certificate(request , id):
    sid = request.session.get('sid')
    if sid:
        so = Student.objects.get(sid = sid)
        co = Course.objects.get(cid = id)
        certificate_obj = Certificate.objects.filter(student = so , course = co).first()
        if certificate_obj:
            return FileResponse(certificate_obj.file.open("rb") , as_attachment = True ,
             filename = f"{so.fullname}_certificate.png")
        else:
            image = Image.open('static/images/certificate.png')
            draw = ImageDraw.Draw(image)
            nameFont = ImageFont.truetype(r"C:\Windows\Fonts\ITCEDSCR.ttf" , 70)
            courseFont = ImageFont.truetype( r"C:\Windows\Fonts\georgia.ttf" , 45)
            dateFont = ImageFont.truetype( r"C:\Windows\Fonts\georgia.ttf" , 25)
            draw.text((610 , 440) , so.fullname , fill = "black" , font = nameFont)
            draw.text((680 , 590) , co.cname , fill = 'white' , font = courseFont)
            draw.text((1050 , 850) , date.today().strftime("%d-%m-%Y") , fill = 'black' , font = dateFont)
            path = f"media/certificates/{so.fullname}_{co.cname}.png"
            image.save(path)
            ico = Certificate()
            ico.certificate_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"
            ico.student = so
            ico.course = co
            with open (path , "rb") as f:
                ico.file.save(f"{so.fullname}_{co.cname}.png" , File(f))
            ico.save()

            return FileResponse(open(path , "rb") , as_attachment = True ,
             filename = f"{so.fullname}_{co.cname}_certificate.png")

def student_logout(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('homepage'))


def signin_trainer(request):
    display = {}
    if request.method == 'POST':
        email = request.POST['te']
        tpw = request.POST['pw']
        TO = Trainer.objects.filter(temail = email ).first()
        if not TO:
            display['email'] = "Email doesnot match"
        else:
            if not check_password(tpw , TO.tpassword):
                display['password'] = "Password doesnot match"
        if display:
            return render(request , 'signin_trainer.html' , {'display':display})

        if TO:
            request.session['tid'] = TO.tid
            return HttpResponseRedirect(reverse('trainer_dashboard'))
        else:
            return render(request , 'signin_trainer.html')    
    
    return render(request , 'signin_trainer.html')



@cache_control(no_cache = True , must_revalidate = True , no_store = True)
@never_cache
def trainer_dashboard(request):
    tid = request.session.get('tid')
    if tid:
        to = Trainer.objects.get(tid = tid) 
        lencrs = to.cid.count()
        lenstd = to.student_set.count()
        sn = to.student_set.all()
        d = {'to':to , 'lencrs': lencrs , 'lenstd':lenstd , 'sn':sn}
        
    else:
        return HttpResponseRedirect(reverse('homepage'))
    
    return render(request , 'trainer_dashboard.html' , d)

def edit_trainer_profile(request):
    message = {}
    tid = request.session.get('tid')
    if tid:
        to = Trainer.objects.get(tid = tid)
    else:
        return HttpResponseRedirect(reverse('trainer_dashboard'))
    if request.method == "POST":  
        name = request.POST['nm']
        mail = request.POST['email']
        spe = request.POST['spe']
        exp = request.POST['exp']
        sal = request.POST['sal']
        pic = request.FILES.get('pic')
        
        if name == "":
            message['name'] = "please enter the name"
        if mail == "":
            message['mail'] = "please enter the email"
        if spe == "":
            message['spe'] = "please enter the specialization"
        if exp == "":
            message['exp'] = "please enter the experience"
        if sal == "":
            message['sal'] = "please enter the salary"
        else:
            salary = int(sal)
            UTO = Trainer.objects.filter(tid = tid).update(tname = name , temail = mail , specializtion = spe ,
                    experience = exp , tsal = salary , profile_pic = pic)
            if pic:
                if to.profile_pic:
                    to.profile_pic.delete()
                to.profile_pic = pic
                to.save()
            if UTO:
                message['updated'] = "your details are updated successfully"
            else:
                message['error'] = "Your details are not updated"

    d = {'to':to , 'message':message}
    return render(request , 'edit_trainer_profile.html' , d)


def trainer_change_pw(request):
    dismsg = {}
    tpw = request.session.get('tid')
    if tpw:
        tp = Trainer.objects.get(tid = tpw)
    else:
        return HttpResponseRedirect(reverse('trainer_dashboard'))
    if request.method == 'POST':
        ctpw = request.POST['ctpw']
        npw = request.POST['npw']
        cmpw = request.POST['cmpw']
        encnpw = make_password(npw)
        TPO = Trainer.objects.filter(tid = tp.tid , tpassword = ctpw).update(tpassword = encnpw)
        if TPO:
            dismsg['updated'] = "Password changed successfully"
        else:
            dismsg['notupdated'] = "Your password is not updated"
    d = {'dismsg':dismsg}

    return render(request , 'trainer_change_pw.html' , d)

def send_otp(request):
    error = {}
    if request.method == "POST":
        email = request.POST['mail']
        if email:
            to = Trainer.objects.filter(temail = email )
            if to:
                otp = ""
                for n in range(6):
                    otp += str(random.randint(0,9))
                request.session['otp'] = otp
                request.session['email'] = email
                error['email'] = email
                error['showotp'] = True

                try:   
                   send_brevo_email(
                        subject="Your OTP for forgot password",
                        html_content=otp,
                        to_email=email,
                    )
                except Exception as e:
                    print("MAIL ERROR : " , repr(e))
            else:
                error['mailerror'] = "Email does not match"

    return render(request , 'trainer_forgot_pw.html' , {'error':error})

def verify_otp(request):
    display = {}
    if request.method == "POST":
        enteredOTP = request.POST['otp']
        mainotp = request.session.get('otp')
        display['showotp'] = True
        if mainotp == enteredOTP:
            display['verified'] = "OTP verification completed"
            display['showpw'] = True
            display['otp'] = enteredOTP
        else:
            display['notverified'] = "Invalid OTP entered"
    
    return render(request , 'trainer_forgot_pw.html' , {"display":display})

def validate_password (request):
    msg = {}
    if request.method == "POST":
        newpw = request.POST['newpw']
        mail = request.session.get('email')
        print(mail)
        msg['email'] = mail
        encnewpw = make_password(newpw)
        tpuo = Trainer.objects.filter(temail = mail).update(tpassword = encnewpw)
        if tpuo:
            msg['updated'] = "Your password is updated"
            request.session.flush()
            return redirect('signin_trainer')
        else: 
            msg['notupdated'] = "Password updation failed"
            
    return render(request , 'trainer_forgot_pw.html' , {'msg':msg})

def trainer_logout(request):

    logout(request)

    request.session.flush()

    return HttpResponseRedirect(reverse('homepage'))


def add_course_content(request):
    tid = request.session.get('tid')
    if tid:
        to = Trainer.objects.get(tid = tid)
        tco = to.cid.all()
        d = {'tco':tco}
        if request.method == "POST":
            ct = request.POST['ct']
            video = request.FILES.get('video')
            pdf = request.FILES.get('pdf')
            
            scrs = request.POST['sc']
            video_id = ""
            pdf_id = ""
            if video:
                video_id = upload_file_to_drive(video)
            if pdf:
                pdf_id = upload_file_to_drive(pdf)
            if scrs:
                sco = Course.objects.get(cid = scrs)
                to = Trainer.objects.get(tid = tid)
            
                CCO = CourseContent.objects.get_or_create(course = sco , title = ct , video = video_id , pdf = pdf_id ,
                 uploaded_by = to)
                if CCO[1]:
                    d['success'] = "Content uploaded successfully"
                else:
                    d['fail'] = "Content Upload failed"
    else:
        return redirect('homepage')
    
    return render(request , 'add_course_content.html' , d)

def display_course_content(request):
    tid = request.session.get('tid')
    if tid:
        
        to = Trainer.objects.get(tid = tid)
        lco = to.cid.all()
        cco = CourseContent.objects.filter(course__in = lco).exclude(pdf = "")
        pdfcount = cco.count()

        lcvo = CourseContent.objects.filter(course__in = lco ).exclude(video = "")
        videocount = lcvo.count()
    else:
        return redirect('homepage')
    
    d = {'cco':cco , 'pdfcount':pdfcount , 'lcvo':lcvo , 'videocount':videocount }
    return render(request , 'display_course_content.html' , d)

def search_content(request):
    qscco = CourseContent.objects.all() 
    return JsonResponse({'content':qscco})

def view_video(request , id):
    tid = request.session.get('tid')
    if tid:
        cvo = CourseContent.objects.get(id = id) 
        if cvo.video:
            cvo.video_url = get_drive_file_url(cvo.video)
        print(cvo.video_url)
    else:
        return redirect('homepage')

    d = {'cvo':cvo}
    return render(request , 'view_video.html' , d)

def delete_video(request):
    data = json.loads(request.body)
    vid_id = data['content_id']


    try:
        co = CourseContent.objects.get(id=vid_id)
    except CourseContent.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Content not found"}, status=404)

    # delete video from Drive
    if co.video:
        deleted = delete_file_from_drive(co.video)
        if not deleted:
            return JsonResponse({"status": "error", "message": "Failed to delete video from Drive"}, status=500)

    # delete pdf from Drive too, if present
    if co.pdf:
        deleted_pdf = delete_file_from_drive(co.pdf)
        if not deleted_pdf:
            return JsonResponse({"status": "error", "message": "Failed to delete PDF from Drive"}, status=500)

    co.delete()

    return JsonResponse({"status": "success"})