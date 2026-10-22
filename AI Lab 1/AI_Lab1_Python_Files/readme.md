# AI Lab 1 — Easy Explanation

## What are we doing?
We are making a simple scholarship checker in Python. It tells us whether an application should be checked by a person.

## File 1: `lab1_compare.py`
This file compares two methods:
- **Rule-based:** follows fixed rules, such as documents must be complete and score must be 70 or more.
- **Probability-based:** says `Review` when the probability is 0.70 or more.

The program prints both results and shows whether they disagree.

## File 2: `lab1_rules.py`
This file checks four conditions:
1. Documents are complete.
2. Score is at least 70.
3. Student is eligible.
4. Application is submitted before the deadline.

If all conditions pass, it prints `Review`. Otherwise, it prints `Hold`.

## The four tests
- **Pass:** all conditions are true → `Review`.
- **Eligibility failure:** eligibility is false → `Hold`.
- **Deadline failure:** deadline condition is false → `Hold`.
- **Boundary:** score is exactly 70 and the other conditions pass → `Review`.

## Important
The score limit and extra conditions are made-up examples for this lab. `Review` means a person should check the application; it does not mean the student gets a scholarship. The probability values are examples too; the code does not train an AI model.

## How to run
1. Open the files in VS Code.
2. Run each Python file.
3. Check the output.
4. Add the code results and explanation to your lab report.
