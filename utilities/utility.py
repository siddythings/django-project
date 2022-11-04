import base64
import calendar
import csv
import os
import urllib
import logging
import boto3
import uuid
from inspect import getmembers, isfunction, getsourcelines, isclass
import math
import secrets
import requests
import json
import random
from django.core.cache import cache

from django.http import HttpResponse
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pathlib import Path
from datetime import date, datetime, timedelta, time
from application import settings
from application import constants

CACHE_TTL = 60 * 60 *24



def date_string_to_date_time(date, end_time=False):
    try:
        date = datetime.strptime(date, '%d-%m-%Y').date()
    except:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    date = datetime(date.year, date.month, date.day)
    if end_time:
        date = date + timedelta(hours=23, minutes=59, seconds=59)
    return date


def fetch_resources(uri, rel):
        """
        Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
        `uri` is the href attribute from the html link element.
        `rel` gives a relative path, but it's not used here.

        """
        path = ''
        if uri.startswith("http://") or uri.startswith("https://"):
            return uri
        elif uri.startswith("/media/"):
            # path = settings.MEDIA_ROOT + uri.replace('/media/', 'media/')
            path = os.path.join(settings.MEDIA_ROOT,
                                uri.replace("/media/", ""))
        elif uri.startswith("/static/"):
            path = os.path.join(settings.STATIC_ROOT,
                                uri.replace("/static/", ""))
        return path


class DatetimeUtils():

    @classmethod
    def get_current_time(cls, month=1, year=2020):
        return datetime.now()
    
    @classmethod
    def get_today_slot(cls, month=1, year=2020):
        date = datetime.utcnow() + timedelta(hours=7 , minutes=30)
        time_now = date.hour
        slot = []
        for obj in constants.SLOT_HOURS:
            if int(time_now) < obj.get("time"):
                slot.append(obj.get("slot"))
        
        rsp = {
            "date": str(datetime.now().strftime("%d")) + " " + 
            str(datetime.now().strftime("%b")) + " (" 
            +str(datetime.now().strftime("%a")) + ")",
            "slot": slot
        }

        return rsp

    @classmethod
    def get_dated_slot(cls, month=1, year=2020):
        date_slot = []

        for date in range(1,4):
            date_day = datetime.utcnow() + timedelta(date)
            rsp = {
                "date": str(date_day.strftime("%d")) + " " + 
                    str(date_day.strftime("%b")) + " (" 
                    +str(date_day.strftime("%a")) + ")",
                "slot": constants.ALL_SLOTS
            }
            date_slot.append(rsp)

        return date_slot


class GeneratorUtils():

    @classmethod
    def get_booking_id(cls, month=1, year=2020):
        
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        nums = '0123456789'
        return "TW-"+ ''.join([random.choice(chars) for i in range(6)]+[random.choice(nums) for i in range(4)])
        
    @classmethod
    def get_user_id(cls, month=1, year=2020):
        
        return uuid.uuid4().hex
        
    @classmethod
    def get_order_id(cls, month=1, year=2020):
        
        return str(uuid.uuid4().hex).upper()
        
    @classmethod
    def get_application_id(cls, month=1, year=2020):
        
        return str(uuid.uuid4().hex).upper()
        

