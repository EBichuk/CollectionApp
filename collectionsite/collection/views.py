from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django import forms
from collection.models import Collections, Items, Image, Itemfeaches, Feaches, CollectionProfile, Typecollections, Users, Likes
from collection.forms import AddForm, AddCollection, AddTypeCol
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Мои коллекции
@login_required
def home(request):
    user_id = request.user.id
    col_user = Collections.objects.filter(collection_profile=user_id)
    return render(request, 'home.html', {'col_user': col_user})


# Показ конкретной коллекции
@login_required
def user_collection(request, collection_id):
    item = Items.objects.filter(collection=collection_id) & Items.objects.filter(visibility=1)
    img = []
    for i in item:
        img.append(Image.objects.filter(item=i.pk))
    items = zip(item, img)
    clct = Collections.objects.get(collection_id=collection_id)
    return render(request, 'collection.html', {'items': items, 'clct': clct, 'collection_id': collection_id})


# Элемент
@login_required
def items(request, item_id):
    item = Items.objects.get(item_id=item_id)
    item_feaches = Itemfeaches.objects.filter(item=item_id)
    col_id = Items.objects.get(item_id=item_id).collection.pk
    imgs = Image.objects.filter(item=item_id)
    if request.POST.get('public'):
        Items.objects.filter(item_id=item_id).update(is_public=1)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    if request.POST.get('un_public'):
        Items.objects.filter(item_id=item_id).update(is_public=0)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return render(request, 'item.html',  {'item_feaches': item_feaches, 'imgs': imgs, 'item': item, 'col_id': col_id})


# Скрытие элемента
@login_required
def del_item(request, item_id):
    Items.objects.filter(item_id=item_id).update(visibility=0)
    col_id = Items.objects.get(item_id=item_id).collection.pk
    return user_collection(request, collection_id=col_id)


# добавление изображения
def add_image_item(image, item):
    new_image = Image(image=image, item=item)
    new_image.save()


# добавление описания элемента
def add_item_feaches(data_feaches, item):
    for f in data_feaches.items():
        new_feaches = Itemfeaches(data=str(f[1]),
                                  feaches=Feaches.objects.get(feaches_id=int(f[0])),
                                  item=item)
        new_feaches.save()


@login_required
def add_item_form(request, collection_id):
    type_clct = Collections.objects.get(collection_id=collection_id).type_collection
    feache = Feaches.objects.filter(type_collection=type_clct)

    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES, slugs_cnt=feache)
        if form.is_valid():
            data_item = form.cleaned_data
            name, description = data_item.pop('itemname', 'нет имени'), data_item.pop('description', 'нет описания')
            image = data_item.pop('image', 'нет изображения')
            new_item = Items(itemname=name,
                             description=description,
                             visibility=1,
                             like=0,
                             collection=Collections.objects.get(collection_id=collection_id),
                             is_public=0)
            new_item.save()
            add_image_item(image, new_item)
            add_item_feaches(data_item, new_item)
    else:
        form = AddForm(slugs_cnt=feache)
    return render(request, 'additem.html', {'form': form, 'collection_id': collection_id})


# Редактиование элемента
@login_required
def edit_item(request, item_id):
    collection_id = Items.objects.get(item_id=item_id).collection.pk
    type_clct = Collections.objects.get(collection_id=collection_id).type_collection
    feache = Feaches.objects.filter(type_collection=type_clct)
    item_feaches = Itemfeaches.objects.filter(item=item_id)
    rr = {str(i.feaches.pk): i.data for i in item_feaches}
    if request.method == 'POST':
        form = AddForm(request.POST, request.FILES, slugs_cnt=feache)
        if form.is_valid():
            data_item = form.cleaned_data
            name, description = data_item.pop('itemname', 'нет имени'), data_item.pop('description', 'нет описания')
            image = data_item.pop('image', 'нет изображения')
            new_item = Items(itemname=name,
                             description=description,
                             visibility=1,
                             like=0,
                             collection=Collections.objects.get(collection_id=collection_id),
                             is_public=0)
            new_item.save()
            add_image_item(image, new_item)
            add_item_feaches(data_item, new_item)
    else:
        form = AddForm(slugs_cnt=feache, initial=rr)
    return render(request, 'edititem.html', {'form': form, 'collection_id': collection_id, 'item_id': item_id})


# Добавление коллекции
@login_required
def add_collection(request):
    type_col = Typecollections.objects.filter(visibility=1)
    if request.method == 'POST':
        form = AddCollection(request.POST, request.FILES)
        if form.is_valid():
            new_col = Collections(**form.cleaned_data,
                                  visiblity=1,
                                  like=0,
                                  collection_profile=CollectionProfile.objects.get(pk=request.user.id))
            new_col.save()
    else:
        form = AddCollection()
    return render(request, 'addcollection.html', {'type_col': type_col, 'form': form, 'y': range(1, 10)})


# Создание нового типа коллекции
@login_required
def add_type_collection(request, i):
    if request.method == 'POST':
        form = AddTypeCol(request.POST, slugs_cnt=i)
        if form.is_valid():
            data = form.cleaned_data
            name = data.pop('name', 'нет имени')
            new_type = Typecollections(name=name,
                                       visibility=1,
                                       user=Users.objects.get(pk=request.user.id))
            new_type.save()
            for d in range(i):
                new_feaches = Feaches(feache_name=data[f'{d}_name'],
                                      datatype=data[f'{d}_type'], type_collection=new_type)
                new_feaches.save()
    else:
        form = AddTypeCol(slugs_cnt=i)
    return render(request, 'addtypecollection.html', {'form': form, 'i': i})


# Публичные коллекции
@login_required
def public(request):
    item = Items.objects.filter(is_public=1) & Items.objects.filter(visibility=1)
    img, item_feaches = [], []
    for i in item:
        img.append(Image.objects.filter(item=i.pk))
        item_feaches.append(Itemfeaches.objects.filter(item=i.pk))
    items = zip(item, img, item_feaches)
    return render(request, 'public.html', {'items': items})


@login_required
def like_item(request, item_id):
    username = request.user.username
    item_likes = Items.objects.get(item_id=item_id)
    like_filter = Likes.objects.filter(item_id=item_id, username=username).first()
    if like_filter is None:
        new_likes = Likes(item=item_likes, username=username)
        new_likes.save()
        item_likes.like = item_likes.like + 1
        item_likes.save()
        return redirect('/public')
    else:
        like_filter.delete()
        item_likes.like = item_likes.like - 1
        item_likes.save()
        return redirect('/public')

# Профиль
@login_required
def profile(request):
    username = request.user.username
    email = request.user.email
    return render(request, 'profile.html', {'user_name': username, 'user_email': email, 'other': CollectionProfile.objects.get(pk=request.user.id)})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')