# PerfTracker

PerfTracker is a Python performance tracking package designed to assist developers in monitoring and tracking the execution time of their functions. It provides a straightforward and efficient way to measure function performance, enabling you to optimize your code effectively.

![](https://img.shields.io/pypi/v/perftracker)
![](https://img.shields.io/pypi/dm/perftracker)

## Features

- **Ease of Use**: Simply add a decorator to your functions.
- **Flexibility**: Can be used without decorator for manual tracking.
- **Detailed Statistics**: PerfTracker provides comprehensive statistics about your function's performance. It allows you to get the execution times and calculate the average calls per minute over a certain period. This information can be crucial in identifying bottlenecks in your code and optimizing it.

## Disclaimer

This package uses a global variable `_perf` for the performance model. It uses a key schema
of `module_name.function_name` to avoid interference when multiple packages use it for tracking.

## Installation

You can install PerfTracker using pip, the Python package installer. Run the following command in your terminal:

```bash
pip install perftracker
```

## Usage

Using PerfTracker is straightforward. Here are some examples:

### Basic Usage

```python
from perftracker import perf, get_stats

@perf(max_entries=100)
def my_function():
    # Your code here...

# Get performance statistics
stats = get_stats()
```

### Retrieving Execution Time Records

```python
from perftracker import perf, get_stats

@perf(max_entries=100)
def my_function():
    # Your code here...

# Get performance statistics
stats = get_stats()

# Retrieve execution time records
records = stats.get(my_function)
```

### Calculating Calls Per Minute

```python
from perftracker import perf, get_stats
from datetime import timedelta

@perf(max_entries=100)
def my_function():
    # Your code here...

# Get performance statistics
stats = get_stats()

# Calculate calls per minute for the last hour
cpm = stats.cpm(my_function, timedelta(hours=1))
```

### Tracking things manually

```python
from perftracker import get_stats
from time import perf_counter

def some_function():
    stats = get_stats()
    start_time = perf_counter()

    ...  # Some code that takes time...

    end_time = perf_counter()
    delta = end_time - start_time

    # Add time manually, the 'add' method can take strings too
    stats.add("my_custom_function_key", delta)
```

### Methods

PerfTracker provides several methods to track and retrieve function performance data:

- `perf(max_entries=None)`: A decorator to measure and record the execution time of a function. If `max_entries` is set, it will limit the number of records kept for the function to this value.
- `get_stats()`: Returns the current Performance instance, which contains all recorded performance data.
- `Performance.add(function, exe_time, max_entries=None)`: Adds an execution time record for a function. You can use this method to manually add execution time records.
- `Performance.get(function)`: Returns the execution time records for a function. This can be useful if you want to analyze the performance data further.
- `Performance.cpm(function, time_delta)`: Calculates the average calls per minute (CPM) of a function over a certain period. This can give you an idea of how frequently a function is called.
- `Performance.avg_time(function, time_delta)`: Calculate the average time a function takes to execute over a certain period. This can help you identify slow functions that may need optimization.

## Contributing

We welcome contributions to PerfTracker. If you have a feature request, bug report, or want to improve the code, please feel free to submit a Pull Request.

## License

PerfTracker is licensed under the terms of the MIT license. This means you are free to use, modify, and distribute the code, as long as you include the original copyright and license notice.
