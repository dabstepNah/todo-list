from flask import Flask, request, jsonify

app = Flask(__name__)

todos = [ # имитация базы данных 
    {
        'id': 1,
        'title': 'Выучить Docker',
        'done': False
    },
    {
        'id': 2,
        'title': 'Сделать проект',
        'done': True
    }
]

next_id = 3

@app.route('/')
def home():
    return 'Todo API is running'

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            return jsonify(todo), 200
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    global next_id
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    new_todo = {
        'id': next_id,
        'title': data['title'],
        'done': False
    }
    
    todos.append(new_todo)
    next_id += 1
    
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    
    for todo in todos:
        if todo['id'] == todo_id:
            if 'title' in data:
                todo['title'] = data['title']
            if 'done' in data:
                todo['done'] = data['done']
            return jsonify(todo), 200
    
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    
    for i, todo in enumerate(todos):
        if todo['id'] == todo_id:
            deleted = todos.pop(i)
            return jsonify({'message': f'Todo {deleted["id"]} deleted'}), 200
    
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)