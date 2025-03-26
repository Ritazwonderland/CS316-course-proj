from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length, Regexp
from app.models.user import User
from flask_login import current_user
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120, message="Email must be less than 120 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, message="Password cannot be empty.")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email):
        # Sanitize email input
        sanitized_email = email.data.strip().lower()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', sanitized_email):
            raise ValidationError('Invalid email format.')
        
    def validate(self, extra_validators=None):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        try:
            sanitized_email = self.email.data.strip().lower()
            user = User.get_by_auth(sanitized_email, self.password.data)
            if user is None:
                self.email.errors.append('Invalid email or password')
                self.password.errors.append('Invalid email or password')
                return False
            return True
        except Exception as e:
            self.email.errors.append('An error occurred during login. Please try again.')
            return False

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[
        DataRequired(),
        Length(min=1, max=50, message="First name must be between 1 and 50 characters.")
    ])
    lastname = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=1, max=50, message="Last name must be between 1 and 50 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120, message="Email must be less than 120 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=1, message="Password cannot be empty.")
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        # Sanitize email input
        sanitized_email = email.data.strip().lower()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', sanitized_email):
            raise ValidationError('Invalid email format.')
        
        if User.email_exists(sanitized_email):
            raise ValidationError('Email already registered.')

    def validate_firstname(self, firstname):
        # Sanitize and validate firstname
        if not firstname.data.strip():
            raise ValidationError('First name cannot be empty.')
        if not re.match(r'^[a-zA-Z\s\'-]{1,50}$', firstname.data.strip()):
            raise ValidationError('First name contains invalid characters.')

    def validate_lastname(self, lastname):
        # Sanitize and validate lastname
        if not lastname.data.strip():
            raise ValidationError('Last name cannot be empty.')
        if not re.match(r'^[a-zA-Z\s\'-]{1,50}$', lastname.data.strip()):
            raise ValidationError('Last name contains invalid characters.')

class UserPurchasesForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[NumberRange(min=0, message="User ID must be a non-negative integer.")])
    submit = SubmitField('Get Purchases')

    def validate_user_id(self, field):
        print(f"Validating user_id: {field.data}")  # Debug print
        print(f"Type of user_id: {type(field.data)}")  # Debug print

class EditProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[
        DataRequired(),
        Length(min=1, max=50, message="First name must be between 1 and 50 characters.")
    ])
    lastname = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=1, max=50, message="Last name must be between 1 and 50 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120, message="Email must be less than 120 characters.")
    ])
    submit = SubmitField('Save Changes')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = current_user.email

    def validate_email(self, email):
        if email.data != self.original_email:
            sanitized_email = email.data.strip().lower()
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', sanitized_email):
                raise ValidationError('Invalid email format.')
            
            user = User.get_by_email(sanitized_email)
            if user:
                raise ValidationError('Email already registered to another account.')

    def validate_firstname(self, firstname):
        if not firstname.data.strip():
            raise ValidationError('First name cannot be empty.')
        if not re.match(r'^[a-zA-Z\s\'-]{1,50}$', firstname.data.strip()):
            raise ValidationError('First name contains invalid characters.')

class AddAddressForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    is_default = BooleanField('Set as Default Address')
    submit = SubmitField('Add Address')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[
        DataRequired(),
        Length(min=1, message="Password cannot be empty.")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=1, message="Password cannot be empty.")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')

    def validate_new_password(self, new_password):
        # Prevent using the same password
        if current_user.check_password(new_password.data):
            raise ValidationError('New password must be different from current password.')

class AddFundsForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0.")])
    submit = SubmitField('Add Funds')

class WithdrawFundsForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0.")])
    submit = SubmitField('Withdraw Funds')

class TopUpForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0.")])
    submit = SubmitField('Top Up')

class WithdrawForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0.")])
    submit = SubmitField('Withdraw')
