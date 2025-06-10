from flask import Flask, render_template, request, redirect, url_for
import json
import uuid
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'diary.json'

def load_entries():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_entries(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=4)

@app.route('/')
def index():
    entries_by_date = load_entries()
    sorted_dates = sorted(entries_by_date.keys(), reverse=True)
    return render_template('index.html', entries_by_date=entries_by_date, sorted_dates=sorted_dates)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        title = request.form['title']
        mood = request.form['mood']
        content = request.form['content']
        date = datetime.now().strftime("%Y-%m-%d")
        entry_id = str(uuid.uuid4())

        new_entry = {
            "id": entry_id,
            "title": title,
            "mood": mood,
            "content": content,
            "time": datetime.now().strftime("%H:%M")
        }

        entries = load_entries()
        if date not in entries:
            entries[date] = []
        entries[date].append(new_entry)
        save_entries(entries)
        return redirect(url_for('index'))

    return render_template('add.html')



@app.route('/edit/<entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    entries = load_entries()
    for date, date_entries in entries.items():
        for entry in date_entries:
            if entry['id'] == entry_id:
                if request.method == 'POST':
                    entry['title'] = request.form['title']
                    entry['mood'] = request.form['mood']
                    entry['content'] = request.form['content']
                    save_entries(entries)
                    return redirect(url_for('index'))
                return render_template('edit.html', entry=entry)
    return "Entry not found", 404


@app.route('/delete/<entry_id>')
def delete_entry(entry_id):
    entries = load_entries()
    for date in list(entries):
        entries[date] = [e for e in entries[date] if e['id'] != entry_id]
        if not entries[date]:
            del entries[date]
    save_entries(entries)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



