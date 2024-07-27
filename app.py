from . import app
from flask import request, make_response, jsonify
from .models import *

# ThIs will make post req. onretreats, built to make the mock retreats table
@app.route('/retreat', methods=['POST'])
def create_retreat():
    try:
        data = request.json
        new_retreat = Retreats(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            date=data['date'],
            location=data['location'],
            price=data['price'],
            type=data['type'],
            condition=data['condition'],
            image=data['image'],
            tag=data['tag'],
            duration=data['duration']
        )
        db.session.add(new_retreat)
        db.session.commit()
        return jsonify({"message": "Retreat created successfully"}), 201


    except Exception as e:
        db.session.rollback()
        return make_response(
            jsonify({"errors": e}), 
            500
        )
    

'''
# This will return entries in the retreats
@app.route('/retreats', methods=['GET'])
def get_retreats():
    try:
        retreats = Retreats.query.all()
        
        if not retreats:
            return jsonify({"message": "No retreats found"}), 200
        
        print("Retreats fetched successfully")
        serialized_retreats = [
            {
                "id": retreat.id,
                "title": retreat.title,
                "description": retreat.description,
                "date": retreat.date,
                "location": retreat.location,
                "price": retreat.price,
                "type": retreat.type,
                "condition": retreat.condition,
                "image": retreat.image,
                "tag": retreat.tag,
                "duration": retreat.duration
            }
            for retreat in retreats
        ]
        
        return jsonify(serialized_retreats), 200
    
    except Exception as e:
        print(f"Error fetching retreats: {str(e)}")
        return jsonify({"Error": str(e)}), 400

'''

# This will make a post request in bookings
@app.route('/booking', methods=['POST'])
def create_booking():
    try:
        data = request.json
        
        # Check if the booking already exists 
        unique = Bookings.query.filter_by(user_id=data['user_id'], retreat_id=data['retreat_id']).first() # This will ensure no duplicate enties.
        if not unique:
            new_booking = Bookings(
                user_id=data['user_id'],
                user_name=data['user_name'],
                user_email=data['user_email'],
                user_phone=data['user_phone'],
                retreat_id=data['retreat_id'],
                retreat_title=data['retreat_title'],
                retreat_location=data['retreat_location'],
                retreat_price=data['retreat_price'],
                retreat_duration=data['retreat_duration'],
                payment_details=data['payment_details'],
                booking_date=int(time.time())  # current Unix timestamp
            )
            db.session.add(new_booking)
            db.session.commit()
            return jsonify({"message": "Booking created successfully"}), 201
        else:
            return jsonify({"message": "Booking already exists"}), 409

    except Exception as e:
        db.session.rollback()
        return make_response(
            jsonify({"errors": str(e)}), 
            500
        )
    
#This will ensure all features like paginations, filters & search API
@app.route('/retreats', methods=['GET'])
def get_retreats():
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        query = Retreats.query
        
        # Filtering
        filter_value = request.args.get('filter')
        if filter_value:
            query = query.filter(
                Retreats.title.ilike(f'%{filter_value}%') |
                Retreats.description.ilike(f'%{filter_value}%') |
                Retreats.location.ilike(f'%{filter_value}%') |
                Retreats.type.ilike(f'%{filter_value}%') |
                Retreats.condition.ilike(f'%{filter_value}%') |
                Retreats.tag.any(filter_value)     
            )
        
        # Field-specific filtering
        location = request.args.get('location')
        if location:
            query = query.filter_by(location=location)
        
        # Search
        search = request.args.get('search')
        if search:
            query = query.filter(
                Retreats.title.ilike(f'%{search}%') |
                Retreats.description.ilike(f'%{search}%') |
                Retreats.location.ilike(f'%{search}%') |
                Retreats.type.ilike(f'%{search}%') |
                Retreats.condition.ilike(f'%{search}%') |
                Retreats.tag.any(search)
            )
        
        # Pagination
        retreats = query.paginate(page=page, per_page=limit)
        
        # Serialization for putting out results
        result = {
            "total": retreats.total,
            "pages": retreats.pages,
            "current_page": retreats.page,
            "next_page": retreats.next_num,
            "prev_page": retreats.prev_num,
            "retreats": [retreat.serialize() for retreat in retreats.items]  
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error fetching retreats: {str(e)}")
        return jsonify({"Error": str(e)}), 400
