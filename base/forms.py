from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator,
)

from django import forms
from .models import CustomUser, Folder, UploadedFile


class RegisterForm(UserCreationForm):

    username = forms.CharField(
        error_messages={"required": "사용자의 아이디를 넣어주세요"},
        validators=[
            MinLengthValidator(5, message="아이디의 길이는 5 ~ 12글자 입니다."),
            MaxLengthValidator(12, message="아이디의 길이는 5 ~ 12글자 입니다."),
            RegexValidator(
                regex="^[a-z0-9]+$",
                message="영소문자 | 숫자만 가능합니다",
                code="invaild",
            ),
        ],
    )
    nickname = forms.CharField(
        error_messages={"required": "이름을 넣어주세요"},
        validators=[
            MinLengthValidator(3, message="아이디의 길이는 3 ~ 8글자 입니다."),
            MaxLengthValidator(8, message="아이디의 길이는 3 ~ 8글자 입니다."),
            RegexValidator(
                regex="^[a-zA-Z가-힣]+$",
                message="영문 | 한글 문장만 가능합니다",
                code="invaild",
            ),
        ],
    )
    password1 = forms.CharField(
        error_messages={"required": "비밀번호를 넣어주세요"},
        validators=[
            MinLengthValidator(8, message="비밀번호의 길이는 8 ~ 16글자 입니다."),
            MaxLengthValidator(16, message="비밀번호의 길이는 8 ~ 16글자 입니다."),
            RegexValidator(
                regex="^[a-z0-9!@#$]+$",
                message="영소문자 | 숫자 | !@#$ 만 가능합니다",
                code="invaild",
            ),
        ],
    )

    password2 = forms.CharField(
        error_messages={
            "required": "확인 비밀번호를 넣어주세요",
        },
        validators=[
            MinLengthValidator(8, message="비밀번호의 길이는 8 ~ 16글자 입니다."),
            MaxLengthValidator(16, message="비밀번호의 길이는 8 ~ 16글자 입니다."),
            RegexValidator(
                regex="^[a-z0-9!@#$]+$",
                message="영소문자 | 숫자 | !@#$ 만 가능합니다",
                code="invaild",
            ),
        ],
    )

    class Meta:
        model = CustomUser
        fields = ("username", "nickname", "password1", "password2")
        # 1. 회원가입 필드에 username 하고 nickname , password 는 최소 길이 최대 길이가 존재 하고 vaildate 함.
        # 2. password 같은지 검사.

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                message="비밀번호가 서로 일치하지 않습니다.", code="password_mismatch"
            )

    def clean(self):
        clean_data = super().clean()
        if CustomUser.objects.count() >= 5:
            raise ValidationError("현재 사용자 추가 제한이 있습니다.")
        return clean_data


class LoginForm(forms.Form):
    username = forms.CharField(
        error_messages={"required": "사용자의 아이디를 넣어주세요"}
    )
    password = forms.CharField(
        error_messages={
            "required": "사용자의 비밀번호를 넣어주세요",
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        # authenticate 함수는 유효하지 않은 자격증명에 대해 None을 반환합니다.
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("유효하지 않은 아이디 | 패스워드 입니다.")

        # 사용자 객체를 폼 데이터에 추가할 수 있습니다.
        self.cleaned_data["user"] = user

        return self.cleaned_data

class FolderWithUserForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ("title", "user")
        

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ("file",)
