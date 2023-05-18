#!/usr/bin/env python3

import aws_cdk as cdk

from infra.pet_cuddle_o_tron_stack import PetCuddleOTronStack


app = cdk.App()
PetCuddleOTronStack(app, "pet-cuddle-o-tron-cdk-stack")

app.synth()
