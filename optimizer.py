from typing import Generator
from time import time

class Linfit:
    """
    A class designed to minimize the residual error in a linear equation of the form `L = a*x + b*y`
    by finding integer values for `x` and `y` that yield the closest approximation to `L`.

    The goal is to minimize the residual error `L - (a*x + b*y)` by iterating over a valid range
    of integer `x` values and calculating the corresponding integer `y` values.

    The class implements an optimization technique that reduces the residual by switching the
    coefficients `a` and `b` if necessary, ensuring that the larger coefficient is always associated
    with `x`. This makes the search more efficient.

    Attributes:
    -----------
    _L : float
        The target value `L` to approximate using the linear equation.
    _a : float
        The coefficient for the variable `x` in the equation. Automatically adjusted if `b > a`.
    _b : float
        The coefficient for the variable `y` in the equation. Automatically adjusted if `b > a`.

    Methods:
    --------
    _reduceResidualsInVarSwitching(a: float, b: float) -> None:
        Adjusts coefficients `a` and `b` to ensure that the larger coefficient is used for `x`.

    _getValidXRange() -> range:
        Computes the valid range of integer `x` values based on the given target `L` and coefficient `a`.

    _y(x: float) -> float:
        Computes the corresponding `y` value for a given `x` in the equation.

    _max_y_int(y: float) -> int:
        Returns the largest integer less than or equal to the computed `y` value.

    _errorPlane(x: float | int, y: float | int) -> float:
        Calculates the residual error `L - (a*x + b*y)` for given values of `x` and `y`.

    _getError(x_int: float) -> float:
        Computes the residual error for a given integer `x` and its corresponding integer `y`.

    _minimalErrorGenerator(x_range: range) -> Generator:
        Iterates over the range of `x` values and generates tuples of the minimum residual error
        and the corresponding `x` value.

    _undercutMinError(error_generator: Generator) -> int:
        Extracts the `x` value that yields the minimum residual error from the error generator.

    _printResult(x_sol: int, y_sol: int, len_resi: int, len_time: str) -> None:
        Prints the optimized solution, showing the integer values `x_sol` and `y_sol` and their
        coefficients, the final computed result, and the minimal residual error.

    solve(L: float) -> tuple:
        Executes the minimization process by computing valid `x` values, the corresponding errors,
        and identifying the optimal solution with minimal residual error. Returns a tuple `(x_sol, y_sol)`
        containing the optimized values of `x` and `y`.

    Example:
    --------
    ```python
    if __name__ == '__main__':
        myOpt = Linfit(a=0.80, b=1.25)
        myOpt.solve(L=12321.123123)
    ```
    This will attempt to minimize the residual error for the equation `L = 0.8*x + 1.25*y` where `L` is `12321.123123`
    and print the optimized integer values of `x` and `y` that yield the smallest error.
    """
    def __init__(self, a:float, b:float) -> None:
        """
        Initializes the Linfit class with the coefficients `a` and `b`. The class is designed to find
        integer values for `x` and `y` that minimize the residual error in the equation `L = a*x + b*y`.

        The method automatically adjusts the coefficients to ensure `a >= b`, which optimizes the search
        process by associating the larger coefficient with `x`. This switching is handled internally.

        Parameters:
        -----------
        a : float
            Coefficient for the variable `x` in the linear equation. If `a < b`, the values are swapped.
        b : float
            Coefficient for the variable `y` in the linear equation. If `a < b`, the values are swapped.

        Example:
        --------
        ```python
        myOpt = Linfit(a=0.80, b=1.25)
        ```
        This initializes the optimizer with coefficients `a = 0.80` and `b = 1.25`, but the values will
        be swapped internally so that `a = 1.25` and `b = 0.80`.
        """
        self._reduceResidualsInVarSwitching(a, b)

    
    def _reduceResidualsInVarSwitching(self, a:float, b:float) -> None:
        if a < b:
            self._a, self._b = b, a # switch
        else:
            self._a, self._b = a, b


    def _getValidXRange(self) -> range:
        return range(int(self._L / self._a)+1) # +1 -> range omits last int
    

    def _y(self, x:float) -> float:
        return (self._L - self._a * x) / self._b

    def _max_y_int(self, y:float) -> int:
        return int(y - y%1)
    
    def _errorPlane(self, x:float|int, y:float|int) -> float:
        return self._L - self._a*x - self._b*y


    def _getError(self, x_int:float) -> float:
        y_int = self._max_y_int(self._y(x_int))
        error = self._errorPlane(x_int, y_int)
        return error


    def _minimalErrorGenerator(self, x_range:range) -> Generator:
        min_error = float('inf')
        min_x = None
        for x in x_range:
            error = self._getError(x)
            if error < min_error:
                min_error = error
                min_x = x
                yield min_error, min_x


    def _undercutMinError(self, error_generator: Generator) -> int:
        min_error = float('inf')
        best_x_values = []

        for error, x in error_generator:
            if error < min_error:
                min_error = error
                best_x_values = [x]
            elif error == min_error:
                best_x_values.append(x)
        
        return max(best_x_values)


    def _printResult(self, x_sol:int, y_sol:int, len_resi:int, len_time:str) -> None:

        result_len = self._a * x_sol + self._b * y_sol

        min_error = self._errorPlane(x_sol, y_sol)

        result_string = (
            f"{x_sol} * [{self._a:0.3f}] + "
            f"{y_sol} * [{self._b:0.3f}] + "
            f"{min_error:0.3f} = "
            f"{(result_len+min_error):0.3f}"
        )

        horizonal_bar = "="*len(result_string)

        print(
            "==================\n"
            "optimized solution\n"
            "==================\n"
            f"L = {self._L:0.3f}\n"
            f"a = {self._a:0.3f}\n"
            f"b = {self._b:0.3f}\n"
            f"{horizonal_bar}\n"
            f"{result_string}\n"
            f"{horizonal_bar}\n"
            F"> target len without error: {result_len:0.3f}\n"
            f"> got minimum out of {len_resi} residuals\n"
            f"> optimization took {len_time} sec"
            )


    def solve(self, L:float) -> tuple:
        """
        Executes the minimization process to find integer values `x` and `y` that minimize the residual error 
        in the equation `E = L - a*x - b*y`.

        The method calculates the valid range of `x` values based on the coefficient `a`, computes the 
        corresponding `y` values for each `x`, and identifies the solution with the minimal residual error.
        It also prints the optimized result and displays information about the process, including the number
        of residuals evaluated and the time taken for optimization.

        Parameters:
        -----------
        L : float
            The target value to approximate using the linear equation `L = a*x + b*y`.

        Returns:
        --------
        tuple:
            A tuple `(x_sol, y_sol)` containing the optimized integer values of `x` and `y` that yield the 
            smallest residual error.

        Example:
        --------
        ```python
        myOpt = Linfit(a=0.80, b=1.25)
        x_sol, y_sol = myOpt.solve(L=12321.123123)
        ```
        This will attempt to minimize the residual error for `L = 12321.123123` using the equation 
        `L = 0.8*x + 1.25*y`, and return the optimal `x` and `y` integer values.
        
        The process will also print a formatted solution showing:
        - The coefficients `a` and `b`
        - The computed `x_sol` and `y_sol`
        - The minimal residual error
        - The number of residuals evaluated
        - The time taken for the optimization.
        """
        self._L = L

        x_range = self._getValidXRange()
        error_generator = self._minimalErrorGenerator(x_range)
        
        start_time = time()
        x_sol = self._undercutMinError(error_generator)
        y_sol = self._max_y_int(self._y(x_sol))
        end_time = time()

        len_time = end_time - start_time

        self._printResult(x_sol, y_sol, len(x_range), len_time)

        return x_sol, y_sol




if __name__ == '__main__':
    myOpt = Linfit(a=0.80, b=1.25)
    myOpt.solve(L=1200321.123123)