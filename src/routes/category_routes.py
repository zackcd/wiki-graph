from flask import Blueprint, jsonify, current_app


bp = Blueprint('category', __name__)

@bp.route('/category/<category>', methods=['GET'])
def process_category(category):
    try:
        # Get the service from app context instead of creating new instance
        service = current_app.category_service
        result = service.process_category(category)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500 