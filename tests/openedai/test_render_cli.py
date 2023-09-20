# The issue might be in the lines involving the Jinja2 loops or conditionals.
# Let's correct the template syntax and rewrite the test.

import importlib.util
import sys

import pytest
import yaml
from click.testing import CliRunner
from jinja2 import Template

cli_yaml = """
# CLI YAML Configuration for OpenAI Chat Client Using Arguments and Options
commands:
  - name: init
    role: user
    description: "Initialize a new chat session."
    arguments:
      - name: session
        type: string
        required: true
        description: "Unique identifier for chat session."
        validation:
          regex: "^[a-zA-Z0-9]+$"
    options:
      - long: verbose
        short: v
        type: boolean
        flag: true
        description: "Enable verbose output."

  - name: send
    role: user
    description: "Send a message to the chat."
    arguments:
      - name: message
        type: string
        required: true
        description: "The message content."
        validation:
          regex: "^[a-zA-Z0-9 .,!?'\\"-]+$"
    options:
      - long: timestamp
        short: t
        type: boolean
        required: false
        flag: true
        description: "Add a timestamp to the message."

  - name: history
    role: user
    description: "Retrieve the chat history."
    arguments:
      - name: session
        type: string
        required: true
        description: "Session identifier."
        validation:
          regex: "^[a-zA-Z0-9]+$"
    options:
      - long: limit
        short: l
        type: integer
        required: false
        description: "Limit the number of messages to retrieve."

  - name: close
    role: user
    description: "Close the chat session."
    arguments:
      - name: session
        type: string
        required: true
        description: "Session identifier to close."
        validation:
          regex: "^[a-zA-Z0-9]+$"
    options:
      - long: force
        short: f
        type: boolean
        required: false
        description: "Forcefully close the session without prompt."

  - name: admin
    role: admin
    description: "Admin actions."
    arguments:
      - name: action
        type: string
        required: true
        description: "Admin action (e.g., delete)."
        validation:
          regex: "^[a-zA-Z]+$"
    options:
      - long: id
        short: i
        type: integer
        required: false
        description: "ID for admin action."

  - name: search
    role: user
    description: "Perform a vector search."
    arguments:
      - name: query
        type: string
        required: true
        description: "Search query."
        validation:
          regex: "^[a-zA-Z0-9 .,!?'\\"-]+$"
    options:
      - long: radius
        short: r
        type: float
        required: false
        description: "Search radius for the vector search."
"""

yaml_data = yaml.load(cli_yaml, Loader=yaml.FullLoader)

# Mapping YAML types to Python types
type_mapping = {"string": "str", "integer": "int", "boolean": "bool", "float": "float"}

for command in yaml_data["commands"]:
    for argument in command["arguments"]:
        argument["type"] = type_mapping.get(argument["type"], "str")
    for option in command["options"]:
        option["type"] = type_mapping.get(option["type"], "str")

# Fix the Jinja2 template to avoid syntax error
cli_template = """
import click

@click.group()
def cli():
    pass

{% for command in commands %}
@click.command(name='{{ command.name }}')
{% for option in command.options %}
@click.option('--{{ option.long }}', '-{{ option.short }}',
type={{ option.type }}, required={{ option.required  | default(False) }},
help='{{ option.description }}',
is_flag={{ option.flag | default(False) }})
{% endfor %}
{% for argument in command.arguments %}
@click.argument('{{ argument.name }}', type={{ argument.type }})
{% endfor %}
def {{command.name}}({{command.arguments|map(attribute='name')|join(', ')}}, **kwargs):
    \"\"\"{{ command.description }}\"\"\"
    click.echo('Command {{ command.name }} executed')

cli.add_command({{ command.name }})
{% endfor %}
"""

# Render the template
template = Template(cli_template)
rendered_cli_code = template.render(commands=yaml_data["commands"])

# Write to a temporary Python file for testing
temp_file_name = "temp_openai_cli.py"
with open(temp_file_name, "w") as f:
    f.write(rendered_cli_code)

# Dynamically import the temporary CLI module for testing
spec = importlib.util.spec_from_file_location("temp_cli", temp_file_name)
temp_cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = temp_cli
spec.loader.exec_module(temp_cli)


# Your pytest test
@pytest.mark.parametrize(
    "command, expected_output",
    [
        ("init,-v,test_session", "Command init executed\n"),
        ("send,Hello World", "Command send executed\n"),
        ("history,test_session", "Command history executed\n"),
        ("close,test_session", "Command close executed\n"),
    ],
)
def test_cli_commands(command, expected_output):
    runner = CliRunner()
    result = runner.invoke(temp_cli.cli, command.split(","))
    assert result.exit_code == 0
    assert result.output == expected_output
