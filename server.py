from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---- Backtracking Algorithm ----
def is_safe(x, y, maze, visited):
    n = len(maze)
    return 0 <= x < n and 0 <= y < n and maze[x][y] == 1 and not visited[x][y]

def solve_maze(maze):
    n = len(maze)
    path = []
    visited = [[False] * n for _ in range(n)]
    found = backtrack(0, 0, maze, visited, path)
    return path if found else None

def backtrack(x, y, maze, visited, path):
    n = len(maze)
    if x == n - 1 and y == n - 1:
        path.append([x, y])
        return True

    if is_safe(x, y, maze, visited):
        visited[x][y] = True
        path.append([x, y])

        # Order: down, right, up, left
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if backtrack(x + dx, y + dy, maze, visited, path):
                return True

        path.pop()
        return False
    return False


# ---- Flask Routes ----
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    maze = data.get('maze')
    result = solve_maze(maze)
    return jsonify({'solution': result})


if __name__ == '__main__':
    app.run(debug=True)

