from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
import os
from forms import SignUp, CustomOrder, AddProducts
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import base64


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
# for my database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI','sqlite:///bakingShop.sqlite3')
app.config['SECRET_KEY'] = 'Mysweetlemonsapp'
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
# for uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


my_Email = os.environ.get('MYEMAIL')
my_Password = os.environ.get('MYPASSWORDLEMONS')


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


class AddProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(80), unique=True, nullable=False)
    p_price = db.Column(db.Numeric(10, 2), unique=False, nullable=False)
    p_description = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return '<AddProduct %r>' % self.p_name


@app.route('/Add product', methods=['GET', 'POST'])
def add_product():
    form = AddProducts(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST':
        p_name = form.p_name.data
        p_price = form.p_price.data
        p_description = form.p_description.data
        image = form.image.data
        # Read image data from the form and encode it in base64
        image_data = base64.b64encode(image.read())
        addpro = AddProduct(p_name=p_name, p_price=p_price, p_description=p_description, image=image_data)
        db.session.add(addpro)
        db.session.commit()
        flash(f'The product {p_name} has been added to your database', 'success')
        return redirect(url_for('admin_page'))
    return render_template('add_products.html', form=form)


@app.route('/admin')
def admin_page():
    products = AddProduct.query.all()
    return render_template('admin_pro.html', products=products)


@app.route('/Orders')
def cake_order():
    products = AddProduct.query.all()
    return render_template('Orders.html', products=products)


@app.route('/Chosen cake/<int:id>')
def chosen_cake(id):
    product = AddProduct.query.get_or_404(id)
    return render_template('Chosen_Cake.html', product=product)


@app.route('/Cart')
def cart():
    return render_template('cart.html')

@app.route('/base')
def base_page():
    return render_template('base.html')


# form for customized cake orders
@app.route('/custom_order', methods=['GET', 'POST'])
def custom_order():
    form = CustomOrder(CombinedMultiDict((request.files, request.form)))
    if form.is_submitted():
        my_result = request.form
        f = request.files['photo']
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'photos', filename
        ))
        return f'we have received your order thank you for shopping with us, ' \
               f'you should receive an order confirmation soon', print(my_result, f), \
               receive_email(email=my_result['email'],
                             layers=my_result['Cake_layers'],
                             flavors=my_result['sponge_flavor'],
                             msg=my_result['cake_writing'],
                             picture=filename)

    return render_template('custom_order.html', form=form)

# table for users who signed up


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    lesson_type = db.Column(db.String(180), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# table schema


with app.app_context():
    db.create_all()


# sign up form for baking classes


@app.route('/sign up', methods=['GET', 'POST'])
def signup_page():
    form = SignUp()
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
         username=form.username.data,
         password=hash_password,
         email=form.email.data,
         lesson_type=form.lesson_type.data
        )
        db.session.add(user)
        db.session.commit()
        flash('We have received your class registration, you will receive a confirmation email shortly')
        return redirect(url_for('home_page')), send_email()
    return render_template('signUp.html', form=form)


# with app.app_context():
#   db.drop_all()


# defines an email to be sent to the user confirming class registration
def send_email():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_Email, password=my_Password)
    connection.sendmail(from_addr=my_Email,
                        to_addrs=request.form["email"],
                        msg=f"subject:Registration received \n\n hey {request.form['username']}"
                            f"\n we have received you registration form we'll update you with lesson dates")
    connection.close()


# defines an email to be received by the business owner with custom order details
def receive_email(email, layers, flavors, msg, picture):
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_Email, password=my_Password)
    connection.sendmail(from_addr=my_Email,
                        to_addrs='shantelmolemoshi@gmail.com',
                        msg=f"subject:Custom Order! \n\ncustomer's email: {email}\n"
                            f"Number of layers: {layers}\n"
                            f" flavours : {flavors}\n "
                            f"message on the cake: {msg}\n"
                            f"picture: {picture} ")
    connection.close()


if __name__ == '__main__':
    app.run()
