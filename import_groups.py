import boto3
import json
import argparse

####
# This takes the group export file created by export_groups.py and imports them into 
# the specified user pool. The Users must be imported first

parser = argparse.ArgumentParser(description='Cognito User Pool import groups', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--user-pool-id', type=str, help="The user pool ID", required=True)
parser.add_argument('--group-export-file', type=str, help="The user pool group export file", required=True)
args = parser.parse_args()

user_pool_id = args.user_pool_id
group_export_file = args.group_export_file

# Load the JSON file
with open(group_export_file, 'r') as file:
    data = json.load(file)

# Initialize boto3 client for Cognito Identity Provider
cognito_client = boto3.client('cognito-idp')

# Iterate over the groups
for group in data['Groups']:
    group_name = group['GroupName']
    description = group.get('Description', '')

    # Create the group in Cognito
    try:
        cognito_client.create_group(
            GroupName=group_name,
            Description=description,
            UserPoolId=user_pool_id
        )
    except cognito_client.exceptions.GroupExistsException:
        print(f"Group {group_name} already exists.")

    # Add users to the group
    for user in group.get('Users', []):
        try:
            cognito_client.admin_add_user_to_group(
                UserPoolId=user_pool_id,
                Username=user,
                GroupName=group_name
            )
        except Exception as e:
            print(f"Error adding user {user} to group {group_name}: {e}")


