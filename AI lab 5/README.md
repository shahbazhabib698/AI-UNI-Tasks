# AI Lab 3 - Uninformed Search

## What this project does

This project solves the three tasks in Lab 3:

1. Runs BFS and DFS on the original graph from A to G and prints the visit order and path.
2. Runs Depth-Limited Search (DLS) at limits 1, 2, 3 and 4, then tests Iterative Deepening DFS (IDDFS).
3. Adds costs to the graph and compares BFS with Uniform Cost Search (UCS).

## Files

- `lab3_bfs_dfs.py` - BFS, DFS, paths, visit order and a simple trace.
- `lab3_depth_search.py` - DLS and IDDFS with FOUND, CUTOFF and FAILURE statuses.
- `lab3_ucs.py` - weighted graph, BFS comparison, UCS and independent path-cost check.

## How to run

You need Python 3. Open a terminal in this folder and run:

```bash
python lab3_bfs_dfs.py
python lab3_depth_search.py
python lab3_ucs.py
```

On some computers, use `python3` instead of `python`.

## Main ideas in simple words

- **BFS:** checks nearby nodes first. It finds a path with the fewest edges when each edge has equal cost.
- **DFS:** follows one branch deeper before trying another branch.
- **DLS:** DFS with a maximum depth.
- **IDDFS:** runs DLS repeatedly with a bigger depth limit each time.
- **UCS:** expands the available path with the lowest total cost so far.

## Graph and assumptions

The original graph uses A as the start and G as the goal. Neighbour order follows the lab manual. The weighted version keeps the original corridors and adds `C -> G`. The weights are example nonnegative travel-cost units chosen for the experiment: `A-B=1`, `A-C=6`, `B-D=2`, `B-E=1`, `C-F=2`, `C-G=6`, and `E-G=1`.

The weighted example demonstrates that BFS can choose `A -> C -> G` (2 edges, cost 12), while UCS chooses `A -> B -> E -> G` (3 edges, cost 3). BFS does not consider edge costs.

## Expected key results

- BFS original path: `A -> B -> E -> G`
- DFS original path: `A -> B -> E -> G`
- BFS original visit order: `A, B, C, D, E, F, G`
- DFS original visit order: `A, B, D, E, G`
- DLS limits 1 and 2 do not reach G; limits 3 and 4 can reach G.
- Weighted BFS chooses a two-edge route; UCS finds the minimum-cost route.

Exact trace lines are printed by the programs. Save your own terminal output for submission.

## Note

This is a classroom graph simulation, not a real rescue robot. Run the code and check its actual output before submitting. Add your own explanation and any required report material to `Lab3_Report.docx`.
