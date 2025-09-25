import itertools
import random


class Minesweeper:
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
        # cell is a tuple that contains the coordinates of the cell in the board. (i,j)
        i, j = cell
        return self.board[i][j]
        # Self.board will return True if there is a mine in that cell
        # Self.board will return False if there is no mine in that cell

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


class Sentence:
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
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # Para um set de cells com comprimento x, se o valor encontrado na variavel count for igual a x, entao todas as cells sao minas.
        # Isto porque a variavel count vai ser igual ao numero de minas (celulas com o valor True) que existam adjacentes a uma cell.
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Se o valor da variavel count for igual a 0, entao todas as cells sao seguras (False).
        # Não ha celulas adjacentes com o valor True (que representam minas).
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Se a cell está no set de cells, remove-a e decrementa o count, pois uma mina foi encontrada.
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Se a cell está no set de cells, remove-a apenas.
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
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
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1. Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2. Mark the cell as safe
        self.mark_safe(cell)

        # 3. Add a new sentence to the AI's knowledge base
        # based on the value of `cell` and `count`

        # Find neighbors of cell to create a sentence. Loop over all cells
        # within one row and column and check if neighbor is in bounds and is unconfirmed
        unconfirmed_cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # If cell is a known mine then decrease mines count and continue
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # If we know that the cell is already safe then continue loop
                if (i, j) in self.safes:
                    continue

                # After all can be an unconfirmed neighbor if cell is in grid's bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    unconfirmed_cells.add((i, j))

        # Creating sentence object with all unconfirmed neighbors and
        # number of mines around the cell minus number of known mines (already flagged)
        new_sentence = Sentence(unconfirmed_cells, count)

        # Add a new sentence to the knowledge base:
        self.knowledge.append(new_sentence)

        # 4 & 5. Repeat inference until no more progress
        changed = True
        while changed:
            changed = False

            # Check known safes/mines
            for sentence in self.knowledge:
                for cell in sentence.known_safes().copy():
                    if cell not in self.safes:
                        self.mark_safe(cell)
                        changed = True
                for cell in sentence.known_mines().copy():
                    if cell not in self.mines:
                        self.mark_mine(cell)
                        changed = True

            # Subset inference
            new_sentences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1 == s2:
                        continue
                    if s1.cells.issubset(s2.cells):
                        new_sentence = Sentence(
                            s2.cells - s1.cells, s2.count - s1.count
                        )
                        if (
                            new_sentence not in self.knowledge
                            and new_sentence not in new_sentences
                        ):
                            new_sentences.append(new_sentence)
            if new_sentences:
                self.knowledge.extend(new_sentences)
                changed = True

        # Remove empty sentences
        self.knowledge = [s for s in self.knowledge if s.cells]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_cells = []

        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_cells.append(cell)

        if len(possible_cells) == 0:
            return None
        return random.choice(possible_cells)
