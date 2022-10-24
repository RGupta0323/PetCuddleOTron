from constructs import Construct
import boto3
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ses_actions as ses_actions,
    aws_ses as ses,
    aws_sns_subscriptions as subscriptions
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



