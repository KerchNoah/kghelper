from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Database path
DB_PATH = os.path.join("data", "civ_combos.db")

# Retrieve all combos from DB
def get_combos():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    combos = conn.execute("SELECT * FROM combos").fetchall()
    conn.close()
    return combos

# Retrieve a single combo
def get_combo(id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    combo = conn.execute("SELECT * FROM combos WHERE id = ?", (id,)).fetchone()
    conn.close()
    return combo

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/civ7")
def civ7():
    combos = get_combos()
    return render_template("civ7.html", combos=combos)

@app.route("/add_combo", methods=["POST"])
def add_combo():
    try:
        leader = request.form["leader"]
        civ = request.form["civ"]
        abilities = request.form["abilities"]
        synergy = request.form["synergy"]

        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            INSERT INTO combos (leader, civ, abilities, synergy)
            VALUES (?, ?, ?, ?)
        """, (leader, civ, abilities, synergy))
        conn.commit()
        conn.close()

        return redirect("/civ7")
    except Exception as e:
        return f"Error adding combo: {e}", 500

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_combo(id):
    if request.method == "POST":
        data = (
            request.form["leader"],
            request.form["civ"],
            request.form["abilities"],
            request.form["ancient"],
            request.form["medieval"],
            request.form["modern"],
            request.form["synergy"],
            id
        )
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            UPDATE combos SET
            leader = ?, civ = ?, abilities = ?, ancient_pairing = ?, 
            medieval_pairing = ?, modern_pairing = ?, synergy = ?
            WHERE id = ?
        """, data)
        conn.commit()
        conn.close()
        return redirect("/civ7")
    else:
        combo = get_combo(id)
        return render_template("edit_combo.html", combo=combo)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_combo(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM combos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/civ7")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 for local dev
    app.run(host="0.0.0.0", port=port)