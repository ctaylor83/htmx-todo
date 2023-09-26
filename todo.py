from flask import Flask, jsonify, request, render_template, render_template_string

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.form.get('task')
    print(f"Received task: {task}")  # Debugging line
    if task:  # Only append if task is not None or empty
        tasks.append(task)
    task_html = render_template_string("""
    <li>{{ task }}</li>
    """, task=task)
    return task_html

@app.route('/tasks', methods=['GET'])
def list_tasks():
    task_html = render_template_string("""
    <ul>
        {% for task in tasks %}
            <li>{{ task }}</li>
        {% endfor %}
    </ul>
    """, tasks=tasks)
    return task_html

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    new_task = request.form.get('task')
    tasks[task_id] = new_task
    return jsonify({'status': 'success', 'task': new_task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    del tasks[task_id]
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)