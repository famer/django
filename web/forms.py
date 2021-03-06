from django import forms
from .models import City
from captcha.fields import CaptchaField

class NewJobForm(forms.Form):
    title = forms.CharField(label="Название вакансии", required=True, max_length=64)
    company = forms.CharField(label="Компания", required=False, max_length=64)
    tags = forms.CharField(label="Тэги, разделенные запятой", required=False, max_length=128)
    description = forms.CharField(widget=forms.Textarea(), label="Описание позиции", required=True)
    contacts = forms.CharField(label="Контакты для связи", required=True, max_length=64)
    city = forms.ModelChoiceField(queryset=City.objects.all(), label="Местоположение работы", required=True)
    net_salary_from = forms.IntegerField(label="ЗП на руки от", required=False, min_value=0)
    net_salary_to = forms.IntegerField(label="ЗП на руки до", required=False, min_value=0)
    captcha = CaptchaField(label="Капча")

    def __init__(self, *args, **kwargs):
        super(NewJobForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
