import datetime
from flask import (
        request, 
        Blueprint, 
        render_template, 
        jsonify,
        redirect,
        abort
    )

from apps.app import mongo

from apps.url_shortener.utils import get_code

url_shortener = Blueprint(
    'url_shortener', __name__)


@url_shortener.route('/', methods=['GET'])
def index():
    """Rendering index template for VueJS application"""
    if request.method == "GET":
        return render_template('index.html')

@url_shortener.route('/shorten-url', methods=['POST'])   
def shorten_url():
    """Route for shorten a url"""

    payload = request.get_json()

    # Generate a random code
    code = get_code(6)
    
    # checking the random code already present in the
    # DB, if yes, regenerate code.
    while True:
        if "shorten_url" in mongo.db.list_collection_names():
            duplicate = mongo.db.shorten_url.find_one({'code': str(code)})
            if duplicate:
                code = get_code(6)
            else:
                break
        
    # expiration time set delete the item.
    expiration_days = datetime.timedelta(days=30)
    expiration = datetime.datetime.now() + expiration_days
    
    data = {
        "long_url": payload.get('url'),
        "short_url": code,
        "expiration": expiration
    }

    id = mongo.db.shorten_url.insert_one(data)
    

    return jsonify({
        "short_url": data.get("short_url"),
        "expiration": data.get("expiration")
    })


@url_shortener.route('/<url_code>', methods=['GET'])   
def get_long_url(url_code):
    """Route for redirect the long url."""
    result = mongo.db.shorten_url.find_one({'short_url': str(url_code)})

    if result:
        # checking expiration before sending to the long URL.
        now = datetime.datetime.now()
        if now > result.get('expiration'):
            mongo.db.shorten_url.delete_one({'short_url': str(url_code)})
            abort(404)
        return redirect(result.get('long_url'))
    else:
        abort(404)

