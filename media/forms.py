from django import forms
# from .validators import validate_cadastral_number
from .models import TypeWork, Order, OrderFiles
from django.core.validators import MinValueValidator


class OrderForm(forms.ModelForm):
    cadastral_number = forms.CharField(
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
    square_volume = forms.ChoiceField(
        choices=Order.SQUARE_VOLUME,
        widget=forms.Select()
    )
    length = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Длина'})
    )
    length_volume = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_VOLUME,
        widget=forms.Select()
    )
    width = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': ' Ширина'})
    )
    width_volume = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_VOLUME,
        widget=forms.Select()
    )
    height = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Высота'})
    )
    height_volume = forms.ChoiceField(
        choices=Order.HEIGHT_VOLUME,
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
        fields = ('cadastral_number', 'region', 'area', 'city', 'street', 'house_number', 'building',
                  'square', 'square_volume', 'length',  'length_volume', 'width', 'width_volume', 'height', 'height_volume','type_work','title', 'name', 'surname', 
                  'father_name', 'phone_number', 'email')
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'application--form__data-input border'
        self.fields['house_number'].widget.attrs['class'] = 'border mr-2 application--form--input-group__house'
        self.fields['building'].widget.attrs['class'] = 'border application--form--input-group__house'
    
        self.fields['square'].widget.attrs['class'] = 'form-control data-inputdimensions'
        self.fields['length'].widget.attrs['class'] = 'form-control'
        self.fields['height'].widget.attrs['class'] = 'form-control'
        self.fields['width'].widget.attrs['class'] = 'form-control'

        self.fields['square_volume'].widget.attrs['class'] = 'select'
        self.fields['length_volume'].widget.attrs['class'] = 'select'
        self.fields['width_volume'].widget.attrs['class'] = 'select'
        self.fields['height_volume'].widget.attrs['class'] = 'select'

        self.fields['title'].widget.attrs['class'] = 'application--form--textarea__text form-control'
        self.fields['title'].widget.attrs['style'] = 'margin-top:20px;'

        self.fields['name'].widget.attrs['class'] = 'form-control application--form__data-input'
        self.fields['surname'].widget.attrs['class'] = 'form-control application--form__data-input'
        self.fields['father_name'].widget.attrs['class'] = 'form-control application--form__data-input'

        self.fields['phone_number'].widget.attrs['class'] = 'form-control application--form__data-input'
        self.fields['email'].widget.attrs['class'] = 'form-control application--form__data-input'



class OrderFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = OrderFiles
        fields = ('file', )
