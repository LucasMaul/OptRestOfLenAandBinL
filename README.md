# Linfit

`Linfit` is a Python class designed to minimize the error $E_i$ in a discrete linear equation of the form $L = a * x_i + b * y_i + E_i$ by finding **integer** values of $x_i$ and $y_i$ that yield the closest approximation to $L$. $L$, $a$ and $b$ are given constant float values. The programm is designed to take almost no memory when calculating and there is no need of extra packages outside of standard python. First, it dramatically reduces the solution space for finding close discrete solution values for $x_i$ and $y_i$. Afterwards it walks through the found solution space and undercuts every next result, till no smaller error exists.

## Example Output

When you run the optimizer with the parameters shown in the usage example, you'll get output similar to this:

```
==================
optimized solution
==================
L = 1061105.570
a = 1.250
b = 0.800
=====================================================
7 * [1.250] + 1326371 * [0.800] + 0.020 = 1061105.570
=====================================================
> target len without error: 1061105.550
> got minimum out of 848885 residuals
> optimization took 0.27686095237731934 sec
```

This output shows:
- The input parameters (`L`, `a`, `b`)
- The optimized integer values for `x_i` (7) and `y_i` (1326371)
- The resulting equation to match the target `L` value for **integer** `x_i` and `y_i`
- The minimal residual error (0.020 in this case)
- The number of residuals checked to find this optimal solution
- The time it took to find the smallest residual

The discrete solution for `x_i` and `y_i` is beeing returned from `your_instance.solve(L=yourFloat)` as tuple

## Installation

To install the `Linfit` class, you can clone this repository from GitHub:

```bash
git clone https://github.com/LuMaul/OptRestOfLenAandBinL
cd OptRestOfLenAandBinL
```

There are no additional dependencies required beyond Python 3.x, so you can start using the class immediately after cloning the repository.

## Usage

Here's a basic example of how to use the `Linfit` class:

```python
from optimizer import Linfit

myFit = Linfit(a=0.80, b=1.25)
myFit.solve(L=20.5)
```

This will minimize the error for the equation `20.5 = 0.8*x_i + 1.25*y_i + e_i` and print the optimized integer values of `x_i` and `y_i` with the smallest residual error.


## Methods

The class includes several internal methods for calculations and result presentation. The main method `solve()` orchestrates the optimization process.

## Requirements

- Python 3.x
