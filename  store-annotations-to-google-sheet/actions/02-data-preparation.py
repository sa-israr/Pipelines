import json

def prepare(annotation):
    annotations= []
    base = {
        "item_name": annotation.get("metadata", {}).get("name", ""),
        "item_id": annotation.get("metadata", {}).get("id", ""),
        "project_id": annotation.get("project_id", ""),
        "team_id": annotation.get("team_id", "")
    }
    for instance in annotation.get("instances", []):
        row = base.copy()
        row.update({
            "component_id": instance.get("id", ""),
            "component_type": instance.get("type", ""),
            "component_className": instance.get("className", ""),
            "component_createdBy": instance.get("createdBy", {}).get("email", ""),
            "component_attributes": json.dumps(instance.get("attributes", []))  # serialize attributes
        })
        annotations.append(row)

    return annotations

def handler(event, context):
    prepared_data = []

    for annotation in context:  
        prepared_data.extend(prepare(annotation))

    return prepared_data
