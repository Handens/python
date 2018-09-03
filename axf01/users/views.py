import datetime

from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.models import UserModel, UserTicketModel
from utils.functions import get_ticket


def my(request):
    if request.method == 'GET':
        return render(request, 'mine/mine.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            data = {
                'msg': '请填写完整信息'
            }
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                ticket = get_ticket()

                res = HttpResponseRedirect(reverse('user:my'))
                out_time = datetime.now() + datetime.timedelta(days=1)
                res.set_cookie('ticket', ticket, expires=out_time)

                UserTicketModel.objects.create(user=user,
                                               ticket=ticket,
                                               out_time=out_time)
                return res
            else:
                data['msg'] = '密码错误'
        else:
            data ={
                'msg': '用户名不存在'
            }
        return render(request, 'user/user_login.html', data)


def register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')

        if not all([username, email, password]):
            data = {
                'msg': '请填完全您的资料'
            }
            return render(request, 'user/user_register.html', data)
        UserModel.objects.create(username=username, password=make_password(password), email=email, icon=icon)
        return HttpResponseRedirect(reverse('user:login'))