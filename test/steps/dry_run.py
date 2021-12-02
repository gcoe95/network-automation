from behave import *
import multiprocessing, time, os
from jinja2 import Environment, FileSystemLoader, StrictUndefined

@then("The body should contain the CLI commands")
def step_impl(context):
    assert(context.response.json() == ["term len 0","show ip int br"])

@then("The body should contain the create netconf")
def step_impl(context):
    netconf = getData("loopback_create.xml", context.body)
    assert(context.response.text == netconf)

@then("The body should contain the delete netconf")
def step_impl(context):
    netconf = getData("loopback_delete.xml", context.interface)
    assert(context.response.text == netconf)

# Returns the text from a template file
def getData(templateName, params):
    path = os.path.realpath(__file__)  
    path = os.path.dirname(os.path.abspath(path)).replace("test/steps", "src")
    env = Environment(
        autoescape=False,
        loader=FileSystemLoader(f"{path}/templates/"),
        trim_blocks=False,
        undefined=StrictUndefined
    )
    return env.get_template(templateName).render(params)
