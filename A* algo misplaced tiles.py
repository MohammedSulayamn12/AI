import heapq

class PuzzleState:
    def __init__(self, board, goal, path=[]):
        self.board = board
        self.goal = goal
        self.path = path
        self.blank = board.index(0)

    def is_goal(self):
        return self.board == self.goal

    def misplaced_tiles(self):
        return sum([1 for i in range(len(self.board)) if self.board[i] != 0 and self.board[i] != self.goal[i]])

    def get_neighbors(self):
        neighbors = []
        moves = [(-1,0),(1,0),(0,-1),(0,1)] # up, down, left, right
        x, y = divmod(self.blank, 3)
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_blank = nx*3+ny
                new_board = self.board[:]
                new_board[self.blank], new_board[new_blank] = new_board[new_blank], new_board[self.blank]
                neighbors.append(PuzzleState(new_board, self.goal, self.path + [new_board]))
        return neighbors

    def __lt__(self, other):
        return True

def a_star_misplaced(initial, goal):
    open_list = []
    heapq.heappush(open_list, (0, PuzzleState(initial, goal, [initial])))
    visited = set()

    while open_list:
        _, current = heapq.heappop(open_list)
        if tuple(current.board) in visited:
            continue
        visited.add(tuple(current.board))

        if current.is_goal():
            return current.path

        g = len(current.path)-1
        h = current.misplaced_tiles()
        f = g+h

        for neighbor in current.get_neighbors():
            if tuple(neighbor.board) not in visited:
                heapq.heappush(open_list, (f, neighbor))

# Example
initial = [2,8,3,1,6,4,7,0,5]
goal = [1,2,3,8,0,4,7,6,5]
solution = a_star_misplaced(initial, goal)

print("Solution Path:")
for state in solution:
    print(state[0:3], "\n", state[3:6], "\n", state[6:9], "\n")
