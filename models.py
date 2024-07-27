import time
from . import db

## DB model for retreats

class Retreats(db.Model):
    __tablename__ = "retreats"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # date = db.Column(db.Integer, default=lambda: int(time.time()), nullable=False)  # Auto set current Unix timestamp
    date = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.ARRAY(db.String), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Retreat {self.id}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date,
            "location": self.location,
            "price": self.price,
            "type": self.type,
            "condition": self.condition,
            "image": self.image,
            "tag": self.tag,
            "duration": self.duration
        }


## DB model for bookings

class Bookings(db.Model): 
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False)
    user_phone = db.Column(db.Integer, nullable=False)
    retreat_id = db.Column(db.Integer, nullable=False)
    retreat_title = db.Column(db.String(255), nullable=False)
    retreat_location = db.Column(db.String(255), nullable=False)
    retreat_price = db.Column(db.Float, nullable=False)
    retreat_duration = db.Column(db.Integer, nullable=False)
    payment_details = db.Column(db.String(255), nullable=False)
    booking_date = db.Column(db.Integer, default=lambda: int(time.time()), nullable=False)  #  Unix timestamp

    def serialize(self):
        return {
            "booking_id": self.id,
            "user_id" : self.user_id,
            "id - booked": self.retreat_id,
            "booked at": self.booking_date,
            "retreat_title" : self.retreat_title
        }