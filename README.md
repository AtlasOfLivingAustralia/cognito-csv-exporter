#  Export Amazon Cognito User Pool records into CSV

This project allows to export user records to CSV file from [Amazon Cognito User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)

## Instalation

In order to use this script you should have Python 3 installed on your platform
- run `pip3 install -r requirements.txt` (Python 3)

## Run export

To start export proccess:
- `$ python CognitoUserToCSV.py  --user-pool-id 'us-east-1_XXXXXXXXX' -attr Username email_verified given_name family_name UserCreateDate`
- Wait until you see output `INFO: End of Cognito User Pool reached`
- Find file `CognitoUsers.csv` that contains all exported users. [Example](https://github.com/hawkerfun/cognito-csv-exporter/blob/master/CognitoUsers.csv) 

### Script Arguments

- `--user-pool-id` [__Required__] - The user pool ID for the user pool on which the export should be performed
- `--region` [_Optional_] - The user pool region the user pool on which the export should be performed _Default_: `us-east-1`
- `-f` or `--file-name` [_Optional_] - CSV File name or path. _Default_: `CognitoUsers.csv`
- `--profile` [_Optional_] - The AWS IAM profile _Default_: `none`
- `--num-records` [_Optional_] - Max Number of Cognito Records tha will be exported. _Default_: __0__ - All
