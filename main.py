

class LinearEquationErrorMinimizer:
    """
    A class to minimize the error in a linear equation of the form `L = a*x + b*y` 
    by finding integer values of `x` and `y` that yield the closest approximation.

    The goal is to minimize the error (or residual) `L - (a*x + b*y)` by adjusting `x` 
    within a valid range and calculating the corresponding integer `y` values.

    Attributes:
    -----------
    _L : float
        The target length `L` that we aim to approximate using the linear equation.
    _a : float
        The coefficient for the variable `x`.
    _b : float
        The coefficient for the variable `y`.
    _show_residuals : bool
        Whether or not to display the residual errors for all computed `x` values.

    Methods:
    --------
    _getValidXRange() -> list[int]:
        Computes the valid range of integer `x` values based on the equation constraints.

    _y(x: float) -> float:
        Computes the corresponding `y` value (float) for a given `x` in the equation.

    _max_y_int(y: float) -> int:
        Returns the largest integer less than or equal to the computed `y` value.

    _errorPlane(x: float | int, y: float | int) -> float:
        Calculates the error or residual `L - (a*x + b*y)` for given values of `x` and `y`.

    _getError(x_int: float) -> float:
        Computes the error for a given integer `x` and its corresponding integer `y`.

    _mapErrorsToX(x_range: list[float]) -> dict[float, int]:
        Maps computed errors to their respective `x` values for a given range of `x`.

    _extractMinError(x_error_map: dict) -> dict:
        Finds the `x` value that corresponds to the smallest error.

    _printResiduals(errors: dict) -> None:
        Displays the residual errors for all computed `x` values if requested.

    _printResult(x_sol: int, y_sol: int, len_resi: int) -> None:
        Prints the optimized solution showing `x` and `y` values, their coefficients,
        and the final computed result with minimal error.

    _solve() -> tuple:
        Executes the minimization process by calculating valid `x` values, corresponding
        errors, and finding the optimal solution with minimal error. Returns the solution
        `(x_sol, y_sol, errors)`.

    _main() -> None:
        Initializes the minimization process and stores the solution as class attributes.

    Example:
    --------
    ```python
    if __name__ == '__main__':
        myOpt = LinearEquationErrorMinimizer(L=10.5, a=0.80, b=1.25, show_residuals=False)
    ```
    This will minimize the error for the equation `10.5 = 0.8*x + 1.25*y` and print 
    the optimized integer values of `x` and `y` with the smallest residual error.
    """

    def __init__(self, L, a, b, show_residuals: bool = False) -> None:
        """
        Initializes the LinearEquationErrorMinimizer class with the target length `L`, coefficients `a`
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
        self._a = a
        self._b = b
        self._show_residuals = show_residuals

        self._main()


    def _getValidXRange(self) -> list[int]:
        rational_X = (self._L / self._a)
        max_X = int(rational_X - rational_X%1)
        return list(range(int(max_X)+1)) # +1 -> range omits last int
    

    def _y(self, x:float) -> float:
        return (self._L - self._a * x) / self._b

    def _max_y_int(self, y:float) -> int:
        return y - y%1
    
    def _errorPlane(self, x:float|int, y:float|int) -> float:
        return self._L - self._a*x - self._b*y


    def _getError(self, x_int:float) -> float:
        y_int = self._max_y_int(self._y(x_int))
        error = self._errorPlane(x_int, y_int)
        return error


    def _mapErrorsToX(self, x_range:list[float]) -> dict[float, int]:
        errors = list(map(self._getError, x_range))
        x_error_map = dict(zip(errors, x_range))
        return x_error_map


    def _extractMinError(self, x_error_map:dict) -> dict:
        min_error = min(x_error_map)
        return x_error_map[min_error]


    def _printResiduals(self, errors:dict) -> None:

        print(
            "=========================\n"
            f"'error:x_int_value' dict\n"
            "=========================\n"
            f"\n{errors}\n"
            )


    def _printResult(self, x_sol:int, y_sol:int, len_resi:int) -> None:

        result_len = self._a * x_sol + self._b * y_sol

        result_string = (
            f"{x_sol} * [{self._a:0.3f}] + "
            f"{y_sol} * [{self._b:0.3f}] = {result_len:0.3f}"
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
            f"> got mininum out of {len_resi} residuals"
            )


    def _solve(self) -> tuple:

        x_range = self._getValidXRange()
        errors = self._mapErrorsToX(x_range)

        x_sol = self._extractMinError(errors)
        y_sol = self._max_y_int(self._y(x_sol))

        if self._show_residuals:
            self._printResiduals(errors)

        self._printResult(x_sol, y_sol, len(errors))

        return x_sol, y_sol, errors


    def _main(self) -> None:
        self.x_sol, self.y_sol, self.residuals = self._solve()



if __name__ == '__main__':
    myOpt = LinearEquationErrorMinimizer(L=20.5, a=0.80, b=1.25, show_residuals=False)