from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Memo
from django.http import HttpResponseRedirect
from .foms import UserForm, LoginForm, MemoForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# Create your views here.

class MemoLV(ListView):
    model = Memo
    queryset = Memo.objects.all()

    def get(self, request, *args, **kwargs):
        orderby = request.GET.get('orderby')

        if orderby == 'like':
            self.queryset = Memo.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-update_time')
        elif orderby == 'mypost':
            if User.is_authenticated:
                user = User.objects.get(username=request.user.get_username())
                self.queryset = Memo.objects.filter(user_name=user)
            else:
                self.queryset = Memo.objects.all().order_by('-update_time')
        else:
            self.queryset = Memo.objects.all().order_by('-update_time')
        return super(MemoLV, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemoLV, self).get_context_data(**kwargs)
        context['login_user_name'] = self.request.user
        return context


def signup(requset):
    if requset.method == 'POST':
        form = UserForm(requset.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            auth_login(requset, new_user)
            return redirect('memo:index')
    else:
        form = UserForm

    return render(requset, 'user/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(request.POST['username'])
        print(request.POST['password'])
        print(request.POST)
        print(form.errors)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('memo:index')

        messages.warning(request, '로그인 실패. 다시 시도 해보세요.')
        return HttpResponseRedirect('/')

    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form':form})

@login_required
def logout(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.get_username())
        auth_logout(request)

        messages.info(request, '로그아웃 되셨습니다.')
        return HttpResponseRedirect('/')

    else:
        messages.warning(request, '로그인한 유저만 가능합니다.')
        return HttpResponseRedirect('/')


def make(request):
    if request.user.is_authenticated:
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
    else:

        messages.warning(request, '로그인한 유저만 메시지를 남길수 있습니다.')
        return HttpResponseRedirect('/')

def delete(request, pk):
    memo = Memo.objects.get(pk=pk)
    user = User.objects.get(username=request.user.get_username())

    if memo.user_name == user:
        memo.delete()
        messages.info(request, '성공적으로 삭제되었습니다.')
        return HttpResponseRedirect('/')
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


def like(request, pk):
    if request.user.is_authenticated:
        memo = Memo.objects.get(pk=pk)
        user = User.objects.get(username=request.user.get_username())

        if memo.likes.filter(id=user.id).exists():
            memo.likes.remove(user)
        else:
            memo.likes.add(user)
        return redirect('memo:index')

    else:
        messages.warning(request, '로그인한 유저만 좋아요할수 있습니다.')
        return HttpResponseRedirect('/')
