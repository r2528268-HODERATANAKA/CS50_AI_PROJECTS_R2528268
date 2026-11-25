import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        # If the number of cells equals the count, every cell is a mine
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        # If the count is 0, every cell is safe
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        # A mine is removed from the sentence, so the count goes down by 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        # A safe cell is just removed from the sentence
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # 3) Build a new sentence from the undecided neighbors
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                neighbor = (i, j)

                # Skip the cell itself and cells outside the board
                if neighbor == cell:
                    continue
                if not (0 <= i < self.height and 0 <= j < self.width):
                    continue

                if neighbor in self.mines:
                    count -= 1  # already known mine: not undecided
                elif neighbor not in self.safes:
                    neighbors.add(neighbor)

        self.knowledge.append(Sentence(neighbors, count))

        # 4) and 5) Use the new knowledge to draw more conclusions
        self.update_knowledge()

    def update_knowledge(self):

        #Keeps drawing conclusions until nothing new can be learned.

        changed = True
        while changed:
            changed = False

            # Mark mines and safes that the sentences tell us about
            for sentence in self.knowledge:
                for mine in sentence.known_mines():
                    self.mark_mine(mine)
                    changed = True
                for safe in sentence.known_safes():
                    self.mark_safe(safe)
                    changed = True

            # Throw away empty sentences, they tell us nothing
            self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]

            # If one sentence is a subset of another, subtract them:
            # {A, B, C} = 2 and {A, B} = 1  gives  {C} = 1
            for small in list(self.knowledge):
                for big in list(self.knowledge):
                    if small.cells < big.cells:
                        new_sentence = Sentence(big.cells - small.cells,
                                                big.count - small.count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            changed = True

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_moves.append(cell)

        if len(possible_moves) == 0:
            return None
        return random.choice(possible_moves)
