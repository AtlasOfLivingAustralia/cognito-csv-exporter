import boto3
import json
import sys
import argparse

###
# get a dump of all the groups and associated users from a cognito user pool
# uses 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_groups.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_users_in_group.html


USER_POOL_ID = ''
LIMIT = 60

""" Parse All Provided Arguments """
parser = argparse.ArgumentParser(description='Cognito User Pool export groups', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--user-pool-id', type=str, help="The user pool ID", required=True)
args = parser.parse_args()

if args.user_pool_id:
    USER_POOL_ID = args.user_pool_id

client = boto3.client('cognito-idp')

###
# Get all the users in a group, handles pagination
def get_users_in_group(cognito_idp_client, group_name, next_pagination_token =''):  
   users = []

   try:
     if next_pagination_token:
       response = client.list_users_in_group(
         UserPoolId = USER_POOL_ID,
         GroupName = group_name,
         Limit = LIMIT,
         NextToken = next_pagination_token
       )
     else:
       response = client.list_users_in_group(
         UserPoolId = USER_POOL_ID,
         GroupName = group_name,
         Limit = LIMIT
       )
   except Exception as err:
     print("Something went wrong")
     print(err)
     sys.exit()     

   for user in response['Users']:
     users.append(user['Username'])

   if 'NextToken' in response:
     users = users + get_users_in_group(client, group_name, response['NextToken'])

   return users

##
# Function to list all groups with pagination
def get_all_groups(user_pool_id, limit):
    pagination_token = None
    all_groups = []

    while True:
        print('makeing req')
        if pagination_token:
            response = client.list_groups(UserPoolId = USER_POOL_ID, Limit = LIMIT, NextToken = pagination_token)
        else:
            response = client.list_groups(UserPoolId = USER_POOL_ID, Limit = LIMIT)

        all_groups.extend(response.get('Groups', []))

        pagination_token = response.get('NextToken')
        if not pagination_token:
            break

    return all_groups

all_groups = get_all_groups(USER_POOL_ID, LIMIT )

# get the users for each group
for group in all_groups:
  users = get_users_in_group(client, group['GroupName']) 
  group['Users'] = users

print(json.dumps(all_groups, indent=4, default=str))

