import os
import requests
from superannotate import SAClient
import json

def get_sa_client(token):
    return SAClient(token=token)

def flatten_annotation(annotation):
    flattened_rows = []
    base = {
        "metadata_name": annotation.get("metadata", {}).get("name", ""),
        "metadata_id": annotation.get("metadata", {}).get("id", ""),
        "metadata_projectId": annotation.get("metadata", {}).get("projectId", ""),
        "project_id": annotation.get("project_id", ""),
        "team_id": annotation.get("team_id", ""),
    }
    instances = annotation.get("instances", [])
    for inst in instances:
        row = base.copy()
        row.update({
            "instance_id": inst.get("id", ""),
            "instance_type": inst.get("type", ""),
            "instance_className": inst.get("className", ""),
            "instance_createdBy": inst.get("createdBy", {}).get("email", ""),
            "instance_attributes": json.dumps(inst.get("attributes", []))  # serialize to string
        })
        flattened_rows.append(row)
    return flattened_rows

def push_annotations_to_sheet(annotations):
    url = "https://script.google.com/macros/s/AKfycbx6kQ-vFZyUlYUR2Thrrp2HE6IlMagcpXNOaBSEtsTOMYNIcCbZrXn9HUyA6i4veEBcSw/exec"
    
    # Flatten all annotations into rows
    flattened = []
    for annotation in annotations:
        flattened.extend(flatten_annotation(annotation))
    
    payload = {
        "path": "Sheet1",
        "action": "write",
        "annotations": flattened
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print("Google Sheet response status:", response.status_code)
    print("Response text:", response.text)
    return response

def get_project_name(sa_client, project_id):
    project_meta = sa_client.get_project_by_id(project_id=str(project_id))
    return project_meta["name"]

def fetch_items_from_projects(sa_client, project_name):
    items = sa_client.list_items(project=project_name)
    item_names = [item["name"] for item in items]
    return item_names

def fetch_annotations(sa_client, project_name, item_names):
    annotations = sa_client.get_annotations(
        project=project_name,
        items=item_names,        
        data_spec="default"
    )
    return annotations
        
def handler(metadata, context):
    # Initialize SAClient
    sa_client = get_sa_client(os.environ.get("SA_TOKEN"))
    
    # Extract project_id and team_id from context
    project_id = context['after']['id']
    team_id = context['after']['team_id']

    project_name = get_project_name(sa_client, project_id)
    
    items = sa_client.list_items(project=project_name)
    item_names = [item["name"] for item in items]
    
    # Fetch annotations for these items
    annotations = fetch_annotations(sa_client, project_name, item_names)
    
    # Append project_id and team_id to each annotation (optional, but already flattened in flatten function)
    if isinstance(annotations, list):
        for annotation in annotations:
            annotation["project_id"] = project_id  
            annotation["team_id"] = team_id
    
    # Push flattened annotations to Google Sheets
    push_annotations_to_sheet(annotations)
    
    return annotations
