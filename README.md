
# Python Logging Utility

A Python module to simplify logging setup and provide a decorator for easy function execution logging.

## Key Features

*   **Easy Initialization**: Quickly set up console and file logging.
*   **Automatic Log File Naming**: Default unique log names (`./logs/script_timestamp.log`).
*   **Safe File Handling**: Creates log directories; avoids overwriting existing log files by using new names and issues a `LogSettingWarning`.
*   **`@log_execution` Decorator**: Logs function calls, arguments, and intelligently finds a logger instance (passed as kwarg, `self.logger`, or falls back to root logger).
*   **Custom Warning**: `LogSettingWarning` for logging setup issues.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/ivsoan/logexe.git
    ```
2.  Navigate to the directory containing `setup.py`.
    ```bash
    cd ./logexecution
    ```
3.  Install:
    ```bash
    pip install .
    ```

## Quick Start

### 1. Initialize Logger

```python
from logexecution import logging_init

logger = logging_init()
logger.info("Logger is ready!")
```

### 2. Log Function Execution

```python
from logexecution import log_execution, logging_init

# Initialize a logger first
my_logger = logging_init()

@log_execution() # Uses INFO level by default
def my_function(x, y):
    my_logger.debug(f"Inside my_function with {x}, {y}")
    return x + y

# Decorator uses root logger (and warns) if no logger is found
my_function(10, 5)

# For class methods, ensure self.logger exists or pass logger as a kwarg
class MyClass:
    def __init__(self, logger_instance):
        self.logger = logger_instance # @log_execution will find this

    @log_execution(level=logging.DEBUG)
    def process(self, data):
        self.logger.info(f"Processing: {data}")
        return True

# To ensure @log_execution uses your logger for standalone functions:
@log_execution()
def another_function(a, b, logger=None): # Decorator checks 'logger' kwarg
    if logger:
        logger.debug("Another function called")
    return a * b

# Call it with the logger
another_function(3, 4, logger=my_logger)

# Using it with a class instance
instance = MyClass(logger_instance=my_logger)
instance.process("some_data")
```
The `@log_execution` decorator logs a message like `"Calling function my_function with args: (10, 5) kwargs: {}"`.
It tries to find a logger in this order:
1.  `logger` keyword argument passed to the decorated function.
2.  `args[0].logger` (e.g., `self.logger` in a method).
3.  Root logger.
