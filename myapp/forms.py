from django import forms
from .models import Group
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import WellBeingCard, CardSelection

class SignUpForm(UserCreationForm):
    class Meta:
        model = User  # デフォルトの User モデルを使用
        fields = ['username', 'password1', 'password2']  # 'name'フィールドは使用しません

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
        

class CardSelectionForm(forms.ModelForm):
    selected_cards = forms.ModelMultipleChoiceField(
        queryset=WellBeingCard.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # 画像をチェックボックスとして表示
        required=True
    )

    class Meta:
        model = CardSelection
        fields = ['selected_cards']
    
    def clean_selected_cards(self):
        selected = self.cleaned_data.get('selected_cards')
        if len(selected) != 3:
            raise forms.ValidationError("3枚のカードを選んでください。")
        return selected