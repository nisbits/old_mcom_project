from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
import datetime 

# 


# Create your models here.
class DPR_table1(models.Model):
    id=models.CharField(max_length = 100,primary_key=True)
    SITE_ID=models.CharField(max_length = 100)
    CIRCLE=models.CharField(max_length = 100)
    Unique_SITE_ID=models.CharField(max_length = 100)
    BAND=models.CharField(max_length = 100)
    TOCO_NAME=models.CharField(max_length=255)
    OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=models.CharField(max_length = 100)
    Project =models.CharField(max_length = 100)
    Activity=models.CharField(max_length = 100)
    # uploaded_date= models.DateTimeField( auto_now_add=True)
   
    Soft_AT_Status=models.CharField(max_length=100,null=True,blank=True)

    SOFT_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    SOFT_AT_ACCEPTANCE_MAIL=models.FileField(upload_to="dpr/dpr_acceptance_mail/soft_at/",null=True,blank=True)
    
    SOFT_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    SOFT_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # SOFT_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    SOFT_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    SOFT_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    
    SOFT_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    SOFT_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    SOFT_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    PHYSICAL_AT_Status=models.CharField(max_length=100,null=True,blank=True)
    
    PHYSICAL_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PHYSICAL_AT_ACCEPTANCE_MAIL=models.FileField(upload_to="dpr/dpr_acceptance_mail/physical_at/",null=True,blank=True)
    
    PHYSICAL_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PHYSICAL_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # PHYSICAL_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    PHYSICAL_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PHYSICAL_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    
    PHYSICAL_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    PHYSICAL_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    PHYSICAL_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    



    Performance_AT_Status=models.CharField(max_length=100,null=True,blank=True)
    
    
    PERFORMANCE_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    # PERFORMANCE_AT_ACCEPTANCE_MAIL=models.FileField(upload_to="dpr/dpr_acceptance_mail/performance_at/",null=True,blank=True)
    
    PERFORMANCE_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # PERFORMANCE_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True)
    
    PERFORMANCE_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)
    
    PERFORMANCE_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])

    MAPA_STATUS=models.CharField(max_length=100,null=True,blank=True,default="NOT OK")
    
    def __str__ ( self ) :
        return str(self.SITE_ID)
   
class DPR_file(models.Model):
   
    dpr_file=models.FileField(upload_to="dpr_files/")
    uploaded_date= models.DateTimeField( auto_now_add=True)
    
    def __str__ ( self ) :
        return str(self.dpr_file)


class DPR_update_status(models.Model):
   

    id=models.CharField(max_length = 100,primary_key=True)
    SITE_ID = models.CharField(max_length = 100)
    update_status=models.CharField(max_length=100,null=True,blank=True)
    Remark=models.TextField(max_length=100,null=True,blank=True)

    
    def __str__ ( self ):
        return str(self.SITE_ID)

class performance_at_table(models.Model):

    key= models.ForeignKey(DPR_table1, max_length = 100, on_delete=models.CASCADE)
    band=models.CharField(max_length=100,blank=True)
    Performance_AT_Status=models.CharField(max_length=100,blank=True)
    PERFORMANCE_AT_ACCEPTANCE_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    
    PERFORMANCE_AT_ACCEPTANCE_MAIL=models.FileField(upload_to="dpr/dpr_acceptance_mail/performance_at/",null=True,blank=True)
   
    PERFORMANCE_AT_REJECTION_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_REJECTION_REASON=models.TextField(max_length=100,null=True,blank=True)
    # PERFORMANCE_AT_REJECTED_TAT_DATE=models.DateField(null=True,blank=True)

    PERFORMANCE_AT_OFFERED_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    PERFORMANCE_AT_OFFERED_REMARKS=models.TextField(max_length=100,null=True,blank=True)

    PERFORMANCE_AT_PENDING_REASON=models.TextField(max_length=100,null=True,blank=True)
    PERFORMANCE_AT_PENDING_REMARK=models.TextField(max_length=100,null=True,blank=True)
    # PERFORMANCE_AT_PENDING_TAT_DATE=models.DateField(null=True,blank=True,validators=[MaxValueValidator(datetime.date.today())])
    # overall
    def __str__ ( self ) :
        return  str(self.band)