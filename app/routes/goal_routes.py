from flask import Blueprint, Response, request
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from app.routes.route_utilities import create_model, get_models_with_filters, validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.get("")
def get_goals():
    return get_models_with_filters(Goal, None)

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    
    return create_model(Goal, request_body)

@goals_bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return goal.to_dict(), 200

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
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

@goals_bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body.get("task_ids", [])
    
    for task_id in task_ids:
        validate_model(Task, task_id)
    
    for task in goal.tasks:
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
    
    db.session.commit()
    
    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }
    
    return response_body, 200