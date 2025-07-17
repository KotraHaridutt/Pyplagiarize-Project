# PyPlagiarize: AST-Based Code Similarity Detector

PyPlagiarize is a static analysis tool designed to detect plagiarism in Python source code. Unlike traditional tools that compare text, PyPlagiarize parses code into Abstract Syntax Trees (ASTs) to compare the underlying program structure, making it robust against superficial changes like variable renaming, reformatting, and comment modification.

---

## Key Features ✨

* **Structural Comparison:** Analyzes the code's logic and architecture using ASTs, not just text.
* **Robust Detection:** Immune to common plagiarism-masking techniques such as changing variable names, adding whitespace, or modifying comments.
* **Detailed Reporting:** Pinpoints similarity at the function and class level, providing line numbers for easy reference.
* **Normalized Scoring:** Computes a normalized tree-edit distance to provide an intuitive similarity score from 0% to 100%.
* **Command-Line Utility:** Packaged as a clean and easy-to-use command-line tool.

---

## Installation ⚙️

Follow these steps to set up and run the tool on your local machine.

#### 1. Clone the Repository
First, clone the project from GitHub.
```bash
git clone https://github.com/KotraHaridutt/Vector-search-engine-LSH.git

## 2. Create and Activate a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies cleanly.

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install the Tool
With your virtual environment active, install the tool and its required dependencies using pip. This command reads the `pyproject.toml` file and handles the installation automatically.

```bash
pip install .
```

## Usage 🚀
The tool is run from the command line, comparing all functions and classes between two specified Python files.

### Command Structure
```bash
pyplagiarize [OPTIONS] <PATH_TO_FILE_1> <PATH_TO_FILE_2>
```

### Options
- `--threshold FLOAT`: Sets the similarity threshold (from 0.0 to 1.0) for reporting. Only code blocks with a score above this value will be shown. Default is `0.8`.

### Example

Suppose you have two files:

**student1.py**
```python
def calculate_sum(a, b):
    # Add two numbers
    result = a + b
    return result
```

**student2.py**
```python
# Computes the total of x and y
def get_total(x, y):
    return x + y
```

Run the tool to compare them:
```bash
pyplagiarize student1.py student2.py --threshold 0.9
```

**Expected Output:**
```
Comparing definitions in 'student1.py' and 'student2.py'...

[100.00%] High similarity found for Function:
 - 'calculate_sum' in student1.py (line 1)
 - 'get_total' in student2.py (line 2)
```

Author
KotraHaridutt
