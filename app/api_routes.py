from flask import Blueprint, request, jsonify
from app.dictionary_service import get_definition, generate_random_word

# Create a blueprint for API routes
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/definition', methods=['GET'])
def definition():
    """API endpoint for word definitions"""
    word = request.args.get('word', '')
    
    # Use the dictionary service to get definition
    definition_html = get_definition(word)
    
    # Return the HTML directly - will be inserted into the page
    return definition_html

@api.route('/random-word', methods=['GET'])
def random_word():
    """API endpoint for generating random words"""
    word = generate_random_word()
    
    # Check if it's a "real" word or a fallback motivational phrase
    is_from_api = not any(phrase in word for phrase in [
        "You are", "You can", "Stay", "Feel", "Keep", "Trust", 
        "Love is", "Dream", "Shine", "Make it", "You are", 
        "Keep moving", "Stay strong", "Be truly", "Embrace"
    ])
    
    return jsonify({
        "word": word,
        "isFromAPI": is_from_api
    })

# Add this to your main app.py file
# from api_routes import api
