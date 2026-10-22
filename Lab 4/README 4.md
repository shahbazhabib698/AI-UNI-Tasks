# Lab 4 – A* Search (Heuristics)

Rasikh Ali – 42365

## What is this?
A small program that finds the cheapest route from building **S** to building **G** on a campus map.
It uses **A\*** search and compares it with **UCS** (normal search with no guessing).

## Idea in one line
A\* picks the next node with the smallest **f = g + h**
- **g** = cost so far (real)
- **h** = guess of cost left
- **f** = total estimated cost

## How to run
Needs Python 3 only (no extra libraries).

```
python lab4_astar_audit.py
```

To save the output to a file:

```
python lab4_astar_audit.py > output.txt
```

## What the program shows
1. **A\* step by step** – g, h, f for each node and what is left in the queue.
2. **Heuristic check** – h never overestimates (admissible) and passes every edge check (consistent).
3. **A\* vs UCS** – same path, but A\* opens fewer nodes.
4. **Bad heuristic test** – h(C) changed from 2 to 10 and A\* gives a wrong (more expensive) path.

## Results

| Run | Path | Cost | Nodes expanded |
|---|---|---|---|
| A\* (given h) | S → A → C → G | 6 | 3 |
| UCS (h = 0) | S → A → C → G | 6 | 4 |
| A\* with h(C) = 10 | S → B → G | 9 | 3 |

- A\* found the best path and checked one node less than UCS.
- When h(C) was too big, C looked far away, so A\* went through B and returned cost 9 instead of 6.
- **Lesson:** if h overestimates, A\* can give a wrong answer. Even if one run looks fine, that does not prove the heuristic is safe.

## Counting rule
- A node is "expanded" only when we look at its neighbours.
- The goal is not counted.
- Old (stale) queue entries are skipped.

## Files
- `lab4_astar_audit.py` – the code
- `output.txt` – saved output from running the code
- `README.md` – this file

## Credit
A\* code is adapted from the guided code in the CAI601400 lab manual (section 4.2).
