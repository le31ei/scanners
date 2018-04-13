#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time  : 2018/4/9 17:03
# @Author: lxflxf
# @File  : forms.py
# @Ver   : 0.1
from django import forms


class addItemForm(forms.Form):
    itemname = forms.CharField(max_length=100, required=True)
    ip = forms.CharField(max_length=100, required=True)

