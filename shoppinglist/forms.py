from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    StringField,
    SubmitField,
    PasswordField,
    TextAreaField,
    URLField
)

from wtforms.validators import (
    InputRequired,
    NumberRange,
    Email,
    Length,
    EqualTo
)


class StringListField(TextAreaField):

    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = [line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []


class RegisterForm(FlaskForm):

    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=4, max=30, message="Your password must be between 4 and 30 characters long.")]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[InputRequired(), EqualTo("password",message="This password did not match the one in the password field.")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class ItemForm(FlaskForm):

    name = StringField("Name", validators=[InputRequired()])
    cost = IntegerField("Cost(USD)", validators=[InputRequired(), NumberRange(
        min=0, message="Invalid for number below 0")])
    priority = StringField("Priority", validators=[InputRequired()])
    submit = SubmitField("Add Item")


class ExtendedItemForm(ItemForm):

    memo = TextAreaField("Memo")
    requirement = StringListField("Requirement")
    submit = SubmitField("Update")


class ChoiceForm(FlaskForm):

    name = StringField("Name", validators=[InputRequired()])
    price = IntegerField("Price(USD)", validators=[InputRequired(), NumberRange(min=0, message="Invalid for number below 0")])
    brand = StringField("Brand")
    where = StringField("Where to Buy")
    address = URLField("Address or Link")
    submit = SubmitField("Add Choice")
