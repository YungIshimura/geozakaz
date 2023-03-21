from django import forms
from .models import TypeWork, Order, OrderFile
from django.core.validators import MinValueValidator
from .validators import validate_number


class OrderForm(forms.ModelForm):
    cadastral_number = forms.CharField(
        validators=[validate_number],
        widget=forms.TextInput(attrs={'placeholder': 'Кадастровый номер'}))

    street = forms.CharField()

    house_number = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'class':'border mr-2 application--form--input-group__house'})
    )

    building = forms.IntegerField(
        validators=[MinValueValidator(1)]
    )

    square = forms.IntegerField(
        validators=[MinValueValidator(1)]
    )

    square_unit = forms.ChoiceField(
        choices=Order.SQUARE_UNIT,
        widget=forms.Select()
    )

    length = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Длина'})
    )

    length_unit = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_UNIT,
        widget=forms.Select()
    )

    width = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': ' Ширина'})
    )

    width_unit = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_UNIT,
        widget=forms.Select()
    )

    height = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Высота'})
    )

    height_unit = forms.ChoiceField(
        choices=Order.HEIGHT_UNIT,
        widget=forms.Select()
    )

    type_work = forms.ModelMultipleChoiceField(
        queryset=TypeWork.objects.all(), 
        widget=forms.CheckboxSelectMultiple()
    )

    title = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Название объекта'})
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'})
    )

    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'})
    )

    father_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше отчество'})
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона'})
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите номер телефона'}))

    class Meta:
        model = Order
        fields = '__all__'


class OrderFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = OrderFile
        fields = ('file', )
