import os
import json
import re
from superannotate import SAClient

def get_sa_client(token):
    return SAClient(token=token)

def extract_input_values(data):
    """Extract input values from the updated JSON structure including project ID"""
    results = []
    for item in data:
        item_name = item['metadata']['name']
        item_id = item['metadata']['id']
        project_id = item['metadata']['projectId']  
        team_id = item['team_id']
        
        inputs = {'input_1': None, 'input_2': None, 'input_3': None}
        for instance in item['instances']:
            class_name = instance['className']
            if class_name in inputs and instance['attributes']:
                inputs[class_name] = instance['attributes'][0]['name']
        
        results.append({
            'item_name': item_name,
            'item_id': item_id,
            'project_id': project_id,
            'team_id': team_id,
            'input_1': inputs['input_1'],
            'input_2': inputs['input_2'],
            'input_3': inputs['input_3']
        })
    return results

def extract_prefix_from_items(extracted_values):
    """Extract common prefix from item names by removing numeric suffixes"""
    if not extracted_values:
        return "default"
    first_item_name = extracted_values[0]['item_name']
    prefix = re.sub(r'_\d+$', '', first_item_name)
    
    return prefix if prefix else "default"

def find_common_prefix(strings):
    """Find the longest common prefix among a list of strings"""
    if not strings:
        return ""
    
    prefix = strings[0]
    for string in strings[1:]:
        while not string.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix.rstrip('_')

def update_tab_values(sa_client, project_id, item_id, tab1_value, tab2_value, tab3_value):
    """Update both tab textarea values using project_id and item_id"""
    try:
        with sa_client.item_context(project_id, item_id, overwrite=True) as context:
            context.set_component_value('annotation_tab1', tab1_value)
        print(f"Tab 1 updated for item {item_id}")
    except Exception as e:
        if "JSONDecodeError" not in str(e):
            print(f"Tab 1 error for item {item_id}: {e}")
    
    try:
        with sa_client.item_context(project_id, item_id, overwrite=True) as context:
            context.set_component_value('annotation_tab2', tab2_value)
        print(f"Tab 2 updated for item {item_id}")
    except Exception as e:
        if "JSONDecodeError" not in str(e):
            print(f"Tab 2 error for item {item_id}: {e}")
    
    try:
        with sa_client.item_context(project_id, item_id, overwrite=True) as context:
            context.set_component_value('annotation_tab3', tab3_value)
        print(f"Tab 3 updated for item {item_id}")
    except Exception as e:
        if "JSONDecodeError" not in str(e):
            print(f"Tab 3 error for item {item_id}: {e}")

def handler(event, context):
    
    sa_client = get_sa_client(os.environ.get("SA_TOKEN"))
    
    
    extracted_values = extract_input_values(context)  
    print("Extracted values:")
    print(json.dumps(extracted_values, indent=2))
    
    prefix = extract_prefix_from_items(extracted_values)
    print(f"\nExtracted prefix: '{prefix}'")
    
    project = "trying101"
    sa_client.generate_items(project, len(extracted_values), prefix)
    
    for item in extracted_values:
        print(f"Updating tabs for {item['item_name']}...")
        
        update_tab_values(
            sa_client,              
            project,
            item['item_name'],           
            str(item['input_1']),   
            str(item['input_2']),   
            str(item['input_3'])    
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing completed successfully')
    }