from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('profile/', profile, name='profile'),
    path('public/', public, name='public'),
    path('public/<int:item_id>', like_item, name='like_item'),
    path('collections/<int:collection_id>/', user_collection, name='user_collection'),
    path('item/<int:item_id>', items, name='items'),
    path('collections/<int:collection_id>/new', add_item_form, name='add_item'),
    path('collections/new_collection', add_collection, name='add_collection'),
    path('collections/new_collection/<int:i>/', add_type_collection, name='add_type_collection'),
    path('item/<int:item_id>/', del_item, name='delitem'),
    path('item/<int:item_id>/edit', edit_item, name='edititem'),
    path('accounts/', include('django.contrib.auth.urls'))
]
