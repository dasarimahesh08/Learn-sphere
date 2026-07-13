from django.db import models

# Create your models here


class Course(models.Model):
    cid = models.IntegerField(primary_key = True)
    cname = models.CharField(max_length = 20 , unique = True)
    description = models.CharField(max_length = 200)
    price = models.IntegerField()
    duration = models.CharField(max_length = 20)
    cimage = models.ImageField(upload_to = 'course_images')
    

    def __str__(self):
        return self.cname

class Trainer(models.Model):
    tid = models.AutoField(primary_key = True)
    tname = models.CharField(max_length = 30)
    tsal = models.IntegerField()
    temail = models.EmailField(max_length = 40 , unique = True )
    experience = models.CharField(max_length = 40)
    specializtion = models.CharField(max_length = 20)
    tpassword = models.CharField()
    profile_pic = models.ImageField(upload_to = 'trainer_images' , null = True , blank = True)
    cid = models.ManyToManyField(Course)
    dateofjoined = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.tname

class Student(models.Model):
    sid = models.AutoField(primary_key = True)
    fullname = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30 , unique = True)
    dateofbirth = models.DateField()
    address = models.CharField(max_length = 200)
    sage = models.IntegerField()
    gender = models.CharField(max_length = 10)
    phoneno = models.CharField(max_length=10 , unique = True)
    semail = models.EmailField(max_length = 40 , unique = True)
    spassword = models.CharField()
    profile_pic = models.ImageField(upload_to = 'student_images' , null = True , blank = True)
    tid = models.ManyToManyField(Trainer)
    cid = models.ManyToManyField(Course)
    dateofjoined = models.DateField(auto_now_add = True)
    
    def __str__(self):
        return self.fullname

class CourseContent(models.Model):
    course = models.ForeignKey(Course , on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    video = models.CharField(max_length = 100 , null = True , blank = True)
    pdf = models.CharField(max_length = 100 , null = True , blank = True)
    upload_date = models.DateField(auto_now_add = True) 
    uploaded_by = models.ForeignKey(Trainer , on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.title)

class Progress(models.Model):
    student = models.ForeignKey(Student , on_delete = models.CASCADE)
    content = models.ForeignKey(CourseContent , on_delete = models.CASCADE)
    completed = models.BooleanField(default = False)
    completed_at = models.DateTimeField(null = True , blank = True)

    class Meta:
        unique_together = ['student' , 'content']

    def __str__(self):
        return str(self.student) + ' ' + str(self.content)
class Certificate(models.Model):
    student = models.ForeignKey(Student , on_delete = models.CASCADE)
    course = models.ForeignKey(Course , on_delete = models.CASCADE)
    certificate_id = models.CharField(max_length = 20 , unique = True)
    issuedate = models.DateField(auto_now_add = True)
    file = models.FileField(upload_to = 'certificates' , blank = True , null = True)

    def __str__(self):
        return self.certificate_id

class Payment(models.Model):
    student = models.ForeignKey(Student , on_delete = models.CASCADE)
    course = models.ForeignKey(Course , on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits = 10 , decimal_places = 2)
    order_id = models.CharField(max_length = 50)
    payment_id = models.CharField(max_length = 50 , null = True , blank = True)
    status = models.CharField(max_length = 30 , default = 'pending')
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return str(self.course) + ' ' + str(self.amount)