import os
from superannotate import SAClient

def get_sa_client(token):
    return SAClient(token=token)

def get_project_name(sa_client, project_id):
    project_meta = sa_client.get_project_by_id(project_id=str(project_id))
    return project_meta["name"]

def fetch_annotations(sa_client, project_name, item_names):
    annotations = sa_client.get_annotations(
        project=project_name,
        items=item_names        
    )
    return annotations
        
def handler(metadata, context):
    sa_client = get_sa_client(os.environ.get("SA_TOKEN"))
    
    project_id = context['after']['id']
    team_id = context['after']['team_id']
    
    project_name = get_project_name(sa_client, project_id)
    
    items = sa_client.list_items(project=project_name)
    item_names = [item["name"] for item in items]
    
    annotations = fetch_annotations(sa_client, project_name, item_names)
    
    if isinstance(annotations, list):
        for annotation in annotations:
            annotation["project_id"] = project_id  
            annotation["team_id"] = team_id
            
    return annotations
