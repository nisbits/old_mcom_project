from django.contrib import admin
from django.urls import path,include
from trend import views
urlpatterns = [
   
    path("upload_dpr/",views.dpr_key_upload, name="dpr_upload"),
    path("dpr_site_list/",views.dpr_site_list, name="dpr_update"),
    path("single_site_view/<str:pk>/",views.single_site_view, name="single_site_view"),
    path("soft_at_update/<str:pk>/<str:at_status>",views.soft_at_update, name="soft_at_update"),
    path("physical_at_update/<str:pk>/<str:at_status>",views.physical_at_update, name="physical_at_update"),
    path("performance_at_update/<str:pk>/<str:at_status>/<str:band>",views.performance_at_update, name="performance_at_update"),
    path("dashboard/",views.all_dashboard, name="dashboard"),
    path("dpr_view/<str:circle>",views.dpr_view, name="dpr_view"),
    path("circle_wise_dashboard/",views.circle_wise_dashboard, name="circle_wise_dashboard"),
    path("circle_wise_dpr_upload/",views.circle_wise_dpr_upload, name="circle_wise_dpr_upload"),
    path("mapa_status_upld/",views.mapa_status_upld, name="mapa_status_upld"),
    path("performance_at_tat_date/<str:pk>",views.performance_at_tat_date, name="performance_at_tat_date"),
    path("mapa_single_site_update/<str:pk>",views.mapa_single_site_update, name="mapa_single_site_update"),
    


]


