# from django import forms

# class ExamFormFields(forms.Form):
#     name1 = forms.CharField(label='name1', max_length=10, required=False)
#     name2 = forms.CharField(label='name2', max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': '이름'}))
#     age = forms.IntegerField(label='나이', required=False, initial=20)
#     intro = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=400, required=False)
#     birth = forms.DateField(required=False)
#     male = forms.BooleanField(label='남', required=False)
#     female = forms.BooleanField(label='여', required=False, initial=True)
#     mail1 = forms.EmailField(required=False)
#     mail2 = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
#     f = forms.FileField(label='image', max_length=4096, required=False)
#     img = forms.ImageField(label='img', required=False)
#     url1 = forms.URLField(label='fav', required=False)
#     url2 = forms.URLField(label='fav', required=True, widget=forms.TextInput(attrs={'placeholder': 'URL'}))