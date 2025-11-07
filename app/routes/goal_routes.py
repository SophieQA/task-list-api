from flask import Blueprint, Response
from app.models.goal import Goal
from app.db import db
from app.routes.utility import create_model, get_models_with_filters, validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.get("")
def get_goals():
    return get_models_with_filters(Goal, None)

@goals_bp.post("")
def create_goal():
    from flask import request
    request_body = request.get_json()
    
    return create_model(Goal, request_body)

@goals_bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    from flask import request
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body.get("title", goal.title)

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")