from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import dpr_upload_form
from .models import DPR_file
import pandas as pd
from .models import DPR_table1,DPR_update_status,performance_at_table
from django.contrib import messages
from .forms import soft_at_acceptance,soft_at_offered,soft_at_pending,soft_at_rejection
from .forms import physical_at_acceptance,physical_at_offered,physical_at_pending,physical_at_rejection
from .forms import performance_at_acceptance,performance_at_offered,performance_at_pending,performance_at_rejection
from django.contrib.auth.decorators import login_required
from mcom_website.settings import MEDIA_URL,BASE_DIR
import numpy as np
import os
from datetime import datetime



# from rest_framework.decorators import api_view
# from rest_framework.response import Response


# Create your views here
            # for i in range(df.shape[0]):
            #     pk=str(df.loc[i]["SITE_ID"]+df.loc[i]["BAND"])
            #     obj=DPR_table1(id=pk,
            #                                 SITE_ID=str(df.loc[i]["SITE_ID"]),
            #                                 CIRCLE=str(df.loc[i]["CIRCLE"]),
            #                                 Unique_SITE_ID=str(df.loc[i]["Unique_SITE_ID"]),
            #                                 BAND=str(df.loc[i]["BAND"]),
            #                                 TOCO_NAME=str(df.loc[i]["TOCO_NAME"]),
            #                                 OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=df.loc[i]["OA_(COMMERCIAL_TRAFFIC_PUT_ON_AIR)_(MS1)_DATE"],
            #                                 Project=str(df.loc[i]["Project"]),
            #                                 Activity=str(df.loc[i]["Activity"]),
            #                                 )
            #     objs.append(obj)        


def circle_list(objs):
    cir=[]
    
    for obj in objs:
        cir.append(obj.CIRCLE)

    cir_set=set(cir)
    cir=list(cir_set)
    return cir



def index(request):
    
    
    return render(request,"trend/base.html")

# def upload_dpr_file(request):
#     if request.method=="POST":
#         form=dpr_upload_form(request.POST,request.FILES)
#         if form.is_valid():
#             dpr=form.cleaned_data["dpr_file"]
            
#             form.save()
#             print(dpr)
#             print("image saved")
#             return HttpResponse("uploaded")
#     form=dpr_upload_form()
#     return render(request,"trend/DPR_upload.html",{'form':form})


# @login_required(login_url="/accounts/login/")
def dpr_key_upload(request):
    if request.method=="POST":
            DPR_file.objects.all().delete()
            file=request.FILES["myfile"]
            obj=DPR_file.objects.create(dpr_file=file)
            path=str(obj.dpr_file)
            print(path)
            df=pd.read_excel("media/"+path)
            print(df)
            del_obj=[]
            if not(df.empty):
                for d in df.values:
                        pk=str(d[0])+str(d[2])+str(d[3])+str(d[4])+str(d[6])+str(d[7])
                        
                        try:
                            obj=DPR_table1.objects.create(id=pk,
                                            SITE_ID=str(d[1]),
                                            CIRCLE=str(d[0]),
                                            Unique_SITE_ID=str(d[2]),
                                            BAND=str(d[3]),
                                            TOCO_NAME=str(d[4]),
                                            OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=d[5],
                                            Project=str(d[6]),
                                            Activity=str(d[7]),
                                            )
                            bands=str(d[3]).split("_")
                            print(bands)
                            for band in bands:
                                performance_at_table.objects.create(key=obj,band=band)

                            del_obj.append(obj)
                            print("obj created",obj)
                        except:
                            for o in del_obj:
                                o.delete()
                                print("obj deleted",o)
                            messages.warning(request, 'Could not upload,Site id are not unique')
                            break
                else:   
                        messages.success(request, 'DPR is Succesfully uploaded')
                        print("Loop Ended without break")
            else:
                    messages.warning(request, 'Coluld not upload,DPR is empty')
    path="media/dpr/dpr_templates/DPR_KEY_TEMP.xlsx"
    context={"path":path}
    return render(request,"trend/DPR_upload.html",context)                



# @login_required(login_url="/accounts/login/")
# def upload_dpr_file(request):
#     if request.method=="POST":
#         file=request.FILES["myfile"]
#         obj=DPR_file.objects.create(dpr_file=file)
#         path=str(obj.dpr_file)
#         print(path)
#         df=pd.read_excel("media/"+path)
#         print(df)
#         # df["SITE_ID"]=df["SITE_ID"].values.astype(str)
#         objs=[]
#         if not(df.empty):
#             for d in df.values:
#                 pk=str(d[1])+str(d[3])
#                 obj=DPR_table1(id=pk,
#                                 SITE_ID=str(d[1]),
#                                 CIRCLE=str(d[0]),
#                                 Unique_SITE_ID=str(d[2]),
#                                 BAND=str(d[3]),
#                                 TOCO_NAME=str(d[4]),
#                                 OA_COMMERCIAL_TRAFFIC_PUT_ON_AIR_MS1_DATE=d[5],
#                                 Project=str(d[6]),
#                                 Activity=str(d[7]),
#                                 )
#                 objs.append(obj)
#                 print(obj)
#             status=True
#             for i in range(0,len(objs)-1):
#                 print("inside for",i)
#                 for j in range(i+1,len(objs)):
#                     if objs[i]==objs[j]:
#                         messages.warning(request, 'Could not upload,Site id are not unique')
#                         status=False
#                         return render(request,"trend/DPR_upload.html",)
#             if status==True:
#                 for obj in objs:
#                     obj.save()  
#                 messages.success(request, 'DPR is Succesfully uploaded')
#         else:
#             messages.warning(request, 'Coluld not upload,DPR is empty')
#     return render(request,"trend/DPR_upload.html",)


