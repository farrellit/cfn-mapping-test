from aws_cdk import (
    CfnMapping,
    CfnOutput,
    Fn,
    Stack,
    Token,
    aws_apigatewayv2_authorizers
)
from constructs import Construct

class CdkMappingTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        mapping = CfnMapping(self, "Mapping",
            mapping={
                "us-east-2": { "values": [ "value1", "value2" ] }
            },
        )

        authorizer = aws_apigatewayv2_authorizers.HttpJwtAuthorizer(
            "HttpJWTAuthorizer",
            "auther",
            authorizer_name="JWT-Authorizer",
            identity_source=["$request.header.Authorization"],
            #jwt_audience=["value1", "value2"], # synth works
            jwt_audience=Token.as_list(mapping.find_in_map(Fn.ref("AWS::Region"), "values")), # synth does not work
        )
        # fails: "Template format error: The Value field of every Outputs member must evaluate to a String and not a List."
        #CfnOutput(
        #    self,
        #    "values",
        #    value=mapping.find_in_map(Fn.ref("AWS::Region"), "values")
        #)
