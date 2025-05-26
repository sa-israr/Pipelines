import json

def reshaping_annotation(annotation):
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
            "instance_id": instance.get("id", ""),
            "instance_type": instance.get("type", ""),
            "instance_className": instance.get("className", ""),
            "instance_createdBy": instance.get("createdBy", {}).get("email", ""),
            "instance_attributes": json.dumps(instance.get("attributes", []))  # serialize attributes
        })
        annotations.append(row)
    return annotations

def handler(event, context):
    reshaped_annotations = []
    for annotation in context:  
        reshaped_annotations.extend(reshaping_annotation(annotation))
    return reshaped_annotations
