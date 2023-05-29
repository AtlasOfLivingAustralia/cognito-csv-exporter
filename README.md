#  Export Amazon Cognito User Pool records into CSV

This project exports user records from an [Amazon Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html) to a CSV file that is suitable for [import into another User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-using-import-tool.html).

It also exports the Groups and users memberships

## Run the user export

To start the export process:
- `$ python CognitoUserToCSV.py  --user-pool-id 'ap-southeast-2_XXXXXXXXX'`
- Wait until you see output `INFO: End of Cognito User Pool reached`
- The file `CognitoUsers.csv` contains the exported users.

### Script Arguments

- `--user-pool-id` [__Required__] - The user pool ID for the user pool on which the export should be performed
- `--region` [_Optional_] - The user pool region the user pool on which the export should be performed _Default_: `us-east-1`
- `-f` or `--file-name` [_Optional_] - CSV File name or path. _Default_: `CognitoUsers.csv`
- `--profile` [_Optional_] - The AWS IAM profile _Default_: `none`
- `--num-records` [_Optional_] - Max Number of Cognito Records tha will be exported. _Default_: __0__ - All


## Run the group export

- `$python export_groups.py --user-pool-id ap-southeast-2_XXXXXXXXX --region ap-southeast-2 > groups.json`

### Script Arguments

- `--user-pool-id` [__Required__] - The user pool ID for the user pool on which the export should be performed
- `--region` [_Optional_] - The user pool region the user pool on which the export should be performed _Default_: `us-east-1`
- `--profile` [_Optional_] - The AWS IAM profile _Default_: `none`