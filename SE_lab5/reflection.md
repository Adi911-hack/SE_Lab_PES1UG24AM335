# Lab 5: Static Code Analysis — Reflection

**SRN:** PES1UG24AM335

### 1. How did static analysis help identify issues in the program?

Static analysis helped me identify problems in the Python code without having to execute every function manually. Pylint detected code quality issues such as improper naming conventions, missing docstrings, and mutable default arguments. Bandit identified security risks, while Flake8 highlighted formatting issues.

### 2. Which issue was the most important, and why?

The shell command injection vulnerability detected by Bandit was one of the most important issues because it could allow unsafe commands to be executed through an event name. I replaced the shell-based operation with a safer file-reading approach.

I also fixed the mutable default argument because it caused different events to share guest lists, resulting in incorrect seat counts.

### 3. What improvements did you observe after fixing the code?

The Pylint score increased from 4.64/10 to 10.00/10. Bandit findings decreased from four to zero, and Flake8 violations decreased from four to zero.

The program also started producing correct guest lists and seat counts. Both events now maintain independent guest lists, and the data can be saved and restored using JSON.

### 4. What did you learn from this lab?

I learned that a program can execute without crashing and still contain logical bugs, security risks, and code quality problems.

I also learned how to use Pylint, Bandit, and Flake8 to identify different types of issues, apply corrections, and verify the results. Making separate Git commits helped me track the changes made for each analysis tool.