from behave import *
import requests

@given("I have flask app in {mode} mode")
def step_impl(context, mode):
    dryRun = True if mode == "dry run" else False
    url = "http://127.0.0.1:8080/set-dry-run"
    response = requests.post(url, json={"dryRun": dryRun})
    assert(response.ok)

@given("I send a GET request to url")
def step_impl(context):
    url = "http://127.0.0.1:8080/ssh/sandbox-iosxr-1.cisco.com/interfaces"
    context.response = requests.get(url)

@given("I send a POST request")
def step_impl(context):
    url = "http://127.0.0.1:8080/sandbox-iosxr-1.cisco.com/interfaces/Loopback66"
    context.body = {"name": "Loopback66", "description": "POST test"}
    context.response = requests.post(url, json=context.body)

@given("I send a DELETE request")
def step_impl(context):
    url = "http://127.0.0.1:8080/sandbox-iosxr-1.cisco.com/interfaces/Loopback66"
    context.interface = {"name": "Loopback66"}
    context.response = requests.delete(url)

@then("I should get a successful reponse code")
def step_impl(context):
    assert(context.response.ok)