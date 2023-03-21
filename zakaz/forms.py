from django import forms
from .models import TypeWork, Order, OrderFile
from django.core.validators import MinValueValidator
from .validators import validate_number


class OrderForm(forms.ModelForm):
    cadastral_number = forms.CharField(
        validators=[validate_number],
        widget=forms.TextInput()
    )

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
        widget=forms.RadioSelect()
    )

    length = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Длина'})
    )

    length_unit = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_UNIT,
        widget=forms.RadioSelect()
    )

    width = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': ' Ширина'})
    )

    width_unit = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_UNIT,
        widget=forms.RadioSelect()
    )

    height = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Высота'})
    )

    height_unit = forms.ChoiceField(
        choices=Order.HEIGHT_UNIT,
        widget=forms.RadioSelect()
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
        fields = ('cadastral_number', 'region', 'area', 'city', 'street', 'house_number', 'building',
                  'square', 'square_unit', 'length',  'length_unit', 'width', 'width_unit', 'height', 'height_unit','type_work','title', 'name', 'surname', 
                  'father_name', 'phone_number', 'email')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['length_unit'].widget.attrs['class'] = 'custom-btn-check'
        self.fields['height_unit'].widget.attrs['class'] = 'custom-btn-check'
        self.fields['square_unit'].widget.attrs['class'] = 'custom-btn-check'
        self.fields['width_unit'].widget.attrs['class'] = 'custom-btn-check'


class OrderFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = OrderFile
        fields = ('file', )
