from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyStatement
from constructs import Construct
import boto3, json 
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ses_actions as ses_actions,
    aws_ses as ses,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks, 
    aws_apigateway as apigw, 
    aws_s3 as s3, 
    aws_s3_deployment as s3_deploy
)


class PetCuddleOTronStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Stage 1: Setting up SES service & SNS topic
        email_sns_topic = sns.Topic(self, "PetCuddleOTronStack_SNS_Email")

        email_sns_topic.add_subscription(subscriptions.SmsSubscription("+15109962934"))


        ses.ReceiptRuleSet(self, "PetCuddleOTrongStack_SES_RuleSet",
                           rules=[ses.ReceiptRuleOptions(
                               recipients=["guptarohan323@gmail.com"],
                               actions=[
                                   ses_actions.AddHeader(
                                       name="X-Special-Header",
                                       value="AWS_PetCuddleOTronStack_Serverless_App"
                                   )
                               ]
                           ), ses.ReceiptRuleOptions(
                               recipients=["guptarohan323@gmail.com"],
                               actions=[
                                   ses_actions.Sns(
                                       topic=email_sns_topic
                                   )
                               ]
                           )
                           ]
                           )

        # Stage 2: email lambda
        email_lambda = _lambda.Function(self, "PetOCuddleTronEmailLambda",
                                        runtime=_lambda.Runtime.PYTHON_3_9,
                                        code=_lambda.Code.from_asset('./software/src'),
                                        handler="email_lambda.lambda_handler"
                                        )

        #### Stage 3: State Machine stuff #########
        data = None 
        with open("./infra/statemachine.json", "r") as f: 
            data = json.load(f)

        
        state_machine_role = Role(self, "StateMachineRole",
                    assumed_by=ServicePrincipal("states.amazonaws.com")
                    )

        state_machine_role.add_to_policy(PolicyStatement(
            resources=["*"],
            actions=["lambda:InvokeFunction", "sns:*",
                     "logs:CreateLogGroup", "logs:CreateLogStream", 
                     "logs:PutLogEvents", "logs:CreateLogDelivery","logs:GetLogDelivery",
                    "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries",
                    "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups" 
                  ]
        ))

        # State Machien configuration for Stage 3 was manually done in the console. 



        ### STAGE 4 - Implement the API Gateway, API and supporting lambda function ### 

        
        
        lambda_role = Role(self, "PetCuddleOTron_API_LambdaRole",
                           assumed_by=ServicePrincipal("lambda.amazonaws.com"))
        
        lambda_role.add_to_policy(PolicyStatement(
            resources=["*"], 
            actions=["states:ListStateMachine"]
        ))

        api_lambda =  _lambda.Function(self, "PetOCuddleTronAPILambda",
                                        runtime=_lambda.Runtime.PYTHON_3_9,
                                        code=_lambda.Code.from_asset('./software/src'),
                                        handler="api_lambda.lambda_handler", 
                                        role=lambda_role
                                    )
        
        api = apigw.LambdaRestApi(self, "PetOCuddleTron", handler=api_lambda, 
                                  default_cors_preflight_options=apigw.CorsOptions(
                                        allow_origins=apigw.Cors.ALL_ORIGINS,
                                        allow_methods=apigw.Cors.ALL_METHODS
                                    )
                                )

        api_endpoint = api.root.add_resource("petcuddleotron")
        api_endpoint.add_method("GET", apigw.LambdaIntegration(api_lambda))


        ### STAGE 5 - Deploy static website with S3 ### 
        web_files_folder = "./software/resources/webfiles"
        web_files_path = web_files_folder + "/index.html"
        web_bucket = s3.Bucket(self, "PetCuddleOTron-Static-UI-S3-Bucket", public_read_access=True, 
                    website_index_document=web_files_path, website_error_document=web_files_path
                )

        
        s3_deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3_deploy.Source.asset(web_files_folder)],
            destination_bucket=web_bucket,
            content_type="text/html",
            content_language="en",
            storage_class=s3_deploy.StorageClass.STANDARD_IA,
            server_side_encryption=s3_deploy.ServerSideEncryption.AES_256,
            cache_control=[
                s3_deploy.CacheControl.set_public(),
                s3_deploy.CacheControl.max_age(Duration.hours(1))
            ],
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL
        )
        