@login_required(login_url="/accounts/login/")
def dpr_site_list(request):
    
    if "id search" in request.GET:
        search=request.GET["id search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(SITE_ID__iexact = search)
    elif "circle search" in request.GET:
        search=request.GET["circle search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(CIRCLE__iexact = search)
    
    elif "activity search" in request.GET:
        search=request.GET["activity search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(Activity__iexact = search)
    
    elif "project search" in request.GET:
        search=request.GET["project search"]
        # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
        obj=DPR_table1.objects.filter(Project__iexact = search)

    else:
        obj=DPR_table1.objects.all()

    context={"object":obj}

    return render(request,"trend/DPR_site_list.html",context)


@login_required(login_url="/accounts/login/")
def single_site_view(request,pk):
    object=DPR_table1.objects.get(id=pk)
    bands=object.BAND
    band_list=bands.split("_")
    context={"object":object,"band_list":band_list}
    return render(request,"trend/single_site_view.html",context)
@login_required(login_url="/accounts/login/")
def soft_at_update(request,pk,at_status):

        if at_status=="ACCEPTED":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=soft_at_acceptance(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Soft_AT_Status=at_status
                    ins.SOFT_AT_REJECTION_DATE = None
                    ins.SOFT_AT_REJECTION_REASON= ""
                    # ins.SOFT_AT_REJECTED_TAT_DATE= None
                    ins.SOFT_AT_OFFERED_DATE= None
                    ins.SOFT_AT_OFFERED_REMARKS= ""
                    ins.SOFT_AT_PENDING_REASON= ""
                    ins.SOFT_AT_PENDING_REMARK= ""
                    ins.SOFT_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =soft_at_acceptance(instance=ins)
            return render(request, 'trend/form.html',{'form':form})
                
        if at_status=="REJECTED":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=soft_at_rejection(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Soft_AT_Status=at_status

                    ins.SOFT_AT_ACCEPTANCE_DATE=None
                    ins.SOFT_AT_ACCEPTANCE_MAIL=""
                    
                    ins.SOFT_AT_OFFERED_DATE= None
                    ins.SOFT_AT_OFFERED_REMARKS= ""
                    ins.SOFT_AT_PENDING_REASON= ""
                    ins.SOFT_AT_PENDING_REMARK= ""
                    ins.SOFT_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =soft_at_rejection(instance=ins)
            return render(request, 'trend/form.html',{'form':form})
        if at_status=="OFFERED":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=soft_at_offered(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Soft_AT_Status=at_status
                    
                    ins.SOFT_AT_ACCEPTANCE_DATE=None
                    ins.SOFT_AT_ACCEPTANCE_MAIL=""
                    ins.SOFT_AT_REJECTION_DATE = None
                    ins.SOFT_AT_REJECTION_REASON=""
                    # ins.SOFT_AT_REJECTED_TAT_DATE= None
                    
                    ins.SOFT_AT_PENDING_REASON= ""
                    ins.SOFT_AT_PENDING_REMARK= ""
                    ins.SOFT_AT_PENDING_TAT_DATE= None
                    
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =soft_at_offered(instance=ins)
            return render(request, 'trend/form.html',{'form':form})
        if at_status=="PENDING":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=soft_at_pending(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Soft_AT_Status=at_status

                    ins.SOFT_AT_ACCEPTANCE_DATE=None
                    ins.SOFT_AT_ACCEPTANCE_MAIL=""
                    ins.SOFT_AT_REJECTION_DATE = None
                    ins.SOFT_AT_REJECTION_REASON=""
                    # ins.SOFT_AT_REJECTED_TAT_DATE= None
                    ins.SOFT_AT_OFFERED_DATE= None
                    ins.SOFT_AT_OFFERED_REMARKS= ""
                    

                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =soft_at_pending(instance=ins)
            return render(request, 'trend/form.html',{'form':form})


@login_required(login_url="/accounts/login/")        
def physical_at_update(request,pk,at_status):
        if at_status=="ACCEPTED":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=physical_at_acceptance(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.PHYSICAL_AT_Status = at_status
                    
                    ins.PHYSICAL_AT_REJECTION_DATE = None
                    ins.PHYSICAL_AT_REJECTION_REASON =""
                    # ins.PHYSICAL_AT_REJECTED_TAT_DATE=None
                    ins.PHYSICAL_AT_OFFERED_DATE= None
                    ins.PHYSICAL_AT_OFFERED_REMARKS=""
                    ins.PHYSICAL_AT_PENDING_REASON= ""
                    ins.PHYSICAL_AT_PENDING_REMARK= ""
                    ins.PHYSICAL_AT_PENDING_TAT_DATE=None
                    
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =physical_at_acceptance(instance=ins)
            return render(request, 'trend/form.html',{'form':form})
                
        if at_status=="REJECTED":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=physical_at_rejection(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.PHYSICAL_AT_Status=at_status
                    
                    ins.PHYSICAL_AT_ACCEPTANCE_DATE=None
                    ins.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                    
                    
                    ins.PHYSICAL_AT_OFFERED_DATE= None
                    ins.PHYSICAL_AT_OFFERED_REMARKS= ""
                    ins.PHYSICAL_AT_PENDING_REASON= ""
                    ins.PHYSICAL_AT_PENDING_REMARK= ""
                    ins.PHYSICAL_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =physical_at_rejection(instance=ins)
            return render(request, 'trend/form.html',{'form':form})
        if at_status=="OFFERED":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=physical_at_offered(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.PHYSICAL_AT_Status=at_status
                    
                    ins.PHYSICAL_AT_ACCEPTANCE_DATE=None
                    ins.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                    
                    ins.PHYSICAL_AT_REJECTION_DATE = None
                    ins.PHYSICAL_AT_REJECTION_REASON = ""
                    # ins.PHYSICAL_AT_REJECTED_TAT_DATE= None
                    
                    ins.PHYSICAL_AT_PENDING_REASON= ""
                    ins.PHYSICAL_AT_PENDING_REMARK= ""
                    ins.PHYSICAL_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =physical_at_offered(instance=ins)
            return render(request, 'trend/form.html',{'form':form})
        if at_status=="PENDING":
            ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=physical_at_pending(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.PHYSICAL_AT_Status=at_status
                    
                    ins.PHYSICAL_AT_ACCEPTANCE_DATE=None
                    ins.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                    ins.PHYSICAL_AT_Status = at_status
                    ins.PHYSICAL_AT_REJECTION_DATE = None
                    ins.PHYSICAL_AT_REJECTION_REASON = ""
                    # ins.PHYSICAL_AT_REJECTED_TAT_DATE= None
                    ins.PHYSICAL_AT_OFFERED_DATE= None
                    ins.PHYSICAL_AT_OFFERED_REMARKS= ""
                   
                    ins.save()
                    form.save()
                    
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =physical_at_pending(instance=ins)
            return render(request, 'trend/form.html',{'form':form})

def over_all_performance_at_status(pk):
            obj=DPR_table1.objects.get(id=pk)
            ins=performance_at_table.objects.filter(key=obj)
            reason=[]
            for ob in ins:
                if  (ob.Performance_AT_Status ==''):
                    txt=str(ob.band) +"_" + "PENDING"
                    reason.append(txt)
                else:
                    txt=str(ob.band) + "_" + str(ob.Performance_AT_Status)
                    reason.append(txt)
                    
            txt_reason= ",".join(reason)
            accepted_date_list=[]
            rejected_date_list=[]
            
            offered_date_list=[]

            accepted=False
            rejected=False
            pending=False
            offered=False
            for ob in ins:
                # if (not(ob.Performance_AT_Status == None) or not(ob.Performance_AT_Status == '')): 
                if not(ob.Performance_AT_Status ==''): 
                    if ob.Performance_AT_Status == "ACCEPTED" :
                        last_status = ob.Performance_AT_Status
                        accepted_date_list.append(ob.PERFORMANCE_AT_ACCEPTANCE_DATE)
                        accepted=True
                    
                    if ob.Performance_AT_Status == "REJECTED":
                        last_status=ob.Performance_AT_Status
                        
                        rejected_date_list.append(ob.PERFORMANCE_AT_REJECTION_DATE)
                        rejected=True
                       
                    
                    if ob.Performance_AT_Status == "OFFERED":
                        last_status=ob.Performance_AT_Status
                        offered_date_list.append(ob.PERFORMANCE_AT_OFFERED_DATE)
                        
                        offered=True
                        
                    if ob.Performance_AT_Status == "PENDING":
                        last_status=ob.Performance_AT_Status
                        pending=True
                       
                else:
                     last_status="PENDING"
                     pending=True
                     break 
                

            if pending == True:
                    obj.Performance_AT_Status="PENDING"
                   
                    obj.PERFORMANCE_AT_PENDING_REMARK=txt_reason
            else:

                if accepted == True and rejected==True and offered==True:
                    obj.Performance_AT_Status="OFFERED"
                    obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
                    obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
                if accepted == True and rejected==True and offered==False:
                    obj.Performance_AT_Status="REJECTED"
                    obj.PERFORMANCE_AT_REJECTION_DATE=max(rejected_date_list)
                    obj.PERFORMANCE_AT_REJECTION_REASON=txt_reason          
                if accepted == True and rejected==False and offered==False:
                    obj.Performance_AT_Status="ACCEPTED"
                    obj.PERFORMANCE_AT_ACCEPTANCE_DATE=max(accepted_date_list)       
                
                if accepted == False and rejected==True and offered==True:
                    obj.Performance_AT_Status="OFFERED"
                    obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
                    obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason

                if accepted == False and rejected==False and offered==True:
                        obj.Performance_AT_Status="OFFERED"
                        obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
                        obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
                if accepted == True and rejected==False and offered==True:
                        obj.Performance_AT_Status="OFFERED"
                        obj.PERFORMANCE_AT_OFFERED_DATE=max(offered_date_list)
                        obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason

                if accepted == False and rejected==True and offered==False:

                        obj.Performance_AT_Status="REJECTED"
                        obj.PERFORMANCE_AT_REJECTION_DATE=max(rejected_date_list)
                        obj.PERFORMANCE_AT_REJECTION_REASON=txt_reason

            
            # if last_status == "ACCEPTED":
            #     obj.Performance_AT_Status="ACCEPTED"
            #     obj.PERFORMANCE_AT_ACCEPTANCE_DATE=max(date_list)
            
            # if last_status == "REJECTED":
            #     obj.Performance_AT_Status="REJECTED"
            #     obj.PERFORMANCE_AT_REJECTION_DATE=rej_date
            #     obj.PERFORMANCE_AT_REJECTION_REASON=txt_reason
            
            # if last_status == "OFFERED":
            #     obj.Performance_AT_Status="OFFERED"
            #     obj.PERFORMANCE_AT_OFFERED_DATE=ofr_date
            #     obj.PERFORMANCE_AT_OFFERED_REMARKS=txt_reason
           
            # if last_status == "PENDING": 
            #     obj.Performance_AT_Status="PENDING"
            #     # obj.PERFORMANCE_AT_OFFERED_DATE=ofr_date
            #     obj.PERFORMANCE_AT_PENDING_REASON=txt_reason

            # ins.save()
            obj.save()

    


@login_required(login_url="/accounts/login/")
def performance_at_update(request,pk,at_status,band):
        obj=DPR_table1.objects.get(id=pk)
        ins=performance_at_table.objects.get(key=obj,band=band)
        if at_status=="ACCEPTED":
           
            if request.method == 'POST':
                
                form=performance_at_acceptance(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Performance_AT_Status=at_status

                    ins.PERFORMANCE_AT_REJECTION_DATE = None
                    ins.PERFORMANCE_AT_REJECTION_REASON=""
                    # ins.PERFORMANCE_AT_REJECTED_TAT_DATE= None
                    ins.PERFORMANCE_AT_OFFERED_DATE= None
                    ins.PERFORMANCE_AT_OFFERED_REMARKS= ""
                    ins.PERFORMANCE_AT_PENDING_REASON= ""
                    ins.PERFORMANCE_AT_PENDING_REMARK= ""
                    # ins.PERFORMANCE_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    over_all_performance_at_status(pk)
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =performance_at_acceptance(instance=ins)
            context={'form':form,"band":band}
            return render(request, 'trend/form.html',context)
                
        if at_status=="REJECTED":
            # ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=performance_at_rejection(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Performance_AT_Status=at_status

                    ins.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                    # ins.PERFORMANCE_AT_ACCEPTANCE_MAIL=""
                    
                    ins.PERFORMANCE_AT_OFFERED_DATE= None
                    ins.PERFORMANCE_AT_OFFERED_REMARKS= ""
                    ins.PERFORMANCE_AT_PENDING_REASON= ""
                    ins.PERFORMANCE_AT_PENDING_REMARK= ""
                    # ins.PERFORMANCE_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    over_all_performance_at_status(pk)
                    messages.success(request, 'Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =performance_at_rejection(instance=ins)
            context={'form':form,"band":band}
            return render(request, 'trend/form.html',context)
        if at_status=="OFFERED":
            # ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=performance_at_offered(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Performance_AT_Status=at_status

                    ins.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                    # ins.PERFORMANCE_AT_ACCEPTANCE_MAIL=""
                    ins.PERFORMANCE_AT_REJECTION_DATE = None
                    ins.PERFORMANCE_AT_REJECTION_REASON=""
                    # ins.PERFORMANCE_AT_REJECTED_TAT_DATE= None
                   
                    ins.PERFORMANCE_AT_PENDING_REASON= ""
                    ins.PERFORMANCE_AT_PENDING_REMARK= ""
                    # ins.PERFORMANCE_AT_PENDING_TAT_DATE= None
                    ins.save()
                    form.save()
                    over_all_performance_at_status(pk)
                    messages.success(request, ' Status updated successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =performance_at_offered(instance=ins)
            context={'form':form,"band":band}
            return render(request, 'trend/form.html',context)
        if at_status=="PENDING":
            # ins=DPR_table1.objects.get(id=pk)
            if request.method == 'POST':
                
                form=performance_at_pending(request.POST, request.FILES,instance=ins)

                if form.is_valid():
                    ins.Performance_AT_Status=at_status

                    ins.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                    # ins.PERFORMANCE_AT_ACCEPTANCE_MAIL=""
                    ins.PERFORMANCE_AT_REJECTION_DATE = None
                    ins.PERFORMANCE_AT_REJECTION_REASON=""
                    # ins.PERFORMANCE_AT_REJECTED_TAT_DATE= None
                    ins.PERFORMANCE_AT_OFFERED_DATE= None
                    ins.PERFORMANCE_AT_OFFERED_REMARKS= ""
                   
                    ins.save()
                    form.save()
                    over_all_performance_at_status(pk)
                    messages.success(request, 'Status Updated Successfully')
                    return redirect(to='single_site_view',pk=pk)
            else:
                   form =performance_at_pending(instance=ins)
            context={'form':form,"band":band}
            
            return render(request, 'trend/form.html',context)

def performance_at_tat_date(request,pk):
    obj=DPR_table1.objects.get(pk=pk)
    if request.method == 'POST':
    
           obj.PERFORMANCE_AT_PENDING_TAT_DATE=request.POST.get("tat_date")
           obj.save()
    return redirect("single_site_view",pk=pk)



@login_required(login_url="/accounts/login/")   
def dpr_view(request,circle):
           
            if not (circle == "ALL"):
                objs=DPR_table1.objects.filter(CIRCLE=circle)

            else:
                 objs=DPR_table1.objects.all()
            

            if "id search" in request.GET:
                    search=request.GET["id search"]
                    # obj=DPR_table1.objects.filter(SITE_ID__icontains = search)
                    objs=objs.filter(SITE_ID__iexact = search)
            if "MS2 filter" in request.GET:
                    objs= objs.filter( Soft_AT_Status="ACCEPTED").filter(Performance_AT_Status="ACCEPTED").filter(PHYSICAL_AT_Status="ACCEPTED")
                    
                    
                          
            # data=[]
            # for obj in objs:
            #         data.append({
            #             "CIRCLE":obj.CIRCLE,
            #             "SITE_ID":obj.SITE_ID,
            #             "Unique_SITE_ID":obj.Unique_SITE_ID,
            #             "BAND":obj.BAND,
            #             "TOCO_NAME":obj.TOCO_NAME,
            #         })
            # path="media/dpr/dpr_excel/excel.xlsx"
            # pd.DataFrame(data).to_excel(path,index=False)
            path="media/dpr/dpr_excel/excel.xlsx"
            pd.DataFrame(list(objs.values())).to_excel(path,index=False)
            
            context={"object":objs,"circle":circle,"path":path}
            return render(request,"trend/DPR_view.html",context)

def all_dashboard(request):
    obj=DPR_table1.objects.all()
    ms2_site=0
    only_soft_at_done=0
    only_physical_at_done=0
    only_performance_at_done=0
    for o in obj:
            if o.Soft_AT_Status=="ACCEPTED" and o.Performance_AT_Status=="ACCEPTED" and o.PHYSICAL_AT_Status=="ACCEPTED":
                ms2_site=ms2_site+1
            if o.Soft_AT_Status=="ACCEPTED" and o.Performance_AT_Status!="ACCEPTED" and o.PHYSICAL_AT_Status!="ACCEPTED":
                only_soft_at_done=only_soft_at_done+1
            if o.Soft_AT_Status!="ACCEPTED" and o.Performance_AT_Status=="ACCEPTED" and o.PHYSICAL_AT_Status!="ACCEPTED":
                only_performance_at_done=only_performance_at_done+1
            if o.Soft_AT_Status!="ACCEPTED" and o.Performance_AT_Status!="ACCEPTED" and o.PHYSICAL_AT_Status=="ACCEPTED":
                only_physical_at_done=only_physical_at_done+1
    total_no_site=len(DPR_table1.objects.all())

    total_soft_at_done_objs=DPR_table1.objects.filter(Soft_AT_Status="ACCEPTED")
    total_soft_at_done=len( total_soft_at_done_objs)

    
    total_physical_at_done_objs=DPR_table1.objects.filter(PHYSICAL_AT_Status="ACCEPTED")
    total_physical_at_done=len( total_physical_at_done_objs)

    
    total_performance_at_done_objs=DPR_table1.objects.filter(Performance_AT_Status="ACCEPTED")
    total_performance_at_done=len( total_performance_at_done_objs)

    total_mapa=len(obj.filter(MAPA_STATUS="OK"))
    if total_no_site > 0 :
        percent_soft_at_done=round((total_soft_at_done/total_no_site)*100,2)
        percent_physical_at_done=round((total_physical_at_done/total_no_site)*100,2)
        percent_performance_at_done=round((total_performance_at_done/total_no_site)*100,2)
    else:
        percent_soft_at_done=0
        percent_physical_at_done=0
        percent_performance_at_done=0
    if ms2_site>0:
        percent_ms2_site=round((ms2_site/total_no_site)*100,2)

    else:
        percent_ms2_site=0
    context={   "total_soft_at_done":total_soft_at_done,
                "total_performance_at_done":total_performance_at_done,
                "total_physical_at_done": total_physical_at_done,
                "percent_soft_at_done":percent_soft_at_done,
                "percent_physical_at_done":percent_physical_at_done,
                "percent_performance_at_done":percent_performance_at_done,
                "total_no_site":total_no_site,
                "Ms2_site":ms2_site,
                "percent_ms2_site": percent_ms2_site,
                "total_mapa":total_mapa,
                "only_soft_at_done":only_soft_at_done,
                "only_physical_at_done":only_physical_at_done,
                "only_physical_at_done":only_physical_at_done,

                
            }
    
    return render(request, 'trend/DPR_dashboard.html',context)

@login_required(login_url="/accounts/login/")
def circle_wise_dashboard(request):
    
    
    if "project" in request.GET:
        project=request.GET["project"]
        objects=DPR_table1.objects.filter(Project__iexact=project)
        circles=circle_list(objects)
        
    else:
        objects=DPR_table1.objects.all()
        circles=circle_list(objects)
        
    data={}
    for circle in circles:
        ms2_site=0
        obj=objects.filter(CIRCLE__iexact = circle)
        for o in obj:
            if o.Soft_AT_Status=="ACCEPTED" and o.Performance_AT_Status=="ACCEPTED" and o.PHYSICAL_AT_Status=="ACCEPTED":
                ms2_site=ms2_site+1
        total_ms1_site=len(obj)
        total_soft_at_done=len(obj.filter(Soft_AT_Status="ACCEPTED"))
        total_physical_at_done=len(obj.filter(PHYSICAL_AT_Status="ACCEPTED"))
        total_performance_at_done=len(obj.filter(Performance_AT_Status="ACCEPTED"))
        total_mapa=len(obj.filter(MAPA_STATUS="OK"))
        
        if  total_ms1_site > 0 :
            percent_soft_at_done=round((total_soft_at_done/total_ms1_site)*100,2)
            percent_physical_at_done=round((total_physical_at_done/total_ms1_site)*100,2)
            percent_performance_at_done=round((total_performance_at_done/total_ms1_site)*100,2)
        else:
            percent_soft_at_done=0
            percent_physical_at_done=0
            percent_performance_at_done=0
        
        if ms2_site>0:
            percent_ms2_site=round((ms2_site/total_ms1_site)*100,2)

        else:
            percent_ms2_site=0
        data[circle]={ 
                    "total_ms1_site" :total_ms1_site, 
                    "total_soft_at_done" : total_soft_at_done,
                    "total_physical_at_done":  total_physical_at_done,
                    "total_performance_at_done" : total_performance_at_done,
                    "percent_soft_at_done" :percent_soft_at_done,
                    "percent_physical_at_done" :percent_physical_at_done,
                    'percent_performance_at_done' :percent_performance_at_done,
                    "Total_ms2_site":ms2_site,
                    "percent_ms2_site":percent_ms2_site,
                    "total_mapa":total_mapa,
                    }
    context={"data":data}
    return render(request,"trend/circle_wise_dashboard.html",context)


@login_required(login_url="/accounts/login/")  
def circle_wise_dpr_upload(request):
    DPR_update_status.objects.all().delete()
    if request.method=="POST":
            DPR_file.objects.all().delete()
            file=request.FILES["myfile"]
            soft_at=request.FILES["soft_at"]
            # performance_at=request.FILES["performance_at"]
            
            G1800=request.FILES.get("G1800",None)
            L900=request.FILES.get("L900",None)
            L1800=request.FILES.get("L1800",None)
            L2300=request.FILES.get("L2300",None)
            L2100=request.FILES.get("L2100",None)
            print("G1800:",G1800)
            
            
            physical_at=request.FILES["physical_at"]
            
            obj=DPR_file.objects.create(dpr_file=file)
            path=str(obj.dpr_file)
            print(path)
            df=pd.read_excel("media/"+path)
            print(df)
            del_obj=[]
            if not(df.empty):
                
                for i,d in df.iterrows():
                   
                            pk=str(d["CIRCLE"])+str(d["Unique_SITE_ID"])+str(d["BAND"])+str(d["TOCO_NAME"])+str(d["Project"])+str(d["Activity"])
                            try:
                                obj=DPR_table1.objects.get(id=pk)
                                kpi_objs=performance_at_table.objects.filter(key=obj) 
                            except:
                                    status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="site not found in database" )
                                    # message=str(d["Unique_SITE_ID"]) + " not found in database"
                                    # print(message)
                                    # messages.error(request,message)
                                    continue
                           
    ############################################ Soft at ##################################################################           
                           
                            if d["Soft_AT_Status"] == "ACCEPTED" or d["Soft_AT_Status"] == "REJECTED" or d["Soft_AT_Status"] == "OFFERED" or d["Soft_AT_Status"] == "PENDING":
                               
                                if d["Soft_AT_Status"] == "ACCEPTED":
                                        if not obj.Soft_AT_Status == "ACCEPTED":
                                            print("inside ACCEPTED update")
                                            print("DATE:",d["SOFT_AT_ACCEPTANCE_DATE"])

                                            obj.Soft_AT_Status=d["Soft_AT_Status"]
                                            if not pd.isnull(d["SOFT_AT_ACCEPTANCE_DATE"]) and  isinstance(d["SOFT_AT_ACCEPTANCE_DATE"], datetime):
                                                obj.SOFT_AT_ACCEPTANCE_DATE = d["SOFT_AT_ACCEPTANCE_DATE"]
                                            else:
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at acceptance date is missing or date formate is not correct" )
                                                # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                                # messages.error(request,message)
                                                continue
                                            obj.SOFT_AT_ACCEPTANCE_MAIL=soft_at
                                        
                                            obj.SOFT_AT_REJECTION_DATE = None
                                            obj.SOFT_AT_REJECTION_REASON= ""
                                            # obj.SOFT_AT_REJECTED_TAT_DATE= None
                                            obj.SOFT_AT_OFFERED_DATE= None
                                            obj.SOFT_AT_OFFERED_REMARKS= ""
                                            obj.SOFT_AT_PENDING_REASON= ""
                                            obj.SOFT_AT_PENDING_REMARK= ""
                                            obj.SOFT_AT_PENDING_TAT_DATE= None
                                        else:
                                            status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Status Already accepted in the database" )
                                            # message=str(d["Unique_SITE_ID"]) + ": Already accepted"
                                            # messages.error(request,message)
                                            continue
                                
                                
                                
                                
                                
                                
                                if d["Soft_AT_Status"] == "REJECTED":
                                        print("inside REJECTED update")
                                        obj.Soft_AT_Status=d["Soft_AT_Status"]
                                        if not pd.isnull(d["SOFT_AT_REJECTION_DATE"]) and  isinstance(d["SOFT_AT_REJECTION_DATE"], datetime):
                                            obj.SOFT_AT_REJECTION_DATE = d["SOFT_AT_REJECTION_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_REJECTION_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    
                                        if pd.isnull(d["SOFT_AT_REJECTION_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection Reason is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_REJECTION_REASON=d["SOFT_AT_REJECTION_REASON"]
                                                
                                        

                                        if not pd.isnull(d["SOFT_AT_REJECTED_TAT_DATE"]) and  isinstance(d["SOFT_AT_REJECTED_TAT_DATE"], datetime):
                                            obj.SOFT_AT_REJECTED_TAT_DATE=d["SOFT_AT_REJECTED_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_REJECTED_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Rejection TAT  date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    
                                        obj.SOFT_AT_ACCEPTANCE_DATE=None
                                        obj.SOFT_AT_ACCEPTANCE_MAIL=""
                                        
                                        obj.SOFT_AT_OFFERED_DATE= None
                                        obj.SOFT_AT_OFFERED_REMARKS= ""
                                        obj.SOFT_AT_PENDING_REASON= ""
                                        obj.SOFT_AT_PENDING_REMARK= ""
                                        obj.SOFT_AT_PENDING_TAT_DATE= None   
                                                    

                                if d["Soft_AT_Status"] == "OFFERED":
                                        print("inside OFFERED update")
                                        
                                        obj.Soft_AT_Status=d["Soft_AT_Status"]
                                        
                                        if not pd.isnull(d["SOFT_AT_OFFERED_DATE"]) and  isinstance(d["SOFT_AT_OFFERED_DATE"], datetime):
                                            obj.SOFT_AT_OFFERED_DATE=d["SOFT_AT_OFFERED_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_OFFERED_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    

                                        if pd.isnull(d["SOFT_AT_OFFERED_REMARKS"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Offered remark is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_OFFERED_REMARKS=d["SOFT_AT_OFFERED_REMARKS"]  

                                        obj.SOFT_AT_ACCEPTANCE_DATE=None
                                        obj.SOFT_AT_ACCEPTANCE_MAIL=""
                                        obj.SOFT_AT_REJECTION_DATE = None
                                        obj.SOFT_AT_REJECTION_REASON=""
                                        # obj.SOFT_AT_REJECTED_TAT_DATE= None
                                        
                                        obj.SOFT_AT_PENDING_REASON= ""
                                        obj.SOFT_AT_PENDING_REMARK= ""
                                        obj.SOFT_AT_PENDING_TAT_DATE= None
                                        
                                        
                                if d["Soft_AT_Status"] == "PENDING":
                                        print("inside PENDING update")
                                        obj.Soft_AT_Status=d["Soft_AT_Status"]
                                        if pd.isnull(d["SOFT_AT_PENDING_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending Reason is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_PENDING_REASON=d["SOFT_AT_PENDING_REASON"] 

                                        if pd.isnull(d["SOFT_AT_PENDING_REMARK"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending Remark is missing" )
                                                continue
                                        else:
                                              obj.SOFT_AT_PENDING_REMARK=d["SOFT_AT_PENDING_REMARK"]
                                        
                                        
                                        if not pd.isnull(d["SOFT_AT_PENDING_TAT_DATE"]) and  isinstance(d["SOFT_AT_PENDING_TAT_DATE"], datetime):
                                            obj.SOFT_AT_PENDING_TAT_DATE=d["SOFT_AT_PENDING_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["SOFT_AT_PENDING_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Soft at Pending TAT formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue   
                                        obj.SOFT_AT_ACCEPTANCE_DATE=None
                                        obj.SOFT_AT_ACCEPTANCE_MAIL=""
                                        obj.SOFT_AT_REJECTION_DATE = None
                                        obj.SOFT_AT_REJECTION_REASON=""
                                        # obj.SOFT_AT_REJECTED_TAT_DATE= None
                                        obj.SOFT_AT_OFFERED_DATE= None
                                        obj.SOFT_AT_OFFERED_REMARKS= ""
                            
                            else:
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Soft At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )
                                # message=str(d["Unique_SITE_ID"]) + ": Getting Soft At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED "
                                # messages.error(request,message)
                                continue
                            
    ########################################## PHYSICAL AT ############################################################################
                            
                            if d["PHYSICAL_AT_Status"] == "ACCEPTED" or d["PHYSICAL_AT_Status"] == "REJECTED" or d["PHYSICAL_AT_Status"] == "OFFERED" or d["PHYSICAL_AT_Status"] == "PENDING":
                               
                                if d["PHYSICAL_AT_Status"] == "ACCEPTED":
                                        if not obj.PHYSICAL_AT_Status == "ACCEPTED":
                                            print("inside ACCEPTED update")
                                            print("DATE:",d["PHYSICAL_AT_ACCEPTANCE_DATE"])

                                            obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                            if not pd.isnull(d["PHYSICAL_AT_ACCEPTANCE_DATE"]) and  isinstance(d["PHYSICAL_AT_ACCEPTANCE_DATE"], datetime):
                                                obj.PHYSICAL_AT_ACCEPTANCE_DATE = d["PHYSICAL_AT_ACCEPTANCE_DATE"]
                                            else:
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at acceptance date is missing or date formate is not correct" )
                                                # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                                # messages.error(request,message)
                                                continue
                                            obj.PHYSICAL_AT_ACCEPTANCE_MAIL=soft_at
                                        
                                            obj.PHYSICAL_AT_REJECTION_DATE = None
                                            obj.PHYSICAL_AT_REJECTION_REASON= ""
                                            # obj.PHYSICAL_AT_REJECTED_TAT_DATE= None
                                            obj.PHYSICAL_AT_OFFERED_DATE= None
                                            obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                                            obj.PHYSICAL_AT_PENDING_REASON= ""
                                            obj.PHYSICAL_AT_PENDING_REMARK= ""
                                            obj.PHYSICAL_AT_PENDING_TAT_DATE= None
                                        else:
                                            status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Status Already accepted in the database" )
                                            # message=str(d["Unique_SITE_ID"]) + ": Already accepted"
                                            # messages.error(request,message)
                                            continue
                                


                                if d["PHYSICAL_AT_Status"] == "REJECTED":
                                        print("inside REJECTED update")
                                        obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                        if not pd.isnull(d["PHYSICAL_AT_REJECTION_DATE"]) and  isinstance(d["PHYSICAL_AT_REJECTION_DATE"], datetime):
                                            obj.PHYSICAL_AT_REJECTION_DATE = d["PHYSICAL_AT_REJECTION_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_REJECTION_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    
                                        if pd.isnull(d["PHYSICAL_AT_REJECTION_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection Reason is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_REJECTION_REASON=d["PHYSICAL_AT_REJECTION_REASON"]
                                                
                                        

                                        if not pd.isnull(d["PHYSICAL_AT_REJECTED_TAT_DATE"]) and  isinstance(d["PHYSICAL_AT_REJECTED_TAT_DATE"], datetime):
                                            obj.PHYSICAL_AT_REJECTED_TAT_DATE=d["PHYSICAL_AT_REJECTED_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_REJECTED_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Rejection TAT  date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    
                                        obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
                                        obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                                        
                                        obj.PHYSICAL_AT_OFFERED_DATE= None
                                        obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                                        obj.PHYSICAL_AT_PENDING_REASON= ""
                                        obj.PHYSICAL_AT_PENDING_REMARK= ""
                                        obj.PHYSICAL_AT_PENDING_TAT_DATE= None   
                            
                            
                                if d["PHYSICAL_AT_Status"] == "OFFERED":
                                        print("inside OFFERED update")
                                        
                                        obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                        
                                        if not pd.isnull(d["PHYSICAL_AT_OFFERED_DATE"]) and  isinstance(d["PHYSICAL_AT_OFFERED_DATE"], datetime):
                                            obj.PHYSICAL_AT_OFFERED_DATE=d["PHYSICAL_AT_OFFERED_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_OFFERED_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    

                                        if pd.isnull(d["PHYSICAL_AT_OFFERED_REMARKS"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Offered remark is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_OFFERED_REMARKS=d["PHYSICAL_AT_OFFERED_REMARKS"]  

                                        obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
                                        obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                                        obj.PHYSICAL_AT_REJECTION_DATE = None
                                        obj.PHYSICAL_AT_REJECTION_REASON=""
                                        # obj.PHYSICAL_AT_REJECTED_TAT_DATE= None
                                        
                                        obj.PHYSICAL_AT_PENDING_REASON= ""
                                        obj.PHYSICAL_AT_PENDING_REMARK= ""
                                        obj.PHYSICAL_AT_PENDING_TAT_DATE= None
                            
                                         
                                if d["PHYSICAL_AT_Status"] == "PENDING":
                                        print("inside PENDING update")
                                        obj.PHYSICAL_AT_Status=d["PHYSICAL_AT_Status"]
                                        if pd.isnull(d["PHYSICAL_AT_PENDING_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending Reason is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_PENDING_REASON=d["PHYSICAL_AT_PENDING_REASON"] 

                                        if pd.isnull(d["PHYSICAL_AT_PENDING_REMARK"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending Remark is missing" )
                                                continue
                                        else:
                                              obj.PHYSICAL_AT_PENDING_REMARK=d["PHYSICAL_AT_PENDING_REMARK"]
                                        
                                        
                                        if not pd.isnull(d["PHYSICAL_AT_PENDING_TAT_DATE"]) and  isinstance(d["PHYSICAL_AT_PENDING_TAT_DATE"], datetime):
                                            obj.SOFT_AT_PENDING_TAT_DATE=d["PHYSICAL_AT_PENDING_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PHYSICAL_AT_PENDING_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Physical at Pending TAT formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue   
                                        obj.PHYSICAL_AT_ACCEPTANCE_DATE=None
                                        obj.PHYSICAL_AT_ACCEPTANCE_MAIL=""
                                        obj.PHYSICAL_AT_REJECTION_DATE = None
                                        obj.PHYSICAL_AT_REJECTION_REASON=""
                                        # obj.PHYSICAL_AT_REJECTED_TAT_DATE= None
                                        obj.PHYSICAL_AT_OFFERED_DATE= None
                                        obj.PHYSICAL_AT_OFFERED_REMARKS= ""
                            
                            else:
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Physical At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )
                                # message=str(d["Unique_SITE_ID"]) + ": Getting Soft At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED "
                                # messages.error(request,message)
                                continue
                            
                            
    ############################################### PERFORMANCE AT ####################################################           
                           
                            bands=str(d["BAND"]).split("_")
                            print(bands)
                            if d["Performance_AT_Status"] == "ACCEPTED" or d["Performance_AT_Status"] == "REJECTED" or d["Performance_AT_Status"] == "OFFERED" or d["Performance_AT_Status"] == "PENDING":
                               
                                if d["Performance_AT_Status"] == "ACCEPTED":
                                        if not obj.Performance_AT_Status == "ACCEPTED":
                                            print("inside ACCEPTED update")
                                            print("DATE:",d["PERFORMANCE_AT_ACCEPTANCE_DATE"])

                                            obj.Performance_AT_Status=d["Performance_AT_Status"]
                                            if not pd.isnull(d["PERFORMANCE_AT_ACCEPTANCE_DATE"]) and  isinstance(d["PERFORMANCE_AT_ACCEPTANCE_DATE"], datetime):
                                                obj.PERFORMANCE_AT_ACCEPTANCE_DATE = d["PERFORMANCE_AT_ACCEPTANCE_DATE"]
                                            else:
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at acceptance date is missing or date formate is not correct")
                                                # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                                # messages.error(request,message)
                                                continue
                                            # obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=soft_at
                                           
                                           
                                           
                                            for kpi_obj in kpi_objs:
                                                if kpi_obj.band=="G1800":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=G1800
                                                
                                                if kpi_obj.band=="L1800":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L1800
                                                
                                                if kpi_obj.band=="L900":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L900
                                                
                                                if kpi_obj.band=="L2300":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L2300
                                                
                                                if kpi_obj.band=="L2100":
                                                  kpi_obj.Performance_AT_Status="ACCEPTED"
                                                  kpi_obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=L2100
                                                kpi_obj.save()
                                               

                                            
                                            obj.PERFORMANCE_AT_REJECTION_DATE = None
                                            obj.PERFORMANCE_AT_REJECTION_REASON= ""
                                            # obj.PERFORMANCE_AT_REJECTED_TAT_DATE= None
                                            obj.PERFORMANCE_AT_OFFERED_DATE= None
                                            obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
                                            obj.PERFORMANCE_AT_PENDING_REASON= ""
                                            obj.PERFORMANCE_AT_PENDING_REMARK= ""
                                            obj.PERFORMANCE_AT_PENDING_TAT_DATE= None
                                        else:
                                            status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark=" Performance at Status Already accepted in the database" )
                                            # message=str(d["Unique_SITE_ID"]) + ": Already accepted"
                                            # messages.error(request,message)
                                            continue
                                        
                                if d["Performance_AT_Status"] == "REJECTED":
                                        print("inside REJECTED update")
                                        obj.Performance_AT_Status=d["Performance_AT_Status"]
                                        if not pd.isnull(d["PERFORMANCE_AT_REJECTION_DATE"])  and  isinstance(d["PERFORMANCE_AT_REJECTION_DATE"], datetime):
                                            obj.PERFORMANCE_AT_REJECTION_DATE = d["PERFORMANCE_AT_REJECTION_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_REJECTION_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    
                                        if pd.isnull(d["PERFORMANCE_AT_REJECTION_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection Reason is missing" )
                                                continue
                                        else:
                                              print("reason################")
                                              obj.PERFORMANCE_AT_REJECTION_REASON=d["PERFORMANCE_AT_REJECTION_REASON"]
                                                
                                              lis_kpi_status_bandwise=d["PERFORMANCE_AT_REJECTION_REASON"].split(",")
                                              di={}
                                            #   print(lis_kpi_status_bandwise)
                                              for band_status in lis_kpi_status_bandwise:
                                                    lis=band_status.split("_")
                                                    di[lis[0]] = lis[1]
                                                    
                                              for  kpi_obj in kpi_objs:
                                                    if kpi_obj.band in di.keys():
                                                        kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
                                                        print(di[str(kpi_obj.band)], kpi_obj.band)
                                                        kpi_obj.save()
                                              print(di)

                                        if not pd.isnull(d["PERFORMANCE_AT_REJECTED_TAT_DATE"]) and  isinstance(d["PERFORMANCE_AT_REJECTED_TAT_DATE"], datetime):
                                            obj.PERFORMANCE_AT_REJECTED_TAT_DATE=d["PERFORMANCE_AT_REJECTED_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_REJECTED_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Rejection TAT  date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    
                                        obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                        # obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=""
                                        
                                        obj.PERFORMANCE_AT_OFFERED_DATE= None
                                        obj.PERFORMANCE_AT_OFFERED_REMARKS= ""
                                        obj.PERFORMANCE_AT_PENDING_REASON= ""
                                        obj.PERFORMANCE_AT_PENDING_REMARK= ""
                                        obj.PERFORMANCE_AT_PENDING_TAT_DATE= None
                                
                                if d["Performance_AT_Status"] == "OFFERED":
                                        print("inside OFFERED update")
                                        
                                        obj.Performance_AT_Status=d["Performance_AT_Status"]
                                        
                                        if not pd.isnull(d["PERFORMANCE_AT_OFFERED_DATE"]) and isinstance(d["PERFORMANCE_AT_OFFERED_DATE"], datetime):
                                            obj.PERFORMANCE_AT_OFFERED_DATE=d["PERFORMANCE_AT_OFFERED_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_OFFERED_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered date formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue    

                                        if pd.isnull(d["PERFORMANCE_AT_OFFERED_REMARKS"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Offered remark is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_OFFERED_REMARKS=d["PERFORMANCE_AT_OFFERED_REMARKS"]  
                                              lis_kpi_status_bandwise=d["PERFORMANCE_AT_OFFERED_REMARKS"].split(",")
                                              di={}
                                            #   print(lis_kpi_status_bandwise)
                                              for band_status in lis_kpi_status_bandwise:
                                                    lis=band_status.split("_")
                                                    di[lis[0]] = lis[1]
                                                    
                                              for  kpi_obj in kpi_objs:
                                                    if kpi_obj.band in di.keys():
                                                        kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
                                                        print(di[str(kpi_obj.band)], kpi_obj.band)
                                                        kpi_obj.save()
                                              print(di)
                                        obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                        # obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=""
                                        obj.PERFORMANCE_AT_REJECTION_DATE = None
                                        obj.PERFORMANCE_AT_REJECTION_REASON=""
                                        # obj.PERFORMANCE_AT_REJECTED_TAT_DATE= None
                                        
                                        obj.PERFORMANCE_AT_PENDING_REASON= ""
                                        obj.PERFORMANCE_AT_PENDING_REMARK= ""
                                        obj.PERFORMANCE_AT_PENDING_TAT_DATE= None

                                if d["Performance_AT_Status"] == "PENDING":
                                        print("inside PENDING update")
                                        obj.Performance_AT_Status=d["Performance_AT_Status"]
                                        if pd.isnull(d["PERFORMANCE_AT_PENDING_REASON"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending Reason is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_PENDING_REASON=d["PERFORMANCE_AT_PENDING_REASON"] 

                                        if pd.isnull(d["PERFORMANCE_AT_PENDING_REMARK"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending Remark is missing" )
                                                continue
                                        else:
                                              obj.PERFORMANCE_AT_PENDING_REMARK=d["PERFORMANCE_AT_PENDING_REMARK"]
                                              lis_kpi_status_bandwise=d["PERFORMANCE_AT_PENDING_REMARK"].split(",")
                                              di={}
                                            #   print(lis_kpi_status_bandwise)
                                              for band_status in lis_kpi_status_bandwise:
                                                    lis=band_status.split("_")
                                                    di[lis[0]] = lis[1]
                                                    
                                              for  kpi_obj in kpi_objs:
                                                    if kpi_obj.band in di.keys():
                                                        kpi_obj.Performance_AT_Status=di[str(kpi_obj.band)] 
                                                        print(di[str(kpi_obj.band)], kpi_obj.band)
                                                        kpi_obj.save()
                                              print(di)
                                        
                                        
                                        if not pd.isnull(d["PERFORMANCE_AT_PENDING_TAT_DATE"]) and  isinstance(d["PERFORMANCE_AT_PENDING_TAT_DATE"], datetime):
                                            obj.PERFORMANCE_AT_PENDING_TAT_DATE=d["PERFORMANCE_AT_PENDING_TAT_DATE"]
                                            print("updated")
                                        else:
                                            if pd.isnull(d["PERFORMANCE_AT_PENDING_TAT_DATE"]):
                                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending TAT date is missing" )
                                            else:
                                                 status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Performance at Pending TAT formate is not correct" )
                                            # message= str(obj.SITE_ID) + ": Soft at acceptance date is missing or formate is not correct"
                                            # messages.error(request,message)
                                            continue   
                                        obj.PERFORMANCE_AT_ACCEPTANCE_DATE=None
                                        # obj.PERFORMANCE_AT_ACCEPTANCE_MAIL=""
                                        obj.PERFORMANCE_AT_REJECTION_DATE = None
                                        obj.PERFORMANCE_AT_REJECTION_REASON=""
                                        # obj.PERFORMANCE_AT_REJECTED_TAT_DATE= None
                                        obj.PERFORMANCE_AT_OFFERED_DATE= None
                                        obj.PERFORMANCE_AT_OFFERED_REMARKS= ""

                            else:
                                status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="Getting Performance At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED" )
                                # message=str(d["Unique_SITE_ID"]) + ": Getting Soft At Status Other than ACCEPTED/REJECTED/PENDING/OFFERED "
                                # messages.error(request,message)
                                continue
                           
                           

                            
                            obj.save()
                            print(d["Unique_SITE_ID"], " updated")
                            status_obj=DPR_update_status.objects.create(id=pk, update_status="UPDATED",SITE_ID=d["Unique_SITE_ID"])
                            # message=str(d["Unique_SITE_ID"]) + ": Update Successfully"
                            # messages.success(request,message)
                else:
                    status_objs=DPR_update_status.objects.all()
                    context={"status_obj":status_objs}
                    return render(request,"trend/DPR_upload_status_tbl.html",context)          
   
    path="media/dpr/dpr_templates/DPR_TEMP.xlsx"
    context={"path":path }              
    return render(request,"trend/DPR_upload_form.html",context)    
    

                
                                    # else:
                                    #     messages.error(request,"Soft at Status Should be 'ACCEPTED,RECECTED,PENDING,OFFERED,' but getting something else")
                                        # if pd.isnull(d["SOFT_AT_ACCEPTANCE_DATE"]):
                                        #     obj.SOFT_AT_ACCEPTANCE_DATE = None
                                        # else:
                                        #    obj.SOFT_AT_ACCEPTANCE_DATE = d["SOFT_AT_ACCEPTANCE_DATE"]



def mapa_status_upld(request):
    DPR_update_status.objects.all().delete()
    if request.method=="POST":
            DPR_file.objects.all().delete()
            file=request.FILES["MAPA_file"]
            obj=DPR_file.objects.create(dpr_file=file)
            path=str(obj.dpr_file)
            print(path)
            df=pd.read_excel("media/"+path)
            print(df)
            # del_obj=[]
            if not(df.empty):
                
                for i,d in df.iterrows():
                   
                            pk=str(d["CIRCLE"])+str(d["Unique_SITE_ID"])+str(d["BAND"])+str(d["TOCO_NAME"])+str(d["Project"])+str(d["Activity"])
                            try:
                                objs=DPR_table1.objects.get(id=pk)
                                
                            except:
                                    status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="site not found in database" )
                                    
                                    continue
                            if d["Soft_AT_Status"]=="ACCEPTED" and d["Performance_AT_Status"]== "ACCEPTED" and d["PHYSICAL_AT_Status"]=="ACCEPTED" :
                                    objs.MAPA_STATUS=d["MAPA_STATUS"]
                                    print("updating #######################################")
                                    objs.save()
                                    status_obj=DPR_update_status.objects.create(id=pk, update_status="UPDATED",SITE_ID=d["Unique_SITE_ID"] )
                                    messages.success(request,"MAPA_uploaded Succefully")
                            else:
                                  status_obj=DPR_update_status.objects.create(id=pk, update_status="NOT UPDATED",SITE_ID=d["Unique_SITE_ID"], Remark="All status are not accepted" )
                                  continue

                else:
                    status_objs=DPR_update_status.objects.all()
                    context={"status_obj":status_objs}
                    return render(request,"trend/DPR_upload_status_tbl.html",context) 
    
    return render(request,"trend/MAPA_upload.html")




def mapa_single_site_update(request,pk):
        obj=DPR_table1.objects.get(pk=pk)
        if request.method == 'POST':
            if request.POST.get("MAPA")=="OK":
                if obj.Performance_AT_Status=="ACCEPTED" and obj.Soft_AT_Status=="ACCEPTED" and obj.PHYSICAL_AT_Status=="ACCEPTED":
                    obj.MAPA_STATUS=request.POST.get("MAPA")
                    obj.save()
                    messages.success(request,"MAPA updated Succesfully")
                else:
                    messages.error(request,"ALL STATUS are not ACCEPTED")
            if request.POST.get("MAPA")=="NOT OK":  
                    obj.MAPA_STATUS=request.POST.get("MAPA")
                    obj.save()
        return redirect("single_site_view",pk=pk)

