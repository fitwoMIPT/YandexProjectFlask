from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from .models import Item
from . import db

routes = Blueprint("routes", __name__)


@routes.route("/", methods=['GET', 'POST'])
@routes.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@routes.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html', user=current_user, items=items)


@routes.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Запись не должна быть пустой', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Запись создана!', category='success')
            return redirect(url_for('routes.home'))

    return render_template('create_post.html', user=current_user)


@routes.route("/delete-post/<id>", methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Запись не существует", category='error')
    elif current_user.id != post.id:
        flash('У вас нет прав удалить запись', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Запись удалена', category='success')

    return redirect(url_for('routes.home'))


@routes.route("/posts/<username>", methods=['GET', 'POST'])
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Пользователя с подобным именем не существует', category='error')
        return redirect(url_for('routes.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@routes.route("/create-comment/<post_id>", methods=['GET', 'POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Комментарий не должен быть пустым', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Записи не существует', category='error')

    return redirect(url_for('routes.home'))


@routes.route("/delete-comment/<comment_id>", methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Комментария не существует', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('У вас нет прав удалить комментарий.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('routes.home'))
