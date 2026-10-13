from flask import Flask, render_template, request
import sqlite3
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = str(BASE_DIR / "lab.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Login Lab: Classic & Error-based SQL Injection
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #INTENTIONALLY VULNERABLE: local training lab
        query = (
            f"SELECT * FROM users "
            f"WHERE username = '{username}' "
            f"AND password = '{password}'"
        )
        print(query)

        conn = get_db()

        try:
            user = conn.execute(query).fetchone()
            print("RESULT:", user)

            if user:
                message = f"Welcome, {user['username']}!"
            else:
                message = "Invalid username or password."

        except sqlite3.Error as error:
            message = (
                f"Database error: {error}\n\n"
                f"SQL query: {query}"
        )
        finally:
            conn.close()

    return render_template("login.html", message=message)


#MyShop: UNION SQL Injection
@app.route("/shop")
def shop():
    search_term = request.args.get("q", "")

    #INTENTIONALLY VULNERABLE: local UNION SQLi lab
    query = f"""
        SELECT id, name, category, price, description
        FROM products
        WHERE name LIKE '%{search_term}%'
    """

    print("SHOP QUERY:", query)
    conn = get_db()

    try:
        results = conn.execute(query).fetchall()

        return render_template(
            "shop.html",
            results=results,
            error=None,
            search_term=search_term
        )

    except sqlite3.Error as error:
        print("SQLITE ERROR:", repr(error))

        return render_template(
            "shop.html",
            results=None,
            error=str(error),
            search_term=search_term
        )

    finally:
        conn.close()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
