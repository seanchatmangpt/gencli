import logging
import logging.config
from datetime import datetime


# Function to setup logging configurations
def setup_logging():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{levelname}] {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "cli_activity.log",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "": {
                "handlers": ["file"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
    logging.config.dictConfig(logging_config)


# Function to log CLI activity
def log_cli_activity(activity: str, level: str = "info"):
    logger = logging.getLogger()
    log_level = getattr(logger, level, "info")
    log_level(f"[{datetime.utcnow().isoformat()}] - {activity}")


# Function to monitor CLI actions
def monitor_cli_actions(cli_action: str):
    log_cli_activity(f"CLI action executed: {cli_action}")


# Test the logging and monitoring system
def test_logging_and_monitoring_system():
    setup_logging()
    log_cli_activity("Logging system initialized", "info")
    monitor_cli_actions("create_task")
    monitor_cli_actions("delete_task")

    with open("cli_activity.log", "r") as f:
        logs = f.read()
        assert "Logging system initialized" in logs
        assert "CLI action executed: create_task" in logs
        assert "CLI action executed: delete_task" in logs


# Run the test
if __name__ == "__main__":
    test_logging_and_monitoring_system()
