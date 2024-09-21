from typing import Generator

class LinearEquationIntegerOptimizer:
    """
    A class designed to minimize the error in a linear equation of the form `L = a*x + b*y`
    by finding integer values for `x` and `y` that yield the closest approximation to `L`.

    The objective is to minimize the residual error `L - (a*x + b*y)` by adjusting `x`
    within a valid range and determining the corresponding integer `y` values.

    Attributes:
    -----------
    _L : float
        The target value `L` to approximate using the linear equation.
    _a : float
        The coefficient for the variable `x` in the equation.
    _b : float
        The coefficient for the variable `y` in the equation.
    _show_residuals : bool
        Whether or not to display the residual errors for the computed `x` values.

    Methods:
    --------
    _getValidXRange() -> range:
        Computes the valid range of integer `x` values based on the constraints of the equation.

    _y(x: float) -> float:
        Computes the corresponding `y` value for a given `x` in the equation.

    _max_y_int(y: float) -> int:
        Returns the largest integer less than or equal to the computed `y` value.

    _errorPlane(x: float | int, y: float | int) -> float:
        Calculates the error or residual `L - (a*x + b*y)` for given values of `x` and `y`.

    _getError(x_int: float) -> float:
        Computes the residual error for a given integer `x` and its corresponding integer `y`.

    _minimalErrorGenerator(x_range: range) -> Generator:
        Generates the minimum residual error and the corresponding `x` value over the given `x` range.

    _extractMinError(error_generator: Generator) -> int:
        Extracts the `x` value that corresponds to the minimum error from the error generator.

    _printResult(x_sol: int, y_sol: int) -> None:
        Prints the optimized solution showing the integer `x` and `y` values, their coefficients, 
        and the final computed result with minimal residual error.

    _solve() -> tuple:
        Executes the minimization process by computing valid `x` values, the corresponding errors, 
        and identifying the optimal solution with minimal error. Returns a tuple of `(x_sol, y_sol)`.

    _main() -> None:
        Orchestrates the minimization process and stores the solution as class attributes.

    Example:
    --------
    ```python
    if __name__ == '__main__':
        myOpt = LinearEquationIntegerOptimizer(L=10.5, a=0.80, b=1.25, show_residuals=False)
    ```
    This will attempt to minimize the residual error for the equation `10.5 = 0.8*x + 1.25*y`
    and print the optimized integer values of `x` and `y` that yield the smallest error.
    """

    def __init__(self, L, a, b, show_residuals: bool = False) -> None:
        """
        Initializes the LinearEquationIntegerOptimizer class with the target length `L`, coefficients `a`
        and `b`, and an option to show residuals.

        Parameters:
        -----------
        L : float
            The target value for the equation `L = a*x + b*y`.
        a : float
            Coefficient for `x` in the equation.
        b : float
            Coefficient for `y` in the equation.
        show_residuals : bool, optional
            Whether to print the residuals (default is False).
        """
        self._L = L
        self._reduceResidualsInVarSwitching(a, b)
        self._show_residuals = show_residuals

        self._main()

    
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


    def _undercutMinError(self, error_generator:Generator) -> int:
        min_error, x_sol = None, None
        for error, x in error_generator:
            min_error, x_sol = error, x
        return x_sol


    def _printResult(self, x_sol:int, y_sol:int, len_resi:int) -> None:

        result_len = self._a * x_sol + self._b * y_sol

        

        result_string = (
            f"\033[32m{x_sol}\033[0m * [{self._a:0.3f}] + "
            f"\033[32m{y_sol}\033[0m * [{self._b:0.3f}] = {result_len:0.3f}"
        )

        horizonal_bar_above_result = "="*len(result_string)

        print(
            "==================\n"
            "optimized solution\n"
            "==================\n"
            f"l = {self._L:0.3f}\n"
            f"a = {self._a:0.3f}\n"
            f"b = {self._b:0.3f}\n"
            f"{horizonal_bar_above_result}\n"
            f"{result_string}\n"
            F"> minmal rest: {self._errorPlane(x_sol, y_sol):0.3f}\n"
            f"> got minimum out of {len_resi} residuals"
            )


    def _solve(self) -> tuple:

        x_range = self._getValidXRange()
        error_generator = self._minimalErrorGenerator(x_range)

        x_sol = self._undercutMinError(error_generator)
        y_sol = self._max_y_int(self._y(x_sol))
        self._printResult(x_sol, y_sol, len(x_range))

        return x_sol, y_sol


    def _main(self) -> None:
        self.x_sol, self.y_sol = self._solve()



if __name__ == '__main__':
    myOpt = LinearEquationIntegerOptimizer(L=10, a=1.25, b=0.80, show_residuals=False)