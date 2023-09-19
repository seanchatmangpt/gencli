import importlib.util
import sys
import time
from queue import Queue
from threading import Lock, Thread

import pytest
from click.testing import CliRunner
from jinja2 import Template

# Global Lock for thread-safe operations
file_lock = Lock()

# Global Queue for transcript management
transcript_queue = Queue()

COMMANDS = [
    {
        "name": "create",
        "args": ["item", "value"],
        "options": [],
        "documentation": "Create a new item.",
    },
    {"name": "read", "args": ["item"], "options": [], "documentation": "Read an item."},
    {
        "name": "update",
        "args": ["item", "new_value"],
        "options": [],
        "documentation": "Update an item.",
    },
    {
        "name": "delete",
        "args": ["item"],
        "options": [],
        "documentation": "Delete an item.",
    },
]


# Function to perform OpenAI analysis (placeholder, to be replaced with real API call)
def openai_analysis(transcript: str) -> dict:
    return {"commands": COMMANDS}


cli_template = """
import click

@click.group()
def cli():
    pass

{% for command in commands %}
@click.command(name='{{ command.name }}')
{% for option in command.options %}
@click.option('--{{ option.name }}', type={{ option.type }}, 
required={{ option.required }},
help='{{ option.help }}')
{% endfor %}
def {{ command.name }}({{ command.args }}):
    \"\"\"{{ command.documentation }}\"\"\"
    click.echo('Command {{ command.name }} executed.')

cli.add_command({{ command.name }})
{% endfor %}

if __name__ == '__main__':
    cli()
"""


# Function to generate CLI spec based on API data
def generate_cli_spec(api_data: dict) -> str:
    template = Template(cli_template)
    return template.render(commands=api_data["commands"])


# Worker function to process each transcript from the queue
def worker(fs):
    while not transcript_queue.empty():
        transcript = transcript_queue.get()
        api_data = openai_analysis(transcript)
        cli_code = generate_cli_spec(api_data)
        file_name = f"/fake_dir/cli_{hash(transcript)}.py"
        with file_lock:
            fs.create_file(file_name, contents=cli_code)


# Test for high-load conditions
def test_high_load(fs):
    # Create fake directory
    fs.create_dir("/fake_dir")

    # Populate the transcript queue with 100 transcripts
    for i in range(100):
        transcript_queue.put(f"CLI request {i}")

    # Create 10 worker threads
    threads = [Thread(target=worker, args=(fs,)) for _ in range(10)]

    # Start the worker threads
    for thread in threads:
        thread.start()

    # Wait for all worker threads to finish
    for thread in threads:
        thread.join()

    # Verification: Check if all files are created
    for i in range(100):
        transcript = f"CLI request {i}"
        assert fs.exists(f"/fake_dir/cli_{hash(transcript)}.py")


temp_file_name = "temp_crud_cli.py"

# Import the generated CLI for testing
spec = importlib.util.spec_from_file_location("temp_cli", temp_file_name)
temp_cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = temp_cli
spec.loader.exec_module(temp_cli)

# Lock for thread-safe CLI execution
lock = Lock()


# Function to simulate CLI execution within a thread
def thread_execute_cli(command: str, execution_results: Queue):
    runner = CliRunner()
    with lock:
        result = runner.invoke(temp_cli.cli, command.split())
    # Simulating a delay to potentially introduce thread-related problems
    time.sleep(0.1)
    execution_results.put((result.exit_code, result.output))


# Test for high-concurrency CLI executions
@pytest.mark.parametrize(
    "command",
    [
        "create --item test1 --value value1",
        "read --item test2",
        "update --item test3 --new_value new_value3",
        "delete --item test4",
    ],
)
def test_high_concurrency_cli_executions(command):
    # Setting up a queue to collect execution results
    execution_results = Queue()

    # Repeat commands to simulate high concurrency
    commands_to_test = [command] * 25

    threads = []
    for command in commands_to_test:
        thread = Thread(target=thread_execute_cli, args=(command, execution_results))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete execution
    for thread in threads:
        thread.join()

    # Validate results
    while not execution_results.empty():
        exit_code, output = execution_results.get()
        assert exit_code == 0
        assert "Command " in output

    # Catching thread-related issues by checking the queue size
    assert execution_results.qsize() == 0
