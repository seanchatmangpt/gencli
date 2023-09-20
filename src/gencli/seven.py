from typing import List

import openai
from faker import Faker
from loguru import logger

# Initialize Faker
fake = Faker()


def generate_seven_faker_sentences() -> List[str]:
    """
    Generate a list of 7 Faker sentences.

    Returns:
    - List[str]: A list containing 7 Faker-generated sentences.
    """
    sentences = [fake.sentence() for _ in range(7)]
    return sentences


class SevenFunctionAgent:
    """
    An agent that embodies the Seven Function Theory.
    """

    def __init__(self):
        self.perception_choices = generate_seven_faker_sentences()
        self.analysis_choices = generate_seven_faker_sentences()
        self.planning_choices = generate_seven_faker_sentences()
        self.action_choices = generate_seven_faker_sentences()
        self.learning_choices = generate_seven_faker_sentences()
        self.reporting_choices = generate_seven_faker_sentences()

    def fetch_openai_response(self, prompt: str, choices: List[str]) -> str:
        """
        Fetch response using OpenAI's API and select a choice from the list.

        Parameters:
        - prompt (str): The prompt to be used for generating a consistent index
        - choices (List[str]): The list of choices to choose from

        Returns:
        - str: The selected choice
        """
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct-0914",
            prompt=prompt,
            temperature=0,
            max_tokens=10,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[" ", "\n"],
        )
        index = int(
            response.choices[0].text.strip(), 16
        )  # Assume the response is a hexadecimal index
        consistent_index = index % len(choices)
        selected_choice = choices[consistent_index]
        return selected_choice


# Initialize the agent
agent = SevenFunctionAgent()

# Test the agent
prompt_for_perception = (
    "Perception choices are available. Select one based on the Seven Function Theory."
)
selected_perception_choice = agent.fetch_openai_response(
    prompt_for_perception, agent.perception_choices
)
logger.info(f"Selected perception choice: {selected_perception_choice}")
