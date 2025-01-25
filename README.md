# Papers Fetcher Project

This project fetches research papers from PubMed based on a search query and processes the results to filter papers by non-academic authors. The data is saved either to a CSV file or printed to the console, depending on the user's preference.

## Features

- Fetch research papers from PubMed based on a search query.
- Filter papers based on non-academic authors.
- Save results to a CSV file or print to the console.
- Supports debug mode to print intermediate steps.

## Prerequisites

Ensure you have the following:

1. **Python 3.x** installed.
2. **Virtual environment** for isolating dependencies (optional but recommended).

## Installation

1. Clone or download the repository:
    ```bash
    git clone <your-repository-url>
    cd papers_fetcher_project
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv .venv
    ```

3. Activate the virtual environment:
    - **For Linux/macOS**:
        ```bash
        source .venv/bin/activate
        ```
    - **For Windows**:
        ```bash
        .venv\Scripts\activate
        ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setting Up Your API Key

You need a PubMed API key to use this script. You can obtain it by signing up at [NCBI API Key](https://www.ncbi.nlm.nih.gov/account/).

Once you have your key, replace the placeholder `YOUR_API_KEY` in the `get_papers_list.py` file or in your environment variables.

## Running the Script

### Command-line Arguments

To use the script, run it with the following arguments:

```bash
python get_papers_list.py [query] [options]
# Papers Fetcher Project

This project fetches research papers from PubMed based on a search query and processes the results to filter papers by non-academic authors. The data is saved either to a CSV file or printed to the console, depending on the user's preference.

## Features

- Fetch research papers from PubMed based on a search query.
- Filter papers based on non-academic authors.
- Save results to a CSV file or print to the console.
- Supports debug mode to print intermediate steps.

## Prerequisites

Ensure you have the following:

1. **Python 3.x** installed.
2. **Virtual environment** for isolating dependencies (optional but recommended).

## Installation

1. Clone or download the repository:
    ```bash
    git clone <your-repository-url>
    cd papers_fetcher_project
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv .venv
    ```

3. Activate the virtual environment:
    - **For Linux/macOS**:
        ```bash
        source .venv/bin/activate
        ```
    - **For Windows**:
        ```bash
        .venv\Scripts\activate
        ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setting Up Your API Key

You need a PubMed API key to use this script. You can obtain it by signing up at [NCBI API Key](https://www.ncbi.nlm.nih.gov/account/).

Once you have your key, replace the placeholder `YOUR_API_KEY` in the `get_papers_list.py` file or in your environment variables.

## Running the Script
    ```bash
    python scripts/get_papers_list.py "generic research" -f results.csv -d
    python scripts/get_papers_list.py "cancer research" -f results.csv -d
    ```

### Command-line Arguments

To use the script, run it with the following arguments:

```bash
python get_papers_list.py [query] [options]
```