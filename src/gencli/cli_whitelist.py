import os

import openai
from fgn.completion.complete import create
from loguru import logger

openai.api_key = os.getenv("OPENAI_API_KEY")


def choose(prompt: str, choices: list) -> str:
    response = create(
        prompt,
        stop=["\n", " "],
        max_tokens=10,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    try:
        index = int(response, 16)
    except ValueError:
        raise ValueError(f"Response is not a valid hex code: {response}")

    consistent_index = index % len(choices)
    choice = choices[consistent_index]

    return choice


def whitelisted_command_selector(prompt, cli_commands):
    """Select a command from a whitelist of commands."""
    test_prompt = f"Choices: {cli_commands}\n" f"{prompt}\nIndex of choice base-16 0x"

    selected_command = choose(test_prompt, cli_commands)
    logger.info(f"Selected Command: {selected_command}")
    return selected_command


def is_correct_command(prompt, selected_command):
    """Check if the selected command is correct."""
    prompt = f"{prompt}\nWhat is the correct cli command?\nThe correct command is $ "
    response = create(
        prompt,
        max_tokens=5,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    logger.info(f"Response: {response}")
    return selected_command == response.split(" ")[0]


def main():
    cli_commands = [
        "ls",
        "pwd",
        "cd",
        "mkdir",
        "rmdir",
        "cp",
        "mv",
        "rm",
        "touch",
        "cat",
        "docker",
        "kubectl",
    ]
    prompt = "How do I create a docker container?"
    cmd = whitelisted_command_selector(prompt, cli_commands)
    check = is_correct_command(prompt, cmd)
    logger.info(f"Check: {check}")


if __name__ == "__main__":
    main()
