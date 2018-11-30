from django.shortcuts import render, redirect
from django.views.generic import ListView
import json
from .models import Memo
from django.http import HttpResponse
from .foms import UserForm, LoginForm, MemoForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# Create your views here.

class MemoLV(ListView):
    model = Memo

    def get_context_data(self, **kwargs):
        context = super(MemoLV, self).get_context_data(**kwargs)
        context['login_user_name'] = self.request.user
        return context


def signup(requset):
    if requset.method == 'POST':
        form = UserForm(requset.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(requset, new_user)
            return redirect('memo:index')
    else:
        form = UserForm

    return render(requset, 'user/signup.html', {'form': form})

def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST('username')
            password = request.POST('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('memo:index')

        return HttpResponse('로그인 실패. 다시 시도 해보세요.')

    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form':form})


def make(request):
    if request.method == 'POST':
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user_name = User.objects.get(username = request.user.get_username())
            memo.save_memo()
            return redirect('memo:index')
    else:
        form = MemoForm()

    return render(request, 'memo/make_memo.html' , {'form':form})

def delete(request, pk):
    memo = Memo.objects.get(pk=pk)
    user = User.objects.get(username=request.user.get_username())

    if memo.user_name == user:
        memo.delete()
        return redirect('memo:index')
    else:
        return render(request, 'memo/warning.html')

def modify(request, pk):
    memo = Memo.objects.get(pk=pk)

    if request.method == 'POST':
        user = User.objects.get(username=request.user.get_username())
        form = MemoForm(request.POST, instance=memo)
        if user == memo.user_name:
            if form.is_valid():
                form.save()
                return redirect('memo:index')
        else:
            return redirect(request,'/memo/warning.html')
    else:
        form = MemoForm(instance=memo)

    return render(request, 'memo/modify_memo.html', {'memo':memo, 'form':form})

@login_required
def like(request, pk):
    memo = Memo.objects.get(pk=pk)
    user = User.objects.get(username=request.user.get_username())

    if memo.likes.filter(id=user.id).exists():
        memo.likes.remove(user)
    else:
        memo.likes.add(user)

    return redirect('memo:index')
