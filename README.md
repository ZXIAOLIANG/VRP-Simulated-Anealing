# Simulated Anealing for Vehicle Routing Problem
Simulated Anealing is implemented to solve Vehicle Routing Problem in ECE457A. The VRP is defined in `A-n39-k6.vrp`

## Usage
`SA.py` outputs the initial solution, final solution found and its cost. It also outputs the specific configuration of SA.

Sample output:
```bash
current temp: 0.09261387130997902
final temp reached
initial solution: [0, 34, 36, 3, 11, 0, 31, 14, 27, 25, 37, 24, 12, 9, 30, 0, 33, 35, 19, 6, 26, 32, 7, 8, 0, 18, 0, 2, 21, 0, 10, 5, 20, 38, 16, 22, 1, 15, 4, 29, 13, 17, 28, 23]
alpha: 0.9
initial_temp: 10000
temp_itr: 1000
final_temp: 0.1
optimal cost: 1250.7618539978296
optimal solution: [0, 36, 17, 23, 21, 18, 22, 34, 27, 32, 20, 14, 35, 25, 33, 19, 4, 16, 10, 7, 8, 2, 31, 37, 38, 12, 3, 30, 13, 0, 29, 28, 9, 5, 0, 11, 1, 6, 0, 24, 0, 15, 0, 26]
```
