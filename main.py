class MinimiseError:
    def __init__(self, L, a, b) -> None:
        """
        A class to find an optimal integer solution to the equation:

            L = a * x + b * y + E

        where:
            - L is a given constant (the target value),
            - a and b are floating-point coefficients,
            - x and y are non-negative integers,
            - E is the error term that we aim to minimize.
        
        The goal of this class is to find the values of x and y that minimize the error E, 
        effectively making L as close as possible to a * x + b * y.

        Attributes:
        -----------
        _L : float
            The target value for the equation.
        _a : float
            Coefficient of the x variable (floating-point).
        _b : float
            Coefficient of the y variable (floating-point).
        x_sol : int
            The optimized integer solution for x.
        y_sol : int
            The optimized integer solution for y.
        
        Methods:
        --------
        __init__(L: float, a: float, b: float) -> None:
            Initializes the optimizer with the given constants L, a, and b, and immediately 
            solves the equation to find the optimal values of x and y.
        
        _getYRange() -> list[int]:
            Computes and returns the valid range of y values by ensuring the equation remains 
            within non-negative integers.
        
        _x(y: float) -> float:
            Computes the x value corresponding to a given y using the equation L = a * x + b * y.
        
        _y(x: float) -> float:
            Computes the y value corresponding to a given x using the equation L = a * x + b * y.
        
        _x_residual(y: float) -> float:
            Computes the fractional (residual) part of x for a given y.
        
        _y_residual(x: float) -> float:
            Computes the fractional (residual) part of y for a given x.
        
        _dist_d(x_res: float, y_res: float) -> float:
            Computes the shortest distance between the residuals of x and y, representing the 
            "error" in the approximation of the solution.
        
        _getDistance(y: int) -> float:
            For a given y, calculates the residual error based on the corresponding x and y values.
        
        _plane_eq(x: float, y: float) -> float:
            Computes the error term E using the plane equation:

                E = L - (a * x + b * y)
        
        _mapDistancesToY(y_range: list[int]) -> list[float, complex]:
            Maps the residual distances for a given y range.
        
        _mapRealDistances(y_range: list[int], distances: list[float, complex]) -> dict:
            Filters and returns only the real distances from the calculated residual distances.
        
        solve() -> tuple[int, int]:
            Iterates through possible y values to minimize the error E and returns the optimal 
            integer values of x and y that solve the equation with the smallest error.
        
        _main() -> None:
            Calls the solver to find the optimized solution and stores the results (x_sol, y_sol) 
            as attributes.

        Example:
        --------
        To use this optimizer, instantiate it with specific values for L, a, and b:

            myOpt = MinimiseError(L=153540.405, a=0.83, b=1.25)

        This will immediately solve the equation and store the optimized values of x and y in 
        the instance's `x_sol` and `y_sol` attributes.
        """
        self._L = L
        self._a = a
        self._b = b

        self._main()



    def _getYRange(self) -> list[int]:
        rational_Y = (self._L / self._b)
        max_Y = int(rational_Y - rational_Y%1)
        return list(range(int(max_Y)+1)) # +1 -> range omits last int
    

    def _x(self, y:float) -> float:
        return (self._L - self._b * y) / self._a
    
    def _y(self, x:float) -> float:
        return (self._L - self._a * x) / self._b

    def _x_residual(self, y:float) -> float:
        return self._x(y)%1
    
    def _y_residual(self, x:float) -> float:
        return self._y(x)%1


    def _dist_d(self, x_res:float, y_res:float) -> float:
        r_x, r_y = x_res, y_res
        if x_res == y_res and x_res == 0:
            return 0
        
        d = ( # shortest distance to line in x-y Plane with L = 0
            (
            -r_x**(8)
            -2*r_x**(6)*(2*r_y**(2)-1)
            -r_x**(4)*(6*r_y**(4)-6*r_y**(2)+1)
            -2*r_x**(2)*r_y**(2)*(2*r_y**(4)-3*r_y**(2)-1)
            -r_y**(4)*(r_y**(4)-2*r_y**(2)+1)
            )**(1/2)
            /(2*(r_x**(2)+r_y**(2)))
            )
        
        return d
    

    def _getDistance(self, y:int) -> float:
        x_res = self._x_residual(y)
        x = self._x(y)-self._x(y)%1
        y_res = self._y_residual(x)
        d = self._dist_d(x_res, y_res)
        return d 


    def _plane_eq(self, x:float, y:float) -> float:
        return self._L - self._a*x -self._b*y
    

    def _mapDistancesToY(self, y_range:list[int]) -> list[float, complex]:
        distances = list(map(self._getDistance, y_range))
        return distances


    def _mapRealDistances(
            self,
            y_range:list[int],
            distances:list[float, complex]
            ) -> dict:
        
        real_distances_for_y = {}
        for index, y in enumerate(y_range):
            dist = distances[index]
            if isinstance(dist, float):
                real_distances_for_y[dist] = y

        return real_distances_for_y


    def solve(self) -> tuple:

        y_range = self._getYRange()
        distances = self._mapDistancesToY(y_range)
        real_distances = self._mapRealDistances(y_range, distances)
        min_dist = min(real_distances)

        y_sol = real_distances[min_dist]
        x_sol = int(self._x(y_sol) - self._x(y_sol)%1)

        result_len = x_sol * self._a + y_sol * self._b

        print(
            "==================\n"
            "optimized solution\n"
            "==================\n"
            f"l = {self._L:0.3f}\n"
            f"a = {self._a:0.3f}\n"
            f"b = {self._b:0.3f}\n"
            "==========================================\n"
            f"{x_sol} x {self._a:0.3f} + "
            f"{y_sol} x {self._b:0.3f} = {result_len:0.3f}\n"
            F"> minmal rest: {self._plane_eq(x_sol, y_sol):0.3f}\n"
            f"> checked {len(real_distances)} residuals"
            )

        return x_sol, y_sol


    def _main(self) -> None:
        self.x_sol, self.y_sol = self.solve()



if __name__ == '__main__':
    myOpt = MinimiseError(L=153540.405, a=0.83, b=1.25)