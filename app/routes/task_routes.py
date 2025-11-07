from flask import Blueprint, request, Response
from app.models.task import Task
from app.db import db
from app.routes.utility import create_model, get_models_with_filters, validate_model
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_tasks():
    return get_models_with_filters(Task, request.args)

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    return create_model(Task, request_body)

@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_model(Task, task_id)

    return task.to_dict(), 200

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.now()
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")