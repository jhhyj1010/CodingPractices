def reverse_list(l: list):
    """
    Reverse a list without using any built-in functions.
    The function should return a reversed list.
    Input l is a list that may contain any type of data.
    """
    length = len(l)
    for i in range(0, length // 2):
        l[i], l[length - i - 1] = l[length - i - 1], l[i]


def is_valid_sudoku(matrix) -> bool:
    """
    Validate whether a matrix is a valid sudoku
    """
    # Validate Rows
    for i in range(9):
        s = set()
        for j in range(9):
            cell_value = matrix[i][j]
            if cell_value in s:
                return False
            elif cell_value != 0:
                s.add(cell_value)

    # Validate Columns
    for i in range(9):
        s = set()
        for j in range(9):
            cell_value = matrix[j][i]
            if cell_value in s:
                return False
            elif cell_value != 0:
                s.add(cell_value)

    # Validate 3*3 Cells
    starters = [
        (0,0), (0,3), (0,6),
        (3,0), (3,3), (3,6),
        (6,0), (6,3), (6,6)
    ]
    for i, j in starters:
        s = set()
        for r in range(i, i + 3):
            for c in range(j, j + 3):
                cell_value = matrix[r][c]
                if cell_value in s:
                    return False
                elif cell_value != 0:
                    s.add(cell_value)

    return True


def find_empty_cell(matrix):
    """
    Find an empty cell
    """
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return i, j
    return None


def solve_sudoku(matrix):
    """
    Write a program to solve a 9x9 Sudoku board.
    The board must be completed so that every row, column, and 3x3 section
    contains all digits from 1 to 9.
    Input: a 9x9 matrix representing the board.
    """

    # Find out an empty cell
    empty_cell = find_empty_cell(matrix)
    if not empty_cell:
        return True

    r, c = empty_cell
    for number in range(1, 10):
        if is_valid_sudoku(matrix):
            matrix[r][c] = number

            if solve_sudoku(matrix):
                return True
        else:  # Avoid unnecessary checks
            break

        matrix[r][c] = 0

    return False


# Print matrix nicely
def print_matrix(matrix):
    for i in range(9):
        print(matrix[i])
        if i == 2 or i == 5:
            print("---------------------------")


# Test for reverse_list
l1 = [1, 2, 3]
l2 = [1, 2, 3, 4]
reverse_list(l1)
reverse_list(l2)
print(f"List l1 after reversed: {l1}")
print(f"List l2 after reversed: {l2}")


# Test for solve_sudoku
input_board = [
    [5, 0, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 1, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

print(solve_sudoku(input_board))
print("Matrix Board after fix >>>")
print_matrix(input_board)
