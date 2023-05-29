import boto3
import json
import sys
import argparse

###
# get a dump of all the groups and associated users from a cognito user pool
# uses 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_groups.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_users_in_group.html


REGION = ''
USER_POOL_ID = ''
LIMIT = 60
PROFILE = ''

""" Parse All Provided Arguments """
parser = argparse.ArgumentParser(description='Cognito User Pool export groups', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--user-pool-id', type=str, help="The user pool ID", required=True)
parser.add_argument('--region', type=str, default='us-east-1', help="The user pool region")
parser.add_argument('--profile', type=str, default='', help="The aws profile")
args = parser.parse_args()

if args.user_pool_id:
    USER_POOL_ID = args.user_pool_id
if args.region:
    REGION = args.region
if args.profile:
    PROFILE = args.profile

if PROFILE:
    session = boto3.Session(profile_name=PROFILE)
    client = session.client('cognito-idp', REGION)
else:
    client = boto3.client('cognito-idp', REGION)


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

# get all groups
try:
  # not handling pagination here, not expecting more than a few groups
  response = client.list_groups( UserPoolId = USER_POOL_ID, Limit = LIMIT )
except Exception as err:
    print("Something went wrong")
    print(err)
    sys.exit()     

# get the users for each group
for group in response['Groups']:
  users = get_users_in_group(client, group['GroupName']) 
  group['Users'] = users

print(json.dumps(response, indent=4, default=str))

