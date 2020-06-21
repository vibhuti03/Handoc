from django import forms
from .models import Post

class HomeForm(forms.ModelForm):
    Title=forms.CharField(label=False,widget=forms.Textarea(attrs={"placeholder":"Type your title here..",'height':"100%","rows":250, "cols":90,'style':'height: 25px;width: 750px;'}))
    Document=forms.CharField(label=False,widget=forms.Textarea(attrs={"placeholder":"Type your document contents here..",'height':"100%","rows":250, "cols":90,'style':'height: 410px;width: 750px;'}))

    class Meta:
        model=Post
        fields = ('Title','Document',)

