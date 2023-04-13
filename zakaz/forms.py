from django import forms

from django.contrib.postgres.forms import SimpleArrayField
from .models import TypeWork, Order, OrderFile, WorkObjective
from django.core.validators import MinValueValidator
from .validators import validate_number
from phonenumber_field.formfields import PhoneNumberField


class CadastralNumberForm(forms.Form):
    cadastral_number = forms.CharField(
        # validators=[validate_number],
        widget=forms.TextInput(
            attrs={'placeholder': 'Введите кадастровый номер', 'name': 'query'}
        ))


class OrderForm(forms.ModelForm):
    cadastral_numbers = SimpleArrayField(forms.CharField(
        # validators=[validate_number],
        widget=forms.TextInput(attrs={'placeholder': 'Кадастровый номер'}),
    ))

    street = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Улица'}),
        required=True
    )

    house_number = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Номер дома'}),
        required=True
    )

    building = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Корпус/Строение'}),
        required=False
    )

    square = forms.DecimalField(
        label='Площадь',
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Площадь'}),
        required=True
    )

    square_unit = forms.ChoiceField(
        choices=Order.SQUARE_UNIT,
        widget=forms.Select(attrs={'class': "custom-btn-check"})
    )

    length = forms.DecimalField(
        label='Длина',
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Длина'}),
        required=True
    )

    length_unit = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_UNIT,
        widget=forms.Select()
    )

    width = forms.DecimalField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': ' Ширина'}),
        required=False
    )

    width_unit = forms.ChoiceField(
        choices=Order.LENGTH_AND_WIDTH_UNIT,
        widget=forms.Select(),
        required=False
    )

    height = forms.DecimalField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={'placeholder': 'Высота'}),
        required=False
    )

    height_unit = forms.ChoiceField(
        choices=Order.HEIGHT_UNIT,
        widget=forms.Select(),
        required=False
    )

    type_work = forms.ModelMultipleChoiceField(
        queryset=TypeWork.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Комментарий к заказу'}),
        required=False
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
        required=True
    )

    surname = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
        required=True
    )

    father_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ваше отчество'}),
        required=False
    )

    phone_number = PhoneNumberField()

    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'placeholder': 'Введите адрес почты'}),
        required=True
    )

    purpose_building = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Выберите/Введите назначение здания'}),
        required=True,
    )

    work_objective = forms.ModelChoiceField(
        queryset=WorkObjective.objects.all(),
        widget=forms.Select(),
        required=True
    )

    class Meta:
        model = Order
        fields = ('cadastral_numbers', 'region', 'area', 'city', 'street',
                  'house_number', 'building', 'square', 'square_unit', 'length',
                  'length_unit', 'width', 'width_unit', 'height', 'height_unit',
                  'type_work', 'comment', 'name', 'surname', 'father_name',
                  'phone_number', 'email', 'purpose_building', 'work_objective')


    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['cadastral_numbers'].required = False

        self.fields['purpose_building'].empty_label = 'Нажмите, чтобы выбрать назначение здания'
        self.fields['work_objective'].empty_label = 'Нажмите, чтобы выбрать цель работ'

        self.fields['length_unit'].widget.attrs['class'] = 'custom-btn-check'
        self.fields['height_unit'].widget.attrs['class'] = 'custom-btn-check'
        self.fields['square_unit'].widget.attrs['class'] = 'custom-btn-check'
        self.fields['width_unit'].widget.attrs['class'] = 'custom-btn-check'

        self.fields['work_objective'].widget.attrs['class'] = 'form-select'

class OrderFileForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True, 'name': 'file[]'}),
        required=False
    )

    class Meta:
        model = OrderFile
        fields = ('file',)
