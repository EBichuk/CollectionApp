from django.db import models
from collectionsite import settings
from django.contrib.auth.models import User


class Collections(models.Model):
    collection_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Имя коллекции')
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name='Описание')
    visiblity = models.IntegerField()
    like = models.IntegerField()
    img_url = models.ImageField(upload_to='collections/', verbose_name='Изображение')
    type_collection = models.ForeignKey('Typecollections', models.DO_NOTHING, verbose_name='Шаблон')
    collection_profile = models.ForeignKey('CollectionProfile', models.DO_NOTHING, db_column='collection_profile')

    class Meta:
        managed = False
        db_table = 'collections'

    def __str__(self):
        return self.name


class Feaches(models.Model):
    feaches_id = models.AutoField(primary_key=True)
    feache_name = models.CharField(max_length=45)
    datatype = models.CharField(max_length=8)
    type_collection = models.ForeignKey('Typecollections', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'feaches'


class Itemfeaches(models.Model):
    item_feache_id = models.AutoField(primary_key=True)
    data = models.CharField(max_length=45)
    feaches = models.ForeignKey(Feaches, models.DO_NOTHING)
    item = models.ForeignKey('Items', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'itemfeaches'


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=45)
    description = models.CharField(max_length=250, blank=True, null=True)
    visibility = models.IntegerField()
    like = models.IntegerField()
    collection = models.ForeignKey(Collections, models.DO_NOTHING)
    is_public = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'items'


class Typecollections(models.Model):
    type_collection_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    visibility = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'typecollections'

    def __str__(self):
        return self.name


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=45)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=45)
    visibility = models.IntegerField()
    img_url = models.ImageField(upload_to='users/')

    class Meta:
        managed = False
        db_table = 'users'


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='item/')
    item = models.ForeignKey('Items', models.DO_NOTHING)


class CollectionProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    phone = models.CharField(unique=True, max_length=45)
    visibility = models.IntegerField()
    img_url = models.ImageField(upload_to='users/')
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'collection_profile'


class Likes(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey('Items', models.DO_NOTHING)
    username = models.CharField(unique=True, max_length=45)
