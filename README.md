# LinearEquationIntegerOptimizer

`LinearEquationIntegerOptimizer` is a Python class designed to minimize the error in a linear equation of the form `L = a*x + b*y` by finding integer values of `x` and `y` that yield the closest approximation.

## Example Output

When you run the optimizer with the parameters shown in the usage example, you'll get output similar to this:

```
==================
optimized solution
==================
l = 20.500
a = 0.800
b = 1.250
======================================
10 * [0.800] + 10.0 * [1.250] = 20.500
> minmal rest: 0.000
> got mininum out of 25 residuals
```

This output shows:
- The input parameters (`l`, `a`, `b`)
- The optimized integer values for `x` (10) and `y` (10)
- The resulting equation that perfectly matches the target `L` value
- The minimal residual error (0.000 in this case)
- The number of residuals checked to find this optimal solution


## Features

- Calculates the valid range of integer `x` values based on the equation constraints
- Computes corresponding `y` values and rounds them to integers
- Finds the combination of `x` and `y` that minimizes the error `L - (a*x + b*y)`
- Option to display residual errors for all computed `x` values
- Provides a detailed output of the optimized solution

## Installation

To install the `LinearEquationIntegerOptimizer` class, you can clone this repository from GitHub:

```bash
git clone https://github.com/LuMaul/OptRestOfLenAandBinL
cd OptRestOfLenAandBinL
```

There are no additional dependencies required beyond Python 3.x, so you can start using the class immediately after cloning the repository.

## Usage

Here's a basic example of how to use the `LinearEquationIntegerOptimizer` class:

```python
from main import LinearEquationIntegerOptimizer

if __name__ == '__main__':
    myOpt = LinearEquationIntegerOptimizer(L=20.5, a=0.80, b=1.25, show_residuals=False)
```

This will minimize the error for the equation `20.5 = 0.8*x + 1.25*y` and print the optimized integer values of `x` and `y` with the smallest residual error.


## Methods

The class includes several internal methods for calculations and result presentation. The main method `_solve()` orchestrates the optimization process.

## Requirements

- Python 3.x
