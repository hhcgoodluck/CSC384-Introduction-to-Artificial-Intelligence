"""
General notes to consider:
    * The input to these model-generating functions is shaped
      like the following example:

            e.g.
                 [[0,>,0,.,2],
                  [0,.,0,.,0],
                  [0,.,0,<,0]]

            0             -  an empty cell
            .             -  no inequality constraint
            <             -  left cell less than right cell
            >             -  left cell greater than rightcell
            range(1,n+1)  -  pre-set value at this position

      This grid represents the following Futoshiki board:

            e.g.
                -------------
                | _ > _ | 2 |
                | _ | _ | _ |
                | _ | _ < _ |
                -------------

      Note that the input is hence a list of lists where each inner list
      of length 2n - 1 represents a row of the board, where n is the dimension
      of the board.

    * Both models return a tuple (csp, variables):

      csp        - the CSP object representing the Futoshiki game
      variables  - a list of lists of variables corresponding to the
                   solved variables for csp. This list of lists is how
                   the solution to the csp is accessed.

    * An example of how models can be used in conjunction with the
      provided backend:

            e.g.
                 csp, variables = futoshiki_csp_model_1(board)
                 solver = BT(csp)
                 solver.bt_search(prop_FC)

      Upon completion of search, `variables[0][0].get_assigned_value()`
      will return the correct value in the top-left cell of the Futoshiki board.

"""

from typing import Any
from src import Variable, Constraint, CSP, BacktrackingSearch
import itertools


def futoshiki_csp_model_1(grid: list[list[Any]]) -> tuple['CSP', list[list['Variable']]]:
    """
    Return a tuple consisting of the constraint satisfaction problem constructed
    according to the input Futoshiki puzzle grid, and a list of lists of Variable
    objects that represents the matrix of values corresponding to the input grid
    indexed from (0, 0) to (n-1, n-1).

    Constraints for model 1 are built using only binary inequality for both rows
    and columns. That is, all constraints are fixed to two variables in scope.

    :param grid: a list of lists of objects representing the Futoshiki grid, e.g.
                    grid = [[0,>,0,.,2], [0,.,0,.,0], [0,.,0,<,0]]
    # raise NotImplementedError("Futoshiki CSP Model 1 not implemented")
    """
    variables = []
    variable_grid = []
    inequality_grid = []     # stores horizontal relations between adjacent cells

    size = len(grid)
    full_domain = [i + 1 for i in range(size)]

    row_length = len(grid[0])
    inequal_op = ['.', '>', '<']
    constraints = []

    # Step 1: create all variables and record horizontal inequalities
    for i in range(size):
        row_var = []
        row_ieq = []

        for j in range(row_length):
            entry = grid[i][j]

            # Non-symbol entries correspond to actual cells in the puzzle
            if entry not in inequal_op:
                col_idx = j // 2

                if entry == 0:
                    cell_var = Variable(f"V{i}{col_idx}", full_domain)
                else:
                    # A pre-filled cell is represented by a singleton domain
                    cell_var = Variable(f"V{i}{col_idx}", [entry])

                row_var.append(cell_var)
                variables.append(cell_var)

            else:
                # Store '.', '<', or '>' between neighboring cells
                row_ieq.append(entry)

        variable_grid.append(row_var)
        inequality_grid.append(row_ieq)

    # Step 2: create all binary row and column constraints
    for i in range(size):
        for j in range(size):
            for k in range(j + 1, size):

                # Row constraint on (i,j) and (i,k)
                left_var = variable_grid[i][j]
                right_var = variable_grid[i][k]
                row_constraint = Constraint(f"C(V{i}{j},V{i}{k})", [left_var, right_var])

                # If the two variables are adjacent in the row,
                # incorporate the explicit board relation (<, >, or .). Otherwise use !=.
                if k == j + 1:
                    # adjacent: include < or > (or .)
                    op = inequality_grid[i][j]
                else:
                    op = '.'

                # Use full dom to define constraint relation
                row_constraint.add_satisfying_tuples(sat_tuple_generator(op, full_domain, full_domain))
                constraints.append(row_constraint)

                # Column constraint on (j,i) and (k,i)
                top_var = variable_grid[j][i]
                bottom_var = variable_grid[k][i]
                col_constraint = Constraint(f"C(V{j}{i},V{k}{i})", [top_var, bottom_var])
                col_constraint.add_satisfying_tuples(sat_tuple_generator('.', full_domain, full_domain))
                constraints.append(col_constraint)

    # Step 3: assemble the CSP object
    csp_model = CSP(f"size {size} model 1 csp", variables)
    for constraint in constraints:
        csp_model.add_constraint(constraint)

    return csp_model, variable_grid


