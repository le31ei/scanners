#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2018/4/9 16:01
# @Author: lxflxf
# @File  : urls.py
# @Ver   : 0.1
from django.urls import path
from . import views


app_name = 'portscan'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add_scan/', views.AddScanView.as_view(), name='add_scan'),
    path('list_scan/', views.ScanListView.as_view(), name='list_scan'),
    path('detail_scan/<str:uuid>/', views.DetailListView.as_view(), name='detail_scan'),
    path('export/<str:uuid>/', views.ExportExcelView.as_view(), name='export_excel')
]
