import asyncio

import pytest
from click.testing import CliRunner
from faker import Faker

from gencli import temp_crud_cli

# Initialize Faker
fake = Faker()


# Asynchronous function for worker execution
async def worker_cli_executor(agent_name, command, log_queue):
    runner = CliRunner()
    item = fake.unique.first_name()
    value = fake.unique.email()
    new_value = fake.unique.email()

    command_args = {
        "create": ["--item", item, "--value", value],
        "read": ["--item", item],
        "update": ["--item", item, "--new_value", new_value],
        "delete": ["--item", item],
    }

    result = runner.invoke(temp_crud_cli.cli, [command] + command_args[command])

    log_entry = {
        "agent_name": agent_name,
        "command": command,
        "args": command_args[command],
        "result": "success" if result.exit_code == 0 else "failed",
        "echo": result.stdout if result.exit_code == 0 else result.stderr,
        "timestamp": asyncio.get_running_loop().time(),
    }
    print(log_entry)
    await log_queue.put(log_entry)


# Asynchronous function for CLI verification
async def worker_cli_verifier(log_queue, expected_commands):
    executed_commands = set()
    while len(executed_commands) < len(expected_commands):
        log_entry = await log_queue.get()
        if log_entry["result"] == "success":
            executed_commands.add(log_entry["command"])
    return executed_commands


@pytest.mark.asyncio
async def test_agent_simulation():
    command_queues = ["create", "read", "update", "delete"]
    log_queue = asyncio.Queue()
    agent_names = [fake.unique.first_name() for _ in range(5)]

    # Create list to hold all worker tasks
    worker_tasks = []

    # Initialize executor tasks
    for agent_name, command in zip(agent_names[:-1], command_queues):
        task = asyncio.create_task(worker_cli_executor(agent_name, command, log_queue))
        worker_tasks.append(task)

    # Initialize verifier task
    verifier_task = asyncio.create_task(worker_cli_verifier(log_queue, command_queues))

    # Wait for all tasks to complete
    await asyncio.gather(*worker_tasks)
    executed_commands = await verifier_task

    # Assert all CRUD operations are executed
    assert executed_commands == set(
        command_queues
    ), f"Expected all CRUD operations to be executed. Got: {executed_commands}"
