from flask import Flask, jsonify, request, render_template, render_template_string
import json

app = Flask(__name__)

tasks = [] # Each task will be a dictionary with 'id', 'task', and 'done' for example {'id': unique_id, 'task': 'Task Text', 'done': False}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:  
        task_id = len(tasks)
        new_task = {'id': task_id, 'task': task_text, 'done': False}
        tasks.append(new_task)
        return render_template_string("""
            <li id="task-{{ new_task.id }}">
                {{ new_task.task }}
                <input type="checkbox" hx-patch="/tasks/{{ new_task.id }}/done" hx-target="#task-{{ new_task.id }}">
                <button hx-delete="/tasks/{{ new_task.id }}/delete" hx-target="#task-{{ new_task.id }}">Delete</button>
            </li>
        """, new_task=new_task)
    return '', 204

@app.route('/tasks', methods=['GET'])
def list_tasks():
    return render_template_string("""
    <ul>
        {% for task in tasks %}
        <li id="task-{{ task.id }}">
            {{ task.task }}
            <input type="checkbox" {% if task.done %}checked{% endif %} hx-patch="/tasks/{{ task.id }}/done" hx-target="#task-{{ task.id }}">
            <button hx-delete="/tasks/{{ task.id }}/delete" hx-target="#task-{{ task.id }}">Delete</button>
        </li>
        {% endfor %}
    </ul>
    """, tasks=tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    new_task = request.form.get('task')
    tasks[task_id] = new_task
    return jsonify({'status': 'success', 'task': new_task})

@app.route('/tasks/<int:task_id>/delete', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return '', 204

@app.route('/tasks/<int:task_id>/done', methods=['PATCH'])
def mark_task_done(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)