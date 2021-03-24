"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, abort
from app.forms import PropertyForm
from app.models import Property
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mario Munroe")


@app.route('/property', methods=['POST', 'GET'])
def property():
    form = PropertyForm()

    # Validate profile info on submit
    if request.method == 'POST':
    
        # Get image data and save to upload folder
        image = request.files['photo']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Get the rest of the profile data
        title = form.title.data
        description = form.description.data
        rooms = form.rooms.data
        bathrooms = form.bathrooms.data
        price = form.price.data
        location = form.location.data
        propertyType = form.propertyType.data

        # Save data to database
        newProperty = Property(title=title, description=description, rooms=rooms, bathrooms=bathrooms, price=price, location=location, pType=propertyType, photo=filename )
        db.session.add(newProperty)
        db.session.commit()
        
        properties = Property.query.all()
        flash('Succcessfully Added')
        return redirect(url_for('properties', properties=properties))

    return render_template('property.html', form = form)



@app.route('/properties', methods=['POST', 'GET'])
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties = properties)

@app.route('/property/<propertyid>')
def propertyid(propertyid):
    propertyid=PropertyMod.query.get(propertyid)
    return render-template('propertyid.html', propertyid=propertyid)

def get_uploaded_images():
    rootdir = os.getcwd()
    list = []
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads/'):
        for file in files:
            list.append(file)
        return list

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         # if user is already logged in, just redirect them to our secure page
#         # or some other page like a dashboard
#         return redirect(url_for('property'))

#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     # Login and validate the user.
#     if request.method == 'POST' and form.validate_on_submit():
#         # Query our database to see if the username and password entered
#         # match a user that is in the database.
#         username = form.username.data
#         password = form.password.data

#         # user = UserProfile.query.filter_by(username=username, password=password)\
#         # .first()
#         # or
#         user = UserProfile.query.filter_by(username=username).first()

#         if user is not None and check_password_hash(user.password, password):
#             remember_me = False

#             if 'remember_me' in request.form:
#                 remember_me = True

#             # If the user is not blank, meaning if a user was actually found,
#             # then login the user and create the user session.
#             # user should be an instance of your `User` class
#             login_user(user, remember=remember_me)

#             flash('Logged in successfully.', 'success')

#             next_page = request.args.get('next')
#             return redirect(next_page or url_for('home'))
#         else:
#             flash('Username or Password is incorrect.', 'danger')

#     #flash_errors(form)
#     return render_template('login.html', form=form)

# @app.route("/logout")
# @login_required
# def logout():
#     # Logout the user and end the session
#     logout_user()
#     flash('You have been logged out.')
#     return redirect(url_for('home'))


# # user_loader callback. This callback is used to reload the user object from
# # the user ID stored in the session
# @login_manager.user_loader
# def load_user(id):
#     return UserProfile.query.get(int(id))


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
