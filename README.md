# MinimiseError

`MinimiseError` is a Python class designed to minimize the error in a linear equation of the form `L = a*x + b*y` by finding integer values of `x` and `y` that yield the closest approximation.

## Description

This class aims to find the optimal integer solutions for `x` and `y` that minimize the residual error in the equation `L = a*x + b*y`. It's particularly useful in scenarios where you need to approximate a target value using two variables with specific coefficients, but require integer solutions.

## Features

- Calculates the valid range of integer `x` values based on the equation constraints
- Computes corresponding `y` values and rounds them to integers
- Finds the combination of `x` and `y` that minimizes the error `L - (a*x + b*y)`
- Option to display residual errors for all computed `x` values
- Provides a detailed output of the optimized solution

## Installation

To install the `MinimiseError` class, you can clone this repository from GitHub:

```bash
git clone https://github.com/LuMaul/OptRestOfLenAandBinL
cd OptRestOfLenAandBinL
```

There are no additional dependencies required beyond Python 3.x, so you can start using the class immediately after cloning the repository.

## Usage

Here's a basic example of how to use the `MinimiseError` class:

```python
from minimise_error import MinimiseError

if __name__ == '__main__':
    myOpt = MinimiseError(L=20.5, a=0.80, b=1.25, show_residuals=False)
```

This will minimize the error for the equation `20.5 = 0.8*x + 1.25*y` and print the optimized integer values of `x` and `y` with the smallest residual error.

## Parameters

- `L` (float): The target value for the equation `L = a*x + b*y`
- `a` (float): Coefficient for `x` in the equation
- `b` (float): Coefficient for `y` in the equation
- `show_residuals` (bool, optional): Whether to print the residuals (default is False)

## Output

The class will print the optimized solution, showing:
- The input parameters (`L`, `a`, `b`)
- The calculated integer values for `x` and `y`
- The resulting approximation of `L`
- The minimal residual error

## Methods

The class includes several internal methods for calculations and result presentation. The main method `_solve()` orchestrates the optimization process.

## Requirements

- Python 3.x
