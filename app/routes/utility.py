from flask import abort, make_response
from app.models.task import Task
from ..db import db

def validate_model(cls, id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"details": f"{cls.__name__} not found"}
        abort(make_response(invalid, 404))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if not model:    
        not_found = {"details": f"{cls.__name__} not found"}
        abort(make_response(not_found, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as e:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    sort_param = None
    if filters:
        sort_param = filters.get('sort')
        
        for attribute, value in filters.items():
            if attribute != 'sort' and hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    if sort_param == 'asc':
        query = query.order_by(cls.title.asc())
    elif sort_param == 'desc':
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.id)

    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]
    return models_response
