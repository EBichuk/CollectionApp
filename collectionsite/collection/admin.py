from django.contrib import admin
from collection.models import Image, Items, Collections, CollectionProfile
# Register your models here.

admin.site.register(Items)
admin.site.register(Image)
admin.site.register(Collections)
admin.site.register(CollectionProfile)