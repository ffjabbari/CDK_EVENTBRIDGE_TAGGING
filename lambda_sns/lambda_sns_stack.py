from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subs,
    aws_iam as iam
)
from constructs import Construct


class LambdaSnsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a Lambda function
        my_lambda = _lambda.Function(
            self, "MyLambda",
            function_name="MyLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",  # You'll need to provide your own Lambda code
            code=_lambda.Code.from_asset("lambda_code"),  # Create a 'lambda' directory with your code
        )

        # Create an SNS Topic
        sns_topic = sns.Topic(self, "MySNSTopic", topic_name="MySNSTopic")

        # Add an email subscription to the SNS Topic
        sns_topic.add_subscription(sns_subs.EmailSubscription("backamit20@gmail.com"))

        # Create an Event Rule to trigger Lambda on EC2 start and stop events
        event_rule = events.Rule(
            self, "EC2StartStopEventRule",rule_name="MyRule",
            event_pattern={
                "source": ["aws.ec2"],
                "detail_type": ["EC2 Instance State-change Notification"]
            }
        )

        # Grant permissions for Lambda to be triggered by the Event Rule
        my_lambda.add_permission(
            "InvokePermission",
            principal=iam.ServicePrincipal("events.amazonaws.com"),
            source_arn=event_rule.rule_arn
        )

        # Add the Lambda as a target for the Event Rule
        event_rule.add_target(targets.LambdaFunction(my_lambda))

