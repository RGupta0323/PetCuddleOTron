import pytest 
from software.src.api_lambda import get_sm_arn

def test_get_sm_arn(): 
    assert get_sm_arn() != None 