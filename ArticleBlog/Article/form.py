from django import forms


class UserForm(forms.Form):
    name = forms.CharField(max_length=32, required=True, label='账户')
    password = forms.CharField(max_length=32, label='密码')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name == '7':
            self.add_error('name', '不能为7')
        else:
            return name
