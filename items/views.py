from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from categories.models import Category
from django.utils import timezone
import random
from django.db.models import ProtectedError

def storage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    
    category_id = request.GET.get('category')
    if category_id:
        items = Item.objects.filter(owner_user=request.user, category_id=category_id, is_deleted=False)
    else:
        items = Item.objects.filter(owner_user=request.user, is_deleted=False)
    
    return render(request, 'items/storage.html', {'items': items, 'categories': categories})

def search(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)

    keyword = request.GET.get('q', '')
    items = Item.objects.filter(owner_user=request.user, product_name__icontains=keyword, is_deleted=False)
                                                        # 장고 ORM icontains 사용
    return render(request, 'items/storage.html', {'items': items, 'categories': categories })

def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    #수아-수정본
    if request.method == 'POST':
        category_id = request.POST.get('category')
        
        if not category_id:
            return redirect('items:plus')
    
        new_item = Item()
        new_item.owner_user = request.user
        new_item.category = get_object_or_404(Category, pk=category_id) 
        new_item.product_name = request.POST['product_name']
        new_item.image = request.FILES.get('image')
        new_item.product_url = request.POST.get('product_url')
        price = request.POST.get('price')
        if price == '':
            price = None
        new_item.price = price
        new_item.save()
        
        return redirect('items:main')
    
    return redirect('items:plus')

def detail(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    item = get_object_or_404(Item, pk=item_id)
    
    if item.owner_user != request.user:
        return redirect('items:storage')
    
    return render(request, 'items/detail.html', {'item': item})

def edit(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    edit_item = get_object_or_404(Item, pk=item_id)
    
    if edit_item.owner_user != request.user:
        return redirect('items:detail', edit_item.id)
    
    if request.method == 'POST':
        edit_item.category = get_object_or_404(Category, pk=request.POST['category'])
        edit_item.product_name = request.POST['product_name']
        edit_item.save()
        return redirect('items:detail', edit_item.id)
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)

    return render(request, 'items/edit.html', {'item': edit_item, 'categories': categories})

def scrap(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    item = get_object_or_404(Item, pk=item_id)
    
    if item.owner_user != request.user:
        return redirect('items:storage')
    
    item.is_scrapped = not item.is_scrapped
    item.save()
    
    return redirect('items:detail', item.id)

def scrapped_list(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    items = Item.objects.filter(owner_user=request.user, is_scrapped=True, is_deleted=False)
    return render(request, 'items/scrapped_list.html', {'items': items})

def delete(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    delete_item = get_object_or_404(Item, pk=item_id)
    
    if delete_item.owner_user != request.user:
        return redirect('items:detail', delete_item.id)
    
    try:
        delete_item.delete() 
    except ProtectedError:
        delete_item.is_deleted = True
        delete_item.save()
    
    return redirect('items:storage')

def plus_info(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    category_id = request.GET.get('category')   
    selected_category = get_object_or_404(Category, pk=category_id) if category_id else None
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    
    return render(request, 'items/plus_info.html', {
        'categories': categories,
        'selected_category': selected_category 
    })


def main(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = (
        Category.objects.filter(is_default=True) |
        Category.objects.filter(creator=request.user)
    ).distinct()
    
    items = Item.objects.filter(
        owner_user=request.user,
        is_deleted=False
    ).order_by('-created_at')
    
    category_id = request.GET.get('category')
    selected_category = None
    
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)

        if not selected_category.is_default and selected_category.creator != request.user:
            return redirect('items:main')

        items = items.filter(category=selected_category)
    else:
        items = items
        
    recent_items = items[:3]

    today_count = Item.objects.filter(
        owner_user=request.user,
        is_deleted=False,
        created_at__date=timezone.localdate()
    ).count()
    
    total_count = items.count() 
    
    for category in categories:
        category.item_count = Item.objects.filter(
            owner_user=request.user,
            category=category,
            is_deleted=False
        ).count()

    return render(request, 'items/main.html', {
        'items': items,
        'recent_items': recent_items,
        'today_count': today_count,
        'total_count': total_count,
        'categories': categories,
        'selected_category': selected_category,
        'nickname': request.user.profile.nickname,
    })

def plus(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    categories = Category.objects.filter(creator=request.user) | Category.objects.filter(is_default=True)
    return render(request, 'items/plus.html', {'categories': categories})

def delete_multiple(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids')
        for item_id in item_ids:
            item = get_object_or_404(Item, pk=item_id, owner_user=request.user)
            try:
                item.delete()  # 실제 삭제 시도
            except ProtectedError:
                item.is_deleted = True  # 토너먼트에 연결되어 있으면 soft delete
                item.save()
    
    return redirect('items:storage')

QUOTES = [
    "마음이 가는 것과 실제로 사고 싶은 것은 다를 수도 있어 ",
    "충동구매보다 더 좋은 건 나에게 정말 필요한 걸 찾는 거야!",
    "무엇을 살지 고민하는 것도 똑똑한 소비의 시작이야 💡",
    "항상 사고 싶은 걸 다 살 수는 없어! 그래서 우리는 선택을 해. 지금 가장 갖고 싶은 단 하나를 찾아보자 ✨",
]

def detail(request, item_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    item = get_object_or_404(Item, pk=item_id)
    quote = random.choice(QUOTES)
    
    if item.owner_user != request.user:
        return redirect('items:storage')
    
    return render(request, 'items/detail.html', {'quote': quote, 'item': item})