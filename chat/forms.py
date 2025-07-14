from django import forms


class ChatForm(forms.Form):
    user_input = forms.CharField(
        # label="Your Message",
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Ask me anything...",
        })
    )