from basic.database import db
from basic.tables import *
from dateutil.tz import gettz
import datetime

tzinfo = gettz('America/Chicago')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    goal_daily_calories = db.Column(db.Float(), default=0)
    goal_daily_protein = db.Column(db.Float(), default=0)
    goal_daily_carbohydrates = db.Column(db.Float(), default=0)
    goal_daily_fat = db.Column(db.Float(), default=0)
    goal_daily_activity = db.Column(db.Float(), default=0)
    application = db.relationship(
        'Application', backref='user', lazy=True, uselist=False)

    def data(self):
        return {'username': self.username,
                'firstName': self.first_name,
                'lastName': self.last_name,
                'goalDailyActivity': self.goal_daily_activity,
                'goalDailyCalories': self.goal_daily_calories,
                'goalDailyProtein': self.goal_daily_protein,
                'goalDailyCarbohydrates': self.goal_daily_carbohydrates,
                'goalDailyFat': self.goal_daily_fat,
                'admin': self.admin}


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(50), default='New Meal')
    date = db.Column(
        db.DateTime(), default=lambda: datetime.datetime.now(tzinfo))

    def data(self):
        return {'id': self.id, 'name': self.name, 'date': self.date.isoformat()}


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer)
    name = db.Column(db.String(50), default='New Food')
    calories = db.Column(db.Float(), default=0)
    protein = db.Column(db.Float(), default=0)
    carbohydrates = db.Column(db.Float(), default=0)
    fat = db.Column(db.Float(), default=0)

    def data(self):
        return {'id': self.id,
                'name': self.name,
                'calories': self.calories,
                'carbohydrates': self.carbohydrates,
                'protein': self.protein,
                'fat': self.fat}


class FoodArchetype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default='New Food')
    measure = db.Column(db.String(50), default='unit')
    calories = db.Column(db.Float(), default=0)
    protein = db.Column(db.Float(), default=0)
    carbohydrates = db.Column(db.Float(), default=0)
    fat = db.Column(db.Float(), default=0)

    def data(self):
        return {'id': self.id,
                'name': self.name,
                'measure': self.measure,
                'calories': self.calories,
                'carbohydrates': self.carbohydrates,
                'protein': self.protein,
                'fat': self.fat}


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(50), default='New Activity')
    duration = db.Column(db.Float(), default=0)
    date = db.Column(
        db.DateTime(), default=lambda: datetime.datetime.now(tzinfo))
    calories = db.Column(db.Float(), default=0)

    def data(self):
        return {'id': self.id,
                'name': self.name,
                'duration': self.duration,
                'date': self.date.isoformat(),
                'calories': self.calories
                }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default='New Product')
    image = db.Column(db.String(50), default='https://via.placeholder.com/350')
    price = db.Column(db.Float(), default=5.0)
    description = db.Column(db.String(16000000),
                            default='<Product Description Text>')
    tags = db.relationship('Tag', secondary=product_tag_link, lazy='subquery',
                           backref=db.backref('products', lazy=True))
    reviews = db.relationship('Review', backref='product', lazy=True)
    category_title = db.Column(db.Integer, db.ForeignKey('category.title'))
    cart = db.relationship('Cart', backref='product', lazy=True)

    def data(self):
        try:
            category = self.category.data()
        except:
            category = None
        return {'id': self.id,
                'name': self.name,
                'image': self.image,
                'price': self.price,
                'description': self.description,
                'category': category
                }


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    title = db.Column(db.String(50), default='Review')
    stars = db.Column(db.Float(), default=2.5)
    text = db.Column(db.String(16000000), default='<Product Review Text>')

    def data(self):
        return {'id': self.id,
                'title': self.title,
                'stars': self.stars,
                'text': self.text
                }


class Category(db.Model):
    title = db.Column(db.String(50), primary_key=True, unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def data(self):
        return self.title


class Tag(db.Model):
    value = db.Column(db.String(50), primary_key=True, unique=True)

    def data(self):
        return self.value


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    page = db.Column(db.String(50), default='home')
    back = db.Column(db.Boolean, default=False)
    dialogflow_updated = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=app_tag_link, lazy='subquery',
                           backref=db.backref('applications', lazy=True))
    messages = db.relationship('Message', backref='application', lazy=True)
    cart = db.relationship('Cart', backref='application', lazy=True)

    def data(self):
        return {'page': self.page,
                'back': self.back,
                'dialogflowUpdated': self.dialogflow_updated}


class Cart(db.Model):
    application_id = db.Column(db.Integer, db.ForeignKey(
        'application.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), primary_key=True)
    count = db.Column(db.Integer, default=1)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey(
        'application.id'), nullable=False)
    date = db.Column(
        db.DateTime(), default=lambda: datetime.datetime.now(tzinfo))
    is_user = db.Column(db.Boolean, default=False)
    text = db.Column(db.String(16000000), default='<Empty Message>')

    def data(self):
        return {'date': self.date.isoformat(),
                'isUser': self.is_user,
                'text': self.text,
                'id': self.id
                }


db.create_all()
