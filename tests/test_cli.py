import os

from gencli.cli import cli

PROJECT_DIR = "tests/test_project"


def test_init_write(runner, fs):
    os.makedirs(PROJECT_DIR)
    os.chdir(PROJECT_DIR)
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert result.output == "Initialized project: /tests/test_project/pyproject.toml\n"


def test_init_write_exception(runner, fs):
    os.makedirs(PROJECT_DIR)
    os.chdir(PROJECT_DIR)
    runner.invoke(cli, ["init"])
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 1
    assert (
        result.output
        == "Error: A pyproject.toml file already exists in the current directory.\n"
    )


def test_build_output(runner):
    result = runner.invoke(cli, ["build"])
    assert result.exit_code == 0
    assert result.output == "Build project.\n"


def test_validate_output(runner):
    result = runner.invoke(cli, ["validate"])
    assert result.exit_code == 0
    assert result.output == "Validate project.\n"


def test_test_output(runner):
    result = runner.invoke(cli, ["test"])
    assert result.exit_code == 0
    assert result.output == "Test project.\n"


def test_deploy_output(runner):
    result = runner.invoke(cli, ["deploy"])
    assert result.exit_code == 0
    assert result.output == "Deploy project.\n"
