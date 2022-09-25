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



class DatetimeUtils():

    @classmethod
    def get_current_time(cls, month=1, year=2020):
        return datetime.now()


class GeneratorUtils():

    @classmethod
    def get_booking_id(cls, month=1, year=2020):
        
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        nums = '0123456789'
        return "TW-"+ ''.join([random.choice(chars) for i in range(6)]+[random.choice(nums) for i in range(4)])
        

