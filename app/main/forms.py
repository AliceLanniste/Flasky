from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Required,Length


class NameForm(Form):
    body = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(Form):
    body = TextAreaField('What is on your mind?',validators=[Required()])
    submit = SubmitField('Submit')


# editprofileform
class EditProfileForm(Form):
    name=StringField('YOUR NAME',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')
