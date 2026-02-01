import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
# The enforce_node_consistency function should update self.domains such that each variable is node consistent.

#     Recall that node consistency is achieved when, for every variable, 
# each value in its domain is consistent with the variable’s unary constraints. 
# In the case of a crossword puzzle, this means making sure that every value in 
# a variable’s domain has the same number of letters as the variable’s length.
#     To remove a value x from the domain of a variable v, 
# since self.domains is a dictionary mapping variables to sets of values, you can call self.domains[v].remove(x).
#     No return value is necessary for this function.

        for var in self.domains:
            
            for word in set(self.domains[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
    #     The revise function should make the variable x arc consistent with the variable y.

    # x and y will both be Variable objects representing variables in the puzzle.
    # Recall that x is arc consistent with y when every value in the domain of x has a possible value in the domain of y 
    # that does not cause a conflict. (A conflict in the context of the crossword puzzle is a square for which 
    # two variables disagree on what character value it should take on.)
    # To make x arc consistent with y, you’ll want to remove any value from the domain of x 
    # that does not have a corresponding possible value in the domain of y.
    # Recall that you can access self.crossword.overlaps to get the overlap, if any, between two variables.
    # The domain of y should be left unmodified.
    # The function should return True if a revision was made to the domain of x; it should return False if no revision was made.
        
        # print(x)
        # print(self.domains[x])
        # print(y, self.domains[y])
        # print(self.crossword.overlaps[x,y][1])

        letter_x = self.crossword.overlaps[x,y][0]
        letter_y = self.crossword.overlaps[x,y][1]

        change = False

        for word1 in set(self.domains[x]):
            check = 0
            for word2 in self.domains[y]:
                if word1[letter_x] != word2[letter_y]:
                    check += 1
            if check == len(self.domains[y]):
                self.domains[x].remove(word1)
                change = True

        return change



    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
    # The ac3 function should, using the AC3 algorithm, enforce arc consistency on the problem. 
    # Recall that arc consistency is achieved when all the values in each variable’s domain satisfy that variable’s binary constraints.

    # Recall that the AC3 algorithm maintains a queue of arcs to process. 
    # This function takes an optional argument called arcs, representing an initial list of arcs to process. 
    # If arcs is None, your function should start with an initial queue of all of the arcs in the problem. 
    # Otherwise, your algorithm should begin with an initial queue of only the arcs that are in the list arcs 
    # (where each arc is a tuple (x, y) of a variable x and a different variable y).
    # Recall that to implement AC3, you’ll revise each arc in the queue one at a time. 
    # Any time you make a change to a domain, though, 
    # you may need to add additional arcs to your queue to ensure that other arcs stay consistent.
    # You may find it helpful to call on the revise function in your implementation of ac3.
    # If, in the process of enforcing arc consistency, 
    # you remove all of the remaining values from a domain, 
    # return False (this means it’s impossible to solve the problem, 
    # since there are no more possible values for the variable). Otherwise, return True.
    # You do not need to worry about enforcing word uniqueness in this function 
    # (you’ll implement that check in the consistent function.)

        if arcs == None:
            queue = []
            for varx in self.domains:
                for vary in self.crossword.neighbors(varx):
                    if varx != vary:
                        queue.append((varx,vary))
        else:
            queue = arcs
        
        while queue:
            (x, y) = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z,x))
        return True

        


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
    #     The assignment_complete function should (as the name suggests) check to see if a given assignment is complete.

    # An assignment is a dictionary where the keys are Variable objects and the values are strings representing the words those variables will take on.
    # An assignment is complete if every crossword variable is assigned to a value (regardless of what that value is).
    # The function should return True if the assignment is complete and return False otherwise.

        for var in self.domains:
            if var not in assignment:
                return False
        return True



    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        check = set()

        for var in assignment:
            if var.length != len(assignment[var]):
                return False
            for c in check:
                if c == assignment[var]:
                    return False
            check.add(assignment[var])

            for var2 in assignment:
                if var != var2:
                    if self.crossword.overlaps[var, var2]:
                        (i, j) = self.crossword.overlaps[var, var2]
                        if assignment[var][i] != assignment[var2][j]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        s_val = {}

        for word1 in self.domains[var]:
            score = 0
            for var2 in self.crossword.neighbors(var):
                (i, j) = self.crossword.overlaps[var, var2] 
                for word2 in self.domains[var2]:
                    if word1[i] != word2[j]:
                        score += 1
            s_val.update({word1:score})

        return [v[0] for v in sorted(s_val.items(), key = lambda item:item[1], reverse = False)]   

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        size = float('inf')

        for var in self.domains:
            if var not in assignment:
                if len(self.domains[var]) < size:
                    size = len(self.domains[var])
                    ans = var
                elif len(self.domains[var]) == size:
                    if self.crossword.neighbors(var) > self.crossword.neighbors(ans):
                        ans = var
        return ans

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if len(assignment) == len(self.domains):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment.update({var:value})
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
    
