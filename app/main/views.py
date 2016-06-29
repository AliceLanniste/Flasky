from datetime import datetime
from flask import render_template,session,redirect,url_for,flash,request,current_app
from flask.ext.login import login_required,current_user
from . import main
from .forms import NameForm,EditProfileForm,PostForm
from .. import db
from .. models import User,Permission,Post
from ..decorator import admin_required, permission_required

@main.route('/',methods=['GET','POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body =form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,
                 per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items
    return render_template('index.html',form=form,posts=posts,pagination=pagination)
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('index.html',form=form,posts=posts)
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


#post route
@main.route('/post/<int:id>')
def post(id):
    post=Post.query.get_or_404(id)
    return render_template('post.html',posts=[post])

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('you are already following this user')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('you are now following %s.' % username)
    return redirect(url_for('.user',username=username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('your followers are logouted.')
        return  redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('you are unfollowed')
        return redirect(url_for('.user',username=username))
    current_user.unfollow(user)
    flash('you are following %s' % username)
    return redirect(url_for('.user',username=username))

@main.route('/followers/<username>')
def followers(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return  redirect('.index')
    page=request.args.get('page',1,type=int)
    pagination=user.followers.paginate(
        page,per_page=current_app.config['FLASKY_FOLLOWERS_PRE_PAGE'],
        error_out=False)
    follows=[{'user':item.follower,'timestamp':item.timestamp}
             for item in pagination.items]
    return render_template('followers.html',user=user,title='Followers of',
                           endpoint='.followers',pagination=pagination,
                           follows=follows)

@main.route('/followed_by/<username>')
def followed_by(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect('.index')
    page=request.args.get('page',i,type=int)
    pagination=user.followed.paginate(
        page,per_page=current_app.config['FLASKY_FOLLOWERES_PAGE'],
        error_out=False)
    follows=[{'user':item.follower,'timestamp':item.timestamp}
             for item in pagination.items]
    return render_template('followers.html',user=user,title='Followed by',
						   endpoint='.followed_by',pagination=pagination,
						   follows=follows)



