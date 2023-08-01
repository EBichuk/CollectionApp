from django import forms
from .models import Collections, Feaches
from django.contrib.auth.forms import UserCreationForm


class AddForm(forms.Form):
    itemname = forms.CharField(max_length=45, label='Название')
    description = forms.CharField(max_length=250, label='Описание')
    image = forms.ImageField(label='Изображение')

    def __init__(self, *args, **kwargs):
        slugs_cnt = kwargs.pop('slugs_cnt', None)
        super(AddForm, self).__init__(*args, **kwargs)

        # Создание полей для определенной коллекции
        for i in slugs_cnt:
            type_f = i.datatype
            if type_f == 'int':
                self.fields[f'{i.feaches_id}'] = forms.IntegerField(label=f'{i.feache_name}')
            elif type_f == 'data':
                self.fields[f'{i.feaches_id}'] = forms.CharField(widget=forms.SelectDateWidget, label=f'{i.feache_name}')
            elif type_f == 'float':
                self.fields[f'{i.feaches_id}'] = forms.FloatField(label=f'{i.feache_name}')
            else:
                self.fields[f'{i.feaches_id}'] = forms.CharField(label=f'{i.feache_name}')


class AddCollection(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type_collection'].empty_label = "Шаблон не выбран"

    class Meta:
        model = Collections
        fields = ['name', 'description', 'img_url', 'type_collection']


class AddTypeCol(forms.Form):
    name = forms.CharField(max_length=45, label='Название')

    def __init__(self, *args, **kwargs):
        slugs_cnt = kwargs.pop('slugs_cnt', None)
        super(AddTypeCol, self).__init__(*args, **kwargs)

        for i in range(slugs_cnt):
            self.fields[f'{i}_name'] = forms.CharField(label='Название характеристики')
            self.fields[f'{i}_type'] = forms.ChoiceField(choices=(('int', 'целое число'), ('datatype', 'дата'), ('float', 'дробное число'), ('str', 'текст')), label=f'Тип характеристики')
