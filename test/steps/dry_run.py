from behave import *
import multiprocessing, requests, time
import api_endpoints

@given(u"I have flask app in dry run mode")
def step_impl(context):
    context.p = multiprocessing.Process(target=api_endpoints.main, kwargs={"port":8080, "host":"0.0.0.0", "dry":True})
    context.p.daemon = True
    context.p.start()
    time.sleep(1)
    assert(True)

@given(u"I send a get request to url")
def step_impl(context):
    url = "http://127.0.0.1:8080/ssh/sandbox-iosxr-1.cisco.com/interfaces"
    context.get_response = requests.get(url)

@then(u"I should get a successful reponse code")
def step_impl(context):
    assert(context.get_response.ok)

@then(u"The body should contain the CLI commands")
def step_impl(context):
    print(context.get_response.text)
    assert(context.get_response.text == '["term len 0","show ip int br"]')

@given(u"I stop the server")
def step_impl(context):
    print("stopping server")
    context.p.terminate()
