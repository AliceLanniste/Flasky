from datetime import datetime
from flask import render_template,session,redirect,url_for,flash
from flask.ext.login import login_required,current_user
from . import main
from .forms import NameForm,EditProfileForm,PostForm
from .. import db
from .. models import User,Permission,Post

@main.route('/',methods=['GET','POST'])
def index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body =form.body.data,
					author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	posts = Post.query.order_by(Post.timestamp.desc()).all()
	return render_template('index.html',form=form,posts=posts)
# def index():
# 	form=NameForm()
# 	if form.validate_on_submit():
# 		user=User.query.filter_by(username=form.name.data).first()
# 		if user is None:
# 			user=User(username=form.name.data)
# 			db.session.add(user)
# 			session['known']=False
# 		else:
# 			session['known']=True
# 		session['name']=form.name.data
# 		form.name.data=''
# 		return render_template(url_for('.index'))
# 	return render_template('index.html',form=form,name=session.get('known',False),current_time=datetime.utcnow())

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user,posts=posts)
	

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me= form .about_me.data
		db.session.add(current_user)
		flash('updated!')
		return redirect(url_for('.user',username = current_user.username))
	form.name.data = 'aa'
	form.about_me.data = 'please write there'
	return  render_template('edit_profile.html',form = form)


