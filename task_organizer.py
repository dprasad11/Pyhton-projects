from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Daily spent tracker</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { color: #333; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 5px; }
        .completed { color: green; font-weight: bold; }
        .incomplete { color: red; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Daily Task Organizer</h1>
    <form method="post">
        <h2>Enter today's tasks:</h2>
        <textarea name="tasks" rows="6" cols="40" placeholder="One task per line"></textarea><br><br>
        <input type="submit" value="Submit Tasks">
    </form>

    {% if tasks %}
        <h2>Review Tasks</h2>
        <form method="post">
            {% for task in tasks %}
                <label>
                    <input type="checkbox" name="completed" value="{{ task }}">
                    {{ task }}
                </label><br>
            {% endfor %}
            <br>
            <input type="hidden" name="all_tasks" value="{{ tasks|join('||') }}">
            <input type="submit" value="Finish Day">
        </form>
    {% endif %}

    {% if completed_tasks %}
        <h2>✅ Completed Tasks</h2>
        <ul>
        {% for task in completed_tasks %}
            <li class="completed">{{ task }}</li>
        {% endfor %}
        </ul>
    {% endif %}

    {% if incomplete_tasks %}
        <h2>❌ Incomplete Tasks</h2>
        <ul>
        {% for task in incomplete_tasks %}
            <li class="incomplete">{{ task }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    completed_tasks = []
    incomplete_tasks = []
    tasks = None

    if request.method == "POST":
        if "tasks" in request.form:
            tasks = request.form["tasks"].splitlines()
        elif "all_tasks" in request.form:
            tasks = request.form["all_tasks"].split("||")
            completed_tasks = request.form.getlist("completed")
            incomplete_tasks = [task for task in tasks if task not in completed_tasks]

    return render_template_string(html_template, tasks=tasks, 
                                  completed_tasks=completed_tasks, 
                                  incomplete_tasks=incomplete_tasks)

if __name__ == "__main__":
    app.run(debug=True)