from django.shortcuts import render
from seller.models import Food
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.
@login_required
def order_detail(request, pk):
    food = Food.objects.get(pk=pk)
    context = {
        'object' : food
    }
    return render(request, 'order/order_detail.html', context)

from django.http import JsonResponse

def modify_cart(request):
    # A 사용자가 카트에 담은 B 음식에 대해서 수량을 조정하는 내용
    # 응답 : 새롭게 변경된 수량, 전체 카트 음식 수량
    # 어떤 사용자?
    user = request.user # 유저 정보는 request의 user에 담겨있으므로
    # 어떤 음식?
    food_id = request.POST['foodId'] # ajax에 담겨있음
    food = Food.objects.get(pk=food_id)
    # 카트 정보
    cart, created = Cart.objects.get_or_create(food=food, user=user)
    # 수량 업데이트
    cart.amount += int(request.POST['amountChange']) # 형 변환 필수
    
    # 수량이 음수인 에러 해결위한 로직
    if cart.amount > 0:
        cart.save()
    
    # "내가" 카트에 담은 전체음식 개수
    # Qustioin - choice 실습에서
    # 특정 문제에 대한 초이스
    # Question.choice_set : 해당 질문을 바라보고 있는 모든 선택지
    totalQuantity = user.cart_set.aggregate(totalcount=Sum('amount'))['totalcount']
    # json
    context = {
        'newQuantity' : cart.amount,
        'totalQuantity' : totalQuantity,
        'message' : '성공',
        'success' : True
    }

    return JsonResponse(context)

def check_cart(request, pk):
    food = Cart.objects.filter(user__id=pk)
    context = {
        'object' : food
    }
    return render(request, 'order/check_cart.html', context)