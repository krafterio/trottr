from typing import Any, cast
from edgy import Model
from fastapi import HTTPException
from core.database import registry


def snake_to_camel_case(snake_str: str) -> str:
    """Convert snake_case to CamelCase"""
    components = snake_str.split('_')

    return ''.join(word.capitalize() for word in components)


def get_model_class(model_name: str) -> Model:
    """Get Edgy model class from registry by snake_case name"""
    camel_case_name = snake_to_camel_case(model_name)

    for model_class in registry.models.values():
        if model_class.__name__ == camel_case_name:
            return cast(Model, model_class)

    raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")


def parse_sort(sort_str: str | None, columns: Any, query: Any) -> Any:
    """
    Parse the sort string and add order_by clauses to the query.
    Expected format: "field1 [asc|desc], field2 [asc|desc], ..."
    
    Args:
        sort_str: String containing sort criteria
        columns: Object containing model columns (e.g. Model.columns)
        query: Query to modify with order_by clauses
    
    Returns:
        Query modified with order_by clauses
    """
    if not sort_str:
        return query
    
    for sort_item in sort_str.split(","):
        sort_item = sort_item.strip()
        if " " in sort_item:
            field, direction = sort_item.split(" ", 1)
            direction = direction.lower()
        else:
            field = sort_item
            direction = "asc"
        
        if direction not in ["asc", "desc"]:
            raise HTTPException(status_code=400, detail="Direction de tri invalide. Utilisez 'asc' ou 'desc'")
        
        column = getattr(columns, field, None)
        if not column:
            raise HTTPException(status_code=400, detail=f"Champ de tri invalide: {field}")
        
        query = query.order_by(column.desc() if direction == "desc" else column.asc())
    
    return query 
