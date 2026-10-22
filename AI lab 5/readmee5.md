# Lab 5 – Minimax & Alpha-Beta Pruning

Rasikh Ali – 42365

## What is this?
A small program that picks the best move in a two-player game.
- **MAX** (us) wants the biggest score.
- **MIN** (opponent) wants the smallest score.

It uses **Minimax**, and then **Alpha-Beta**, which gives the same answer but skips useless branches.

## Idea in simple words
- **Minimax:** start at the bottom of the tree. MAX levels take the max, MIN levels take the min, until you reach the top.
- **Alpha** = the best score MAX is sure to get so far.
- **Beta** = the best score MIN is sure to get so far.
- If **alpha ≥ beta**, the rest of that branch can't change the answer, so we skip it (prune).

## How to run
Needs Python 3 only (no extra libraries).

```
python lab5_minimax_alphabeta.py
```

To save the output to a file:

```
python lab5_minimax_alphabeta.py > output.txt
```

## What the program shows
1. **Hand trace** – the value at every level, from the leaves up to the root.
2. **Leaf counter** – how many leaves each algorithm looked at.
3. **Reordering** – the same tree in a different order: the answer stays the same, but pruning changes.
4. **Edge case** – padding the tree with a different number can change the answer.

## Results

| Tree | Root value | Minimax leaves | Alpha-Beta leaves |
|---|---|---|---|
| 5.1 `[3,5,2,9,0,7]` (+ two 0s) | 5 | 8 | 8 |
| 5.2 `[3,5,2,9,3,5,2,9]` | 5 | 8 | 6 |
| 5.1 best order | 5 | 8 | 5 |
| 5.1 worst order | 5 | 8 | 8 |
| 5.2 best order | 5 | 8 | 5 |
| 5.2 worst order | 5 | 8 | 8 |

- Best move = **LEFT** in the original trees. Reordered trees can show RIGHT because the branches were swapped, but the value is the same.
- Minimax and Alpha-Beta **always agree** on the value.
- Alpha-Beta **never checks more** leaves than Minimax.
- Good ordering (best child first) saves the most work. Bad ordering saves nothing.

## Edge case
Tree 5.1 has 6 leaves, so we add 2 fake leaves to make 8.
- Padding with 0 or -100 gives root = 5.
- Padding with 100 gives root = 7, which is **wrong**.

The fake leaves act like real moves. A better fix is a real tree where nodes can have any number of children.

## Files
- `lab5_minimax_alphabeta.py` – the code
- `output.txt` – saved output from running the code
- `README.md` – this file

## Credit
The Minimax and Alpha-Beta functions are adapted from the CAI601400 lab manual (sections 5.1 and 5.2).
