from django.shortcuts import render, redirect
from .models import Food
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# Create your views here.

# 자신이 판매하는 상품 리스트를 보여주기
# 상품 등록 가능
@login_required # 로그인 안하고 판매자 페이지에 들어가면 에러가 발생한다. 해당 데코레이터를 통해서 로그인이 안되어있다면 로그인하라고 로그인 페이지를 띄어준다.
def seller_index(request):
    foods = Food.objects.all().filter(user__id=request.user.id)
    context = {
        'object_list' : foods
    }
    return render(request, 'seller/seller_index.html', context)

def add_food(request):
    # get
    if request.method == 'GET':
        return render(request, 'seller/seller_add_food.html')
    # post
    elif request.method == 'POST':
        # 폼에서 전달되는 값을 뽑아와서 DB에 저장하는 코드
        # food_name, price, description
        user = request.user
        food_name = request.POST['name']
        food_price = request.POST['price']
        food_description = request.POST['description']

        # 이미지 업로드
        fs = FileSystemStorage()
        uploaded_file = request.FILES['file']
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        Food.objects.create(user=user,
                            name=food_name,
                            price=food_price,
                            description=food_description,
                            image_url=url)
        return redirect('seller:seller_index')
    
def food_detail(request, pk):
    food = Food.objects.get(pk=pk)
    context = {
        'object' : food
    }
    return render(request, 'seller/food_detail.html', context)

def food_delete(request, pk):
    food = Food.objects.get(pk=pk)
    food.delete()
    return redirect('seller:seller_index')