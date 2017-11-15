"""
    Routes
    ~~~~~~
"""
from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask import send_file
from flask import request

from wiki.core import Processor
from wiki.web.forms import EditorForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect

import pypandoc
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders


bp = Blueprint('wiki', __name__)


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)

@bp.route('/PDF_convert/<path:url>/', methods=['GET', 'POST'])
@protect
def PDF_convert(url):
    page = current_wiki.get_or_404(url)
    form = URLForm(obj=page)
    newurl = form.url.data
    current_wiki.move(url, newurl)
    pypandoc.convert('content/' + newurl + '.md', 'pdf', outputfile="wiki/web/PDF/" + newurl + ".pdf", extra_args=['-V', 'geometry:margin=1.5cm'])
    filename = "PDF/" + newurl + ".pdf"
    if os.path.exists("wiki/web/" + filename):
        return send_file(filename, as_attachment=True)
    return redirect(url_for('wiki.display', url=newurl))

@bp.route('/Send_email/', methods=['POST'])
@protect
def Send_email():
    url = request.form['file_location']
    pypandoc.convert('content/' + url + '.md', 'pdf', outputfile="wiki/web/PDF/" + url + ".pdf",
                     extra_args=['-V', 'geometry:margin=1.5cm'])
    username = 'updatewpy@gmail.com'
    password = 'pass1pass1234'
    to = 'arnzent1@mymail.nku.edu'

    if request.method == 'POST':
        to = request.form['email_addresses']
        if "," in to:
            ' ,'.join("'{0}'".format(x) for x in to)

        print(to)
        # to = to.split(",")

    message = MIMEMultipart()
    message['From'] = username
    message['To'] = "[" + to + "]"
    message['Subject'] = url.capitalize()
    body = "Email sent from wikiPy."

    body_send = MIMEText(body, 'plain')
    message.attach(body_send)
    filename = "wiki/web/PDF/" + url + ".pdf"

    element = MIMEBase('application', "octet-stream")
    element.set_payload(open(filename, "rb").read())
    encoders.encode_base64(element)
    element.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
    message.attach(element)


    # message.attach(MIMEText(message))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(username, to, message.as_string())
    server.close()
    return redirect(url_for('wiki.display', url=url))


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.index'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/create/')
def user_create():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404