from django import forms
from customer.models import Customer
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from django.core.exceptions import ValidationError
import pytz
