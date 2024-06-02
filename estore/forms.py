from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, ProductReview, Order


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(max_length=20, label= "Имя пользователя",widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Введите имя пользователя"
    }))
    first_name = forms.CharField(max_length=40, label= "Имя", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Введите имя"
    }))
    last_name = forms.CharField(max_length=30, label= "Фамилия", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Введите фамилию"
    }))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={
        'class': "form-control",
        'placeholder': "Введите электронную почту"
    }))
    password1 = forms.CharField(max_length=40,label= "Пароль", widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Введите пароль"
    }))
    password2 = forms.CharField(max_length=40,label="Подтверждение пароля", widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'placeholder': "Подтвердите пароль"
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):

    username = forms.CharField(max_length=20, label=("Имя пользователя"),
                               widget=forms.TextInput(attrs={
                                   'class': "form-control",
                                   'placeholder': "Имя пользователя"
                               }))
    password = forms.CharField(max_length=40, label="Пароль",
                               widget=forms.PasswordInput(attrs={
                                   'class': "form-control",
                                   'placeholder': "Введите пароль"
                               }))


class UserForm(forms.ModelForm):

    username = forms.CharField(max_length=20, label= "Имя пользователя",widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Введите имя пользователя"
    }))
    first_name = forms.CharField(max_length=40, label= "Имя", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Введите имя"
    }))
    last_name = forms.CharField(max_length=30, label= "Фамилия", widget=forms.TextInput(attrs={
        'class': "form-control",
        'placeholder': "Введите фамилию"
    }))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(attrs={
        'class': "form-control",
        'placeholder': "Введите электронную почту"
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'about', 'image']

        widgets = {

            "phone": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Номер телефона'
            }),

            "address": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Адрес"
            }),

            "about": forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "О себе"
            }),

            "image": forms.FileInput(attrs={
                'class': "form-control"
            })

        }


# Comments
class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']

    review = forms.CharField(widget=forms.Textarea(attrs={
        'class': "form-control",
        'placeholder': "Оставьте отзыв"
    }))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'address', 'email', 'order_note']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите полное имя"
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите номер телефона"
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите адрес"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Введите электронную почту"
            }),
            'order_note': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': "Введите комментарий к заказу"

            }),
        }
