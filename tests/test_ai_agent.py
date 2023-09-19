from threading import Thread

from gencli.utils import fake_openai_analysis


# Function to simulate CLI creation
def create_cli_from_spec(spec: dict, file_path: str) -> None:
    with open(file_path, "w") as f:
        f.write("Simulated CLI based on spec")


# Function to simulate CLI execution
def execute_cli(file_path: str) -> None:
    """In a real-world scenario, we would execute the CLI here"""


# Function to simulate an AI agent
def ai_agent(transcript: str, file_path: str) -> None:
    spec = fake_openai_analysis(transcript)
    create_cli_from_spec(spec, file_path)
    execute_cli(file_path)


def test_ai_agent_with_pyfakefs(fs):
    # Setup
    transcript = "We need a CLI for creating tasks."
    file_path = "/fake_dir/fake_cli.py"
    fs.create_dir("/fake_dir")

    # Action
    ai_agent(transcript, file_path)

    # Verification
    with open(file_path, "r") as f:
        content = f.read()
        assert content == "Simulated CLI based on spec"


# This simulates a situation where multiple agents need to create CLI files
def test_multiple_ai_agents_with_pyfakefs(fs):
    # Setup
    transcripts = [
        "We need a CLI for creating tasks.",
        "We need a CLI for deleting tasks.",
    ]
    fs.create_dir("/fake_dir")
    threads = []

    # Action
    for i, transcript in enumerate(transcripts):
        file_path = f"/fake_dir/fake_cli_{i}.py"
        thread = Thread(target=ai_agent, args=(transcript, file_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Verification
    for i, transcript in enumerate(transcripts):
        file_path = f"/fake_dir/fake_cli_{i}.py"
        assert fs.exists(file_path)
        with open(file_path, "r") as f:
            content = f.read()
            assert content == "Simulated CLI based on spec"
