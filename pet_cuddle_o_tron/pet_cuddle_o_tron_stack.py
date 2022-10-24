from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ses_actions as ses_actions,
    aws_ses as ses,
    aws_sns_subscriptions as subs,
)


class PetCuddleOTronStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # STage 1: Setting up SES service
        email_sns_topic = sns.Topic(self, "PetCuddleOTronStack_SNS_Email")


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