def sat_tuple_generator(ieq, dom1, dom2):
    satisfying_tuples = []
    for t in itertools.product(dom1, dom2):
        if ieq_check(ieq, t[0], t[1]):
            satisfying_tuples.append(t)
    return satisfying_tuples

def ieq_check(ieq, v1, v2):
    if ieq == '.':
        return v1 != v2
    elif ieq == '>':
        return v1 > v2
    else:
        return v1 < v2



def futoshiki_csp_model_2(grid: list[list[Any]]) -> tuple['CSP', list[list['Variable']]]:
    """
    Return a tuple consisting of the constraint satisfaction problem constructed
    according to the input Futoshiki puzzle grid, and a list of lists of Variable
    objects that represents the matrix of values corresponding to the input grid
    indexed from (0, 0) to (n-1, n-1).

    Constraints for model 2 are built using n-ary all-different constraints
    for both rows and columns. That is, there are 2*n + k total constraints:
    n all-different constraints for rows, n all-different constraints for columns,
    and k binary inequality constraints for the inequalities on the board.

    :param grid: a list of lists of objects representing the Futoshiki grid, e.g.
                    grid = [[0,>,0,.,2], [0,.,0,.,0], [0,.,0,<,0]]

    # raise NotImplementedError("Futoshiki CSP Model 2 not implemented")
    """
    variables = []
    variable_grid = []
    inequality_grid = []    # stores horizontal relations between adjacent cells

    size = len(grid)
    full_domain = [i + 1 for i in range(size)]

    row_length = len(grid[0])
    inequal_op = ['.', '>', '<']

    constraints = []

    # Step 1: create all variables and record the inequality operations
    for row_idx in range(size):
        row_var = []
        row_ieq = []

        for j in range(row_length):
            entry = grid[row_idx][j]

            # A non-symbol entry corresponds to an actual board cell
            if entry not in inequal_op:
                col_idx = j // 2
                if entry == 0:
                    cell_var = Variable("V{}{}".format(row_idx, col_idx), full_domain)
                else:
                    cell_var = Variable("V{}{}".format(row_idx, col_idx), [entry])

                row_var.append(cell_var)
                variables.append(cell_var)

            else:
                # Store the horizontal relation between neighboring cells
                row_ieq.append(entry)

        variable_grid.append(row_var)
        inequality_grid.append(row_ieq)

    # Step 2: build row all-different, column all-different,and binary inequality constraints
    for row_idx in range(size):
        row_scope = variable_grid[row_idx]
        col_scope = []

        row_domains = []
        col_domains = []

        for j in range(size):
            # Collect domains for the row all-different constraint
            row_domains.append(row_scope[j].cur_domain())

            # Build the scope/domains for the column all-different constraint
            col_scope.append(variable_grid[j][row_idx])
            col_domains.append(variable_grid[j][row_idx].cur_domain())

            # Add binary inequality constraint between row_scope[j] and row_scope[j+1]
            if j < size - 1 and inequality_grid[row_idx][j] != '.':
                left_var = variable_grid[row_idx][j]
                right_var = variable_grid[row_idx][j + 1]

                left_domain = left_var.cur_domain()
                right_domain = right_var.cur_domain()

                con = Constraint("C(V{}{},V{}{})".format(row_idx, j, row_idx, j + 1), [left_var, right_var])

                valid_pairs = sat_tuple_generator(inequality_grid[row_idx][j], left_domain, right_domain)
                con.add_satisfying_tuples(valid_pairs)
                constraints.append(con)

        # Create one n-ary all-different constraint for this row
        con_row = Constraint("C(Row{})".format(row_idx), row_scope)
        row_tuples = all_diff_tuple_generator(row_domains)
        con_row.add_satisfying_tuples(row_tuples)

        # Create one n-ary all-different constraint for this column
        con_col = Constraint("C(Col{})".format(row_idx), col_scope)
        col_tuples = all_diff_tuple_generator(col_domains)
        con_col.add_satisfying_tuples(col_tuples)

        constraints.append(con_row)
        constraints.append(con_col)

    # Step 3: assemble the CSP object
    csp_model = CSP("size {} model 2 futoshiki".format(size), variables)
    for constraint in constraints:
        csp_model.add_constraint(constraint)

    return csp_model, variable_grid


def all_diff_tuple_generator(domain_lists):
    """
        Generate all satisfying tuples for an all-different constraint
        over the given list of domains.
        Each tuple is kept only if all assigned values are distinct.
        """
    satisfying_tuples = []

    for candidate in itertools.product(*domain_lists):
        if len(candidate) == len(set(candidate)):
            satisfying_tuples.append(candidate)

    return satisfying_tuples
