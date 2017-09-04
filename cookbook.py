from flask import Flask, render_template, request, redirect, \
jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from database_setup import Base, User, Post
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///cbdb.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# App routes for website construction
@app.route('/')
def redirectHome():
    return redirect('/welcome')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    print(login_session)
    users = session.query(User).order_by(asc(User.name))
    return render_template(
        'welcome.html', users=users)


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/home/', defaults={"category_name": "All"})
@app.route('/home/<string:category_name>', methods=['GET'])
def home(category_name):
    count = 0
    if category_name == "All":
        ingSQL = 'SELECT ('
        stepSQL = '('
        while count < 15:
            count += 1
            ingSQL += '(ing' + str(count) + 'Title IS NOT NULL) + '
            stepSQL += '(step' + str(count) + ' IS NOT NULL) + '
            if count == 15:
                ingSQL += '(ing' + str(count) + 'Title IS NOT NULL)) '
                ingSQL += 'AS ingCount, '
                stepSQL += '(step' + str(count) + ' IS NOT NULL)) '
                stepSQL += 'AS stepCount, '
        endSQL = 'p.category, p.id, p.title, p.user_id, '
        endSQL += 'p.description, p.difficulty, p.postDate, u.name '
        endSQL += 'FROM Post p '
        endSQL += 'INNER JOIN User u ON u.id = p.user_id ORDER BY p.id DESC'
        strSQL = ingSQL + stepSQL + endSQL
        shortPosts = session.execute(strSQL)
    else:
        ingSQL = 'SELECT ('
        stepSQL = '('
        while count < 15:
            count += 1
            ingSQL += '(ing' + str(count) + 'Title IS NOT NULL) + '
            stepSQL += '(step' + str(count) + ' IS NOT NULL) + '
            if count == 15:
                ingSQL += '(ing' + str(count) + 'Title IS NOT NULL)) '
                ingSQL += 'AS ingCount, '
                stepSQL += '(step' + str(count) + ' IS NOT NULL)) '
                stepSQL += 'AS stepCount, '
        endSQL = ' p.category, p.id, p.title, p.user_id, p.description, '
        endSQL += 'p.difficulty, p.postDate, u.name FROM Post p '
        endSQL += 'INNER JOIN User u ON u.id = p.user_id '
        endSQL += 'WHERE p.category = "' + category_name + '" '
        endSQL += 'ORDER BY p.id DESC'
        strSQL = ingSQL + stepSQL + endSQL
        shortPosts = session.execute(strSQL)

    catSQL = 'SELECT category, COUNT(*) as sumCat FROM Post '
    catSQL += 'GROUP BY category ORDER BY sumCat DESC'
    categories = session.execute(catSQL)

    if 'username' not in login_session:
        flash(u'You must be signed in to post or view recipes!', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template('home.html',
                               pageTitle=category_name,
                               shortPosts=shortPosts,
                               categories=categories)


@app.route('/home/post/<int:post_id>/edit', methods=['GET', 'POST'])
def editpost(post_id):
    editedPost = session.query(Post).filter_by(id=post_id).one()

    if 'username' not in login_session:
        flash(u'You must be signed in to post or view recipes!', 'danger')
        return redirect(url_for('login'))
    if editedPost.user_id != login_session['user_id']:
        flash(u'You cannot edit a recipe that is not yours!', 'danger')
        return redirect(url_for('home'))
    if request.method == 'POST':
        count = 0
        listLength = len(request.form)
        strSQL = "UPDATE POST SET "
        for i in request.form:
            count += 1
            if count < listLength:
                if i not in ["newIngCount", "newStepCount"]:
                    strSQL += '"' + i + '"="' + request.form[i] + '", '
            else:
                if i not in ["newIngCount", "newStepCount"]:
                    strSQL += '"' + i + '"="' + request.form[i] + '"'
                    strSQL += ' WHERE id=' + str(post_id) + ';'
        session.execute(strSQL)
        session.commit()
        flash(u'Your recipe was successfully edited!', 'success')
        return redirect(url_for('viewpost', post_id=editedPost.id))
    else:
        return render_template('editpost.html', post=editedPost)


@app.route('/post/<int:post_id>/viewfull', methods=['GET'])
def viewpost(post_id):
    strSQL = 'SELECT * FROM Post p INNER JOIN User u ON u.id = p.user_id '
    strSQL += 'WHERE p.id=' + str(post_id)
    posts = session.execute(strSQL)

    if 'username' not in login_session:
        flash(u'You must be signed in to post or view recipes!', 'danger')
        return redirect(url_for('login'))
    else:
    	return render_template('viewpost.html', post_id=post_id, posts=posts)


@app.route('/home/post/<int:post_id>/delete', methods=['GET', 'POST'])
def deletepost(post_id):
    postToDelete = session.query(Post).filter_by(id=post_id).one()

    if 'username' not in login_session:
        flash(u'You must be signed in to post or view recipes!', 'danger')
        return redirect(url_for('login'))
    if postToDelete.user_id != login_session['user_id']:
        flash(u'You cannot delete a recipe that is not yours!', 'danger')
        return redirect(url_for('home'))
    else:
        session.delete(postToDelete)
        session.commit()
        flash(u'Your recipe was successfully deleted!', 'success')
        return redirect(url_for('home'))


@app.route('/home/post/new', methods=['GET', 'POST'])
def newpost():
    if 'username' not in login_session:
        flash(u'You must be signed in to post or view recipes!', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        count = 0
        listLength = len(request.form)
        insertString = "INSERT INTO POST("
        valueInsertString = "VALUES ("
        for i in request.form:
            count += 1
            if count < listLength:
                insertString += '"' + i + '", '
                valueInsertString += '"' + request.form[i] + '", '
            else:
                insertString += '"' + i + '", "user_id") '
                valueInsertString += '"' + request.form[i] + '", '
                valueInsertString += str(login_session['user_id']) + ')'

        strSQL = insertString + valueInsertString
        session.execute(strSQL)
        session.commit()
        flash(u'Your recipe was successfully posted!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('newpost.html')


@app.route('/logout')
def logout():
    if 'provider' in login_session:
        fbdisconnect()
        del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        return redirect('/welcome')


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.10/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.10/me?'
    url += 'access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print ("url sent for API access:%s"% url)
    # print ("API JSON result: %s" % result)
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.10/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Now logged in as %s" % login_session['username'])
    return redirect(url_for('home'))


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    print(login_session)
    print("result:         " + result)


# Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON Endpoints
@app.route('/home/JSON')
def PostHomeJSON():
    posts = session.query(Post).all()
    return jsonify(posts=[p.serialize for p in posts])


@app.route('/home/<string:category_name>/JSON')
def PostSpecJSON(category_name):
    posts = session.query(Post).filter_by(category=category_name).all()
    return jsonify(posts=[p.serialize for p in posts])


@app.route('/home/post/<int:post_id>/viewfull/JSON')
def PostJSON(post_id):
    post = session.query(Post).filter_by(id=post_id).one()
    return jsonify(post=post.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
