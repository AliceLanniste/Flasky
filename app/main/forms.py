from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Required,Length
from flask.ext.pagedown.fields import PageDownField

class NameForm(Form):
    body = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class PostForm(Form):
    body = PageDownField("What's on your mind?",validators=[Required()])
    submit = SubmitField('Submit')

# editprofileform
class EditProfileForm(Form):
    name=StringField('YOUR NAME',validators=[Length(0,64)])
    location=StringField('Location',validators=[Length(0,64)])
    about_me=TextAreaField('About me')
    submit=SubmitField('Submit')
