from django import forms
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'aria-describedby':'basic-addon1',
                                    'placeholder':'Username',
                                    }))
    password = forms.CharField(max_length = 20,
                                widget = forms.PasswordInput(attrs={
                                    'class':"form-control", 
                                    'aria-describedby':"basic-addon1",
                                    'placeholder':"Username",
                                    }))
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if User.objects.get(username=username).password != password :
            raise form.ValidationError("* Username and password do not match.")
        return cleaned_data

    def clean_username(self):
        username = cleaned_data.get('username')
        if not User.objects.get(username=username):
            raise forms.ValidationError("* Username is not exist.")
        return cleaned_data

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={
                                    'class':'form-control nameInput', 
                                    'placeholder':'First Name'}))
    last_name = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={
                                    'class':'form-control nameInput', 
                                    'placeholder':'Last Name'}))
    username = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'aria-describedby':'basic-addon1',
                                    'placeholder':'Username'}))
    email = forms.EmailField(max_length = 100,
                            widget = forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'aria-describedby':'basic-addon3',
                                    'placeholder':'Email'}))
    password1 = forms.CharField(max_length = 20,
                                widget = forms.PasswordInput(attrs={
                                    'class':"form-control", 
                                    'aria-describedby':"basic-addon2",
                                    'placeholder':"Password"}))
    password2 = forms.CharField(max_length = 20, 
                                widget = forms.PasswordInput(attrs={
                                    'class':"form-control", 
                                    'aria-describedby':"basic-addon2",
                                    'placeholder':"Confirm Password"}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        print password1, password2, last_name, first_name, email, username

        if not (password1 and password2 and last_name and first_name and email and username):
            raise forms.ValidationError("You have some field empty!")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data

    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email):
            raise forms.ValidationError("Email is already taken.")
        return email

class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        exclude = ['owner']
        widgets = {
            'text':Textarea(attrs={'form':"postform",
                                'class':"post-input",
                                'id': "post-text-area",
                                'maxlengt':"42",
                                'placeholder':"What do you want to say..."}),
        }
        error_messages={
            'text':{
                'required':"You should write something before post!",
                'max_length':"More than 42 words!",
            },
            'owner':{
                'required':"You should specify a user!",
            },
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['owner']
        widgets = {
            'bio':Textarea(attrs={'form':"EditProfileForm",
                                 'class':"post-input",
                                'placeholder':"Say something about yourself."}),
            'picture':forms.FileInput(),
        }

    # def clean_age(self):
    #     age = self.cleaned_data['age']
    #     if age < 0 or age > 200:
    #         raise forms.ValidationError("Give us a reasonable age...")
    #     return age

class SetPasswordForm(forms.Form):
    username = forms.CharField(max_length = 20,
                                widget = forms.TextInput(attrs={
                                    'class':'form-control', 
                                    'placeholder':'Username'
                                    }))
    password1 = forms.CharField(max_length = 20,
                                label = 'New Password',
                                widget = forms.PasswordInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"New Password",
                                    }))
    password2 = forms.CharField(max_length = 20, 
                                label = 'Confirm Password',
                                widget = forms.PasswordInput(attrs={
                                    'class':"form-control", 
                                    'placeholder':"Confirm Password"}))

    def clean(self):
        cleaned_data = super(SetPasswordForm, self).clean()
        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')
        if not (password1 and password2 and username):
            raise forms.ValidationError("You have some field empty")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("New Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username):
            raise forms.ValidationError("Username does not exist.")
        return username

class ForgetPasswordForm(forms.Form):
    email = forms.CharField(max_length = 40,
                            widget = forms.TextInput(attrs={
                                    'placeholder':'Email',
                                    'class':'form-control', 
                                    'aria-describedby':'basic-addon3'
                            }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError("Email field is empty.")
        user = User.objects.get(email = email)
        if not user:
            raise forms.ValidationError("Email is not exist in our record.")
        return email

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']
        widgets = {
            'content':Textarea(attrs={'form':"contentForm",
                                'class':"post-input",
                                'placeholder':"Add comments here..."}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        print "content validation:",content
        if not content:
            raise forms.ValidationError("empty")
        return content
