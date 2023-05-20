import boto3, json, os, decimal

# Getting state machine arns 
sm = boto3.client('stepfunctions', region_name="us-east-1") 
#SM_ARN = 'YOUR_STATEMACHINE_ARN' 



def lambda_handler(event, context): 
    # Print event data to logs .. 
    print("Received event: " + json.dumps(event))

    # Load data coming from APIGateway
    data = json.loads(event['body'])
    data['waitSeconds'] = int(data['waitSeconds'])
    
    # Sanity check that all of the parameters we need have come through from API gateway
    # Mixture of optional and mandatory ones
    checks = []
    checks.append('waitSeconds' in data)
    checks.append(type(data['waitSeconds']) == int)
    checks.append('message' in data)

    SM_ARN = get_sm_arn()

    # if any checks fail, return error to API Gateway to return to client
    if False in checks:
        response = {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps( { "Status": "Success", "Reason": "Input failed validation" }, cls=DecimalEncoder )
        }
    # If none, start the state machine execution and inform client of 2XX success :)
    else: 
        sm.start_execution( stateMachineArn=SM_ARN, input=json.dumps(data, cls=DecimalEncoder) )
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            "body": json.dumps( {"Status": "Success"}, cls=DecimalEncoder )
        }
    return response



class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
    
def get_sm_arn(): 
    response = sm.list_state_machines()['stateMachines']
    print(response)
    for element in response: 
        if(element["name"] == "PetCuddleOTronStateMachine"): 
            return element["stateMachineArn"]
    print("[api_lambda.py get_sm_arn() line 55] State Machine %s could not be found. Response %s" % ("PetCuddleOTronStateMachine", response))
