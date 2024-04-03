# owner/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, SBU
from django.forms import DateInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add custom classes to form fields
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter your username', 'autofocus': ''})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': '●●●●●●●●', 'aria-describedby': 'password'})

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_owner', 'is_hr', 'is_manager', 'is_team_leader', 'is_employee']

class ExtendedUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role_choices = (
        ('team_leader', 'Team Leader'),
        ('manager', 'Manager'),
        ('hr', 'HR'),
        ('employee', 'Employee'),
    )
    selected_role = forms.ChoiceField(choices=role_choices, required=True)
    custom_role = forms.CharField(required=False)
    manager = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_manager=True), required=False)
    team_leader = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_team_leader=True), required=False)
    hr = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_hr=True), required=False)
    sbu_units = forms.ModelChoiceField(queryset=SBU.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'joining_date','selected_role', 'manager', 'team_leader', 'hr', 'sbu_units']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'joining_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'selected_role': forms.Select(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'team_leader': forms.Select(attrs={'class': 'form-control'}),
            'hr': forms.Select(attrs={'class': 'form-control'}),
            'sbu_units': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_joining_date(self):
        joining_date = self.cleaned_data['joining_date']
        try:
            # Try to parse the date using a flexible format
            return forms.fields.DateField(input_formats=['%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y']).clean(joining_date)
        except forms.ValidationError:
            raise forms.ValidationError('Enter a valid date.')

    def clean(self):
        cleaned_data = super().clean()
        selected_role = cleaned_data.get('selected_role')
        custom_role = cleaned_data.get('custom_role')

        if selected_role == 'custom' and not custom_role:
            raise forms.ValidationError("Custom role must be provided if selected role is 'Custom Role'.")

        return cleaned_data  # No longer setting manager, team_leader, and hr to None here

    def clean_manager(self):
        manager_id = self.cleaned_data.get('manager')
        if manager_id:
            try:
                return CustomUser.objects.get(id=manager_id)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid manager ID.")
        return None

    def clean_team_leader(self):
        team_leader_id = self.cleaned_data.get('team_leader')
        if team_leader_id:
            try:
                return CustomUser.objects.get(id=team_leader_id)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid team leader ID.")
        return None

    def clean_sbu_units(self):
        sbu_name = self.cleaned_data.get('sbu_units')
        if sbu_name:
            try:
                return SBU.objects.get(name=sbu_name)
            except SBU.DoesNotExist:
                raise forms.ValidationError("Invalid SBU unit name.")
        return None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if self.cleaned_data['selected_role'] == 'custom':
            user.custom_role = self.cleaned_data['custom_role']
        else:
            setattr(user, f'is_{self.cleaned_data["selected_role"]}', True)

            # Set manager, team_leader, and hr fields only if the selected role is not 'employee'
            if self.cleaned_data['selected_role'] != 'employee':
                user.manager = self.cleaned_data.get('manager', None)
                user.team_leader = self.cleaned_data.get('team_leader', None)
                user.hr = self.cleaned_data.get('hr', None)
            else:
                # If selected role is 'employee' or 'team_leader', set manager, team_leader, and hr to None
                user.manager = None
                user.team_leader = None
                user.hr = None

                # If selected role is 'team_leader', assign manager based on the provided CSV data
                if self.cleaned_data['selected_role'] == 'team_leader':
                    user.manager = CustomUser.objects.get(username=self.cleaned_data['manager']) if self.cleaned_data[
                        'manager'] else None

        # Check if 'sbu_units' is provided in the form data
        sbu_units = self.cleaned_data.get('sbu_units', None)
        if sbu_units:
            user.sbu_units = sbu_units

        # Check if 'first_name' and 'last_name' are provided in the form data
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')

        if commit:
            user.save()

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_pic', 'first_name', 'last_name', 'email', 'company', 'sbu_units', 'joining_date']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'sbu_units': forms.Select(attrs={'class': 'form-control'}),
            'joining_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            user = kwargs.get('instance')
            if user:
                # Limit the queryset for the 'company' field to the user's company
                self.fields['company'].queryset = Company.objects.filter(id=user.company.id)

                # Limit the queryset for the 'sbu_units' field to the user's company's SBUs
                self.fields['sbu_units'].queryset = SBU.objects.filter(company=user.company)

class BulkUserUploadForm(forms.Form):
    file = forms.FileField(label='Select CSV File')
    widgets = {
        'file': forms.ClearableFileInput(attrs={'class': 'form-control'})
    }

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError('Invalid file format. Please upload a CSV file.')
        return file

