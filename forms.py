from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, \
     SelectField, TextAreaField, validators, IntegerField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

# for users signing up for baking lessons


class SignUp(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=6, max=35)
    ])
    confirm = PasswordField('Repeat Password')
    email = EmailField('Email', validators=[
        InputRequired()])
    lesson_type = SelectField('Lesson type',
                              choices=['beginner class', 'intermediate class', 'advanced class'],
                              validators=[InputRequired()]
                              )

# for users requesting a customized cake order


class CustomOrder(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    Cake_layers = SelectField('cake layer', choices=[2, 3, 4], validators=[InputRequired(message='min of 2 layers')])
    sponge_flavor = SelectField('select flavors', choices=['Vanilla', 'chocolate', 'red velvet'])
    cake_writing = TextAreaField('any message on the cakes?')
    photo = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], message='images only!')
    ])
    submit = SubmitField('Order now')

# for admin to add products to the website


class AddProducts(FlaskForm):
    p_name = StringField('Name', validators=[InputRequired()])
    p_price = IntegerField('Price', validators=[InputRequired()])
    p_description = TextAreaField('Description', validators=[InputRequired()])
    image = FileField('photo', validators=[
        FileRequired()
    ])
