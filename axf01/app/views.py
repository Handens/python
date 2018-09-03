from django.shortcuts import render

from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow


def home(request):
    if request.method == 'GET':
        # 获取轮播图信息
        mainwheels = MainWheel.objects.all()
        # 导购
        mainnavs = MainNav.objects.all()
        # 必购
        mainmustbuys = MainMustBuy.objects.all()
        # 商店
        mainshops = MainShop.objects.all()
        # 主要展示的商品
        mainshows = MainShow.objects.all()

        # 轮播图数据
        data = {
            'mainwheels': mainwheels,
            'mainnavs': mainnavs,
            'mainmustbuys': mainmustbuys,
            'mainshops': mainshops,
            'mainshows': mainshows,
        }
        return render(request, 'home/home.html', data)