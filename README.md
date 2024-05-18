# ScraperProject2024

## Overview

ScraperProject2024 is a modular and scalable web scraping framework designed to simplify the development of web scrapers for various websites. It includes base classes for HTTP requests and Selenium-based web scraping, as well as a finite state machine (FSM) to manage the scraping process.

## Features

- **BaseRequest**: For making HTTP requests.
- **BaseDriver**: For controlling web browsers using Selenium.
- **BaseFSM**: For managing the scraping process using a finite state machine.
- **ZeroMQ Integration**: For inter-process communication (optional).

## Project Structure

```
.
├── core
│   ├── baseDriver.py
│   ├── baseFSM.py
│   ├── baseRequest.py
│   ├── __init__.py
│   └── utils.py
├── data
│   └── logs
├── docs
│   └── core
├── geckodriver
├── __pycache__
├── requirements.txt
├── site
├── tests
└── README.md
```

## Setup

1. **Clone the repository**:


2. **Create and activate a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Generate documentation**:
   ```
   PYTHONPATH=$(pwd) pdoc --html ./core --output-dir ./docs --force
   ```

2. **Run tests**:
   ```
   pytest
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
