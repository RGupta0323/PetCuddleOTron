import pytest 
from software.src.api_lambda import get_sm_arn

def test_get_sm_arn(): 
    result = get_sm_arn() 
    assert type(result) == str 
    assert "arn" in result and "aws" in result and "states" in result and "us-east-1" in result 