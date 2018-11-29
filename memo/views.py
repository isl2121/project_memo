from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Memo

# Create your views here.

class MemoLV(ListView):
    model = Memo
