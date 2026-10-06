from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
import pandas as pd


# =========================================================
# 1. BASIC CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_folder=None)

app.secret_key = "styleai-secret-key-2026"

CORS(app, supports_credentials=True)


# =========================================================
# 2. FILE PATHS
# =========================================================

DATABASE = os.path.join(BASE_DIR, "styleai.db")

EMBEDDINGS_FILE = os.path.join(
    BASE_DIR,
    "df_embeddings.csv"
)


# =========================================================
# 3. LOAD AI EMBEDDINGS
# =========================================================

embeddings_df = None

try:

    if os.path.exists(EMBEDDINGS_FILE):

        embeddings_df = pd.read_csv(
            EMBEDDINGS_FILE
        )

        print(
            f"AI embeddings loaded: "
            f"{len(embeddings_df)} items, "
            f"{embeddings_df.shape[1] - 1} features"
        )

    else:

        print("WARNING: df_embeddings.csv not found.")

except Exception as e:

    print(
        "ERROR loading embeddings:",
        e
    )


# =========================================================
# 4. DATABASE FUNCTIONS
# =========================================================

def get_db():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_db()

    cursor = connection.cursor()


    # -----------------------------
    # Users table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # -----------------------------
    # Recommendations table
    # -----------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            occasion TEXT,

            height REAL,

            style TEXT,

            color TEXT,

            season TEXT,

            outfit_title TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
            REFERENCES users(id)

        )
    """)


    connection.commit()

    connection.close()


# =========================================================
# 5. PASSWORD HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# 6. OUTFIT RECOMMENDATION ENGINE
# =========================================================

def generate_outfit(
    occasion,
    height,
    style,
    color,
    season
):

    occasion_lower = occasion.lower()
    style_lower = style.lower()
    season_lower = season.lower()

    # -----------------------------------------------------
    # Default outfit
    # -----------------------------------------------------

    top = "Classic solid-color shirt"

    bottom = "Straight-fit trousers"

    shoes = "Clean white sneakers"

    accessories = "Minimal watch"

    title = "Smart Everyday Outfit"


    # -----------------------------------------------------
    # Occasion based recommendation
    # -----------------------------------------------------

    if "wedding" in occasion_lower:

        top = "Elegant dress shirt or panjabi"

        bottom = "Tailored formal trousers"

        shoes = "Classic leather shoes"

        accessories = "Minimal watch and simple belt"

        title = "Elegant Wedding Ensemble"


    elif "party" in occasion_lower:

        top = "Stylish textured shirt"

        bottom = "Slim-straight dark trousers"

        shoes = "Clean casual sneakers"

        accessories = "Minimal watch"

        title = "Modern Party Look"


    elif "formal" in occasion_lower:

        top = "Crisp formal shirt"

        bottom = "Tailored formal trousers"

        shoes = "Classic formal shoes"

        accessories = "Leather belt and simple watch"

        title = "Classic Formal Outfit"


    elif "interview" in occasion_lower:

        top = "Solid light-colored formal shirt"

        bottom = "Dark tailored trousers"

        shoes = "Black or brown formal shoes"

        accessories = "Simple watch and belt"

        title = "Professional Interview Look"


    elif "university" in occasion_lower:

        top = "Clean casual shirt or polo"

        bottom = "Straight-fit chinos or jeans"

        shoes = "Clean sneakers"

        accessories = "Simple watch or backpack"

        title = "Smart University Outfit"


    elif "dinner" in occasion_lower:

        top = "Smart casual button-up shirt"

        bottom = "Dark chinos or trousers"

        shoes = "Loafers or clean sneakers"

        accessories = "Minimal watch"

        title = "Smart Dinner Look"


    elif "travel" in occasion_lower:

        top = "Comfortable cotton T-shirt"

        bottom = "Comfortable chinos or jeans"

        shoes = "Comfortable sneakers"

        accessories = "Backpack and simple watch"

        title = "Comfortable Travel Outfit"


    elif "cultural" in occasion_lower:

        top = "Traditional panjabi or kurta"

        bottom = "Comfortable traditional trousers"

        shoes = "Loafers or traditional footwear"

        accessories = "Simple watch"

        title = "Traditional Cultural Look"


    elif "casual" in occasion_lower:

        top = "Clean casual T-shirt or shirt"

        bottom = "Jeans or chinos"

        shoes = "Casual sneakers"

        accessories = "Minimal watch"

        title = "Relaxed Casual Outfit"


    # -----------------------------------------------------
    # Style based modification
    # -----------------------------------------------------

    if "minimal" in style_lower:

        accessories = "Minimal watch"

    elif "streetwear" in style_lower:

        top = "Oversized graphic or solid T-shirt"

        bottom = "Relaxed-fit cargo or trousers"

        shoes = "Classic sneakers"

        accessories = "Cap and minimal accessories"

    elif "traditional" in style_lower:

        top = "Traditional panjabi or kurta"

        bottom = "Comfortable traditional trousers"

        shoes = "Loafers or traditional footwear"

        accessories = "Simple watch"

    elif "formal" in style_lower:

        top = "Crisp formal shirt"

        bottom = "Tailored formal trousers"

        shoes = "Classic leather shoes"

        accessories = "Formal belt and watch"

    elif "smart casual" in style_lower:

        top = "Smart casual button-up shirt"

        bottom = "Chinos or tailored trousers"

        shoes = "Loafers or clean sneakers"

        accessories = "Minimal watch"


    # -----------------------------------------------------
    # Weather based modification
    # -----------------------------------------------------

    if "hot" in season_lower:

        weather_note = (
            "Choose lightweight and breathable fabrics "
            "for hot weather."
        )

    elif "warm" in season_lower:

        weather_note = (
            "Light cotton or linen fabrics are suitable "
            "for warm weather."
        )

    elif "cool" in season_lower:

        weather_note = (
            "Consider a lightweight overshirt or "
            "layer for cooler weather."
        )

    elif "rainy" in season_lower:

        weather_note = (
            "Choose quick-drying fabrics and "
            "water-resistant footwear."
        )

    elif "cold" in season_lower:

        weather_note = (
            "Add a sweater, jacket, or coat "
            "for colder conditions."
        )

    else:

        weather_note = (
            "Choose comfortable fabrics suitable "
            "for the current conditions."
        )


    # -----------------------------------------------------
    # Height based proportion suggestion
    # -----------------------------------------------------

    try:

        height_value = float(height)

    except:

        height_value = 0


    if height_value > 0:

        if height_value < 160:

            height_note = (
                "For garment proportions, slightly shorter "
                "outer layers can create a balanced outfit."
            )

        elif height_value < 175:

            height_note = (
                "Regular-length garments and balanced "
                "proportions are a practical choice."
            )

        else:

            height_note = (
                "Regular or slightly longer garment lengths "
                "can work well for balanced proportions."
            )

    else:

        height_note = (
            "Choose garment lengths that feel comfortable "
            "and provide a balanced fit."
        )


    # -----------------------------------------------------
    # Color recommendation
    # -----------------------------------------------------

    color_note = (
        f"Use {color} as the main or accent color and "
        "combine it with neutral tones such as white, "
        "beige, grey, navy, or black."
    )


    recommended_colors = [
        color,
        "White",
        "Beige",
        "Navy"
    ]


    return {

        "title": title,

        "top": top,

        "bottom": bottom,

        "shoes": shoes,

        "accessories": accessories,

        "weather_note": weather_note,

        "height_note": height_note,

        "color_note": color_note,

        "recommended_colors":
            recommended_colors
    }


# =========================================================
# 7. FRONTEND ROUTES
# =========================================================

@app.route("/")
def home():

    return send_from_directory(
        BASE_DIR,
        "index.html"
    )


@app.route("/style.css")
def style_css():

    return send_from_directory(
        BASE_DIR,
        "style.css"
    )


@app.route("/script.js")
def script_js():

    return send_from_directory(
        BASE_DIR,
        "script.js"
    )


# =========================================================
# 8. SIGN UP
# =========================================================

@app.route(
    "/signup",
    methods=["POST"]
)
def signup():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "Invalid request."
        }), 400


    name = data.get(
        "name",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )


    if not name:

        return jsonify({
            "error": "Name is required."
        }), 400


    if not email:

        return jsonify({
            "error": "Email is required."
        }), 400


    if not password:

        return jsonify({
            "error": "Password is required."
        }), 400


    if len(password) < 6:

        return jsonify({
            "error":
                "Password must be at least 6 characters."
        }), 400


    password_hash = hash_password(
        password
    )


    connection = get_db()

    cursor = connection.cursor()


    try:

        cursor.execute("""
            INSERT INTO users
            (name, email, password)

            VALUES (?, ?, ?)
        """, (
            name,
            email,
            password_hash
        ))

        connection.commit()

        user_id = cursor.lastrowid

        session["user_id"] = user_id

        session["user_name"] = name

        session["user_email"] = email


        return jsonify({

            "success": True,

            "message":
                "Account created successfully.",

            "user": {

                "id": user_id,

                "name": name,

                "email": email

            }

        })


    except sqlite3.IntegrityError:

        return jsonify({

            "error":
                "An account with this email already exists."

        }), 409


    finally:

        connection.close()


# =========================================================
# 9. LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json(
        silent=True
    )

    if not data:

        return jsonify({
            "error": "Invalid request."
        }), 400


    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )


    if not email or not password:

        return jsonify({

            "error":
                "Email and password are required."

        }), 400


    password_hash = hash_password(
        password
    )


    connection = get_db()

    cursor = connection.cursor()


    cursor.execute("""
        SELECT *
        FROM users

        WHERE email = ?
        AND password = ?
    """, (
        email,
        password_hash
    ))


    user = cursor.fetchone()

    connection.close()


    if not user:

        return jsonify({

            "error":
                "Invalid email or password."

        }), 401


    session["user_id"] = user["id"]

    session["user_name"] = user["name"]

    session["user_email"] = user["email"]


    return jsonify({

        "success": True,

        "message":
            "Login successful.",

        "user": {

            "id": user["id"],

            "name": user["name"],

            "email": user["email"]

        }

    })


# =========================================================
# 10. LOGOUT
# =========================================================

@app.route(
    "/logout",
    methods=["POST"]
)
def logout():

    session.clear()

    return jsonify({

        "success": True,

        "message":
            "Logged out successfully."

    })


# =========================================================
# 11. CURRENT USER
# =========================================================

@app.route("/me")
def current_user():

    if "user_id" not in session:

        return jsonify({

            "logged_in": False

        })


    return jsonify({

        "logged_in": True,

        "user": {

            "id":
                session["user_id"],

            "name":
                session["user_name"],

            "email":
                session["user_email"]

        }

    })


# =========================================================
# 12. OUTFIT RECOMMENDATION
# =========================================================

@app.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    # -----------------------------------------------------
    # Get form values
    # -----------------------------------------------------

    occasion = request.form.get(
        "occasion",
        ""
    ).strip()

    height = request.form.get(
        "height",
        ""
    ).strip()

    style = request.form.get(
        "style",
        ""
    ).strip()

    color = request.form.get(
        "color",
        ""
    ).strip()

    season = request.form.get(
        "season",
        ""
    ).strip()


    # -----------------------------------------------------
    # Validation
    # -----------------------------------------------------

    if not occasion:

        return jsonify({
            "error":
                "Please select an occasion."
        }), 400


    if not height:

        return jsonify({
            "error":
                "Please enter your height."
        }), 400


    if not style:

        return jsonify({
            "error":
                "Please select your preferred style."
        }), 400


    if not color:

        return jsonify({
            "error":
                "Please enter your favorite color."
        }), 400


    if not season:

        return jsonify({
            "error":
                "Please select the weather condition."
        }), 400


    # -----------------------------------------------------
    # Validate height
    # -----------------------------------------------------

    try:

        height_value = float(height)

        if height_value <= 0:

            raise ValueError

    except:

        return jsonify({

            "error":
                "Please enter a valid height."

        }), 400


    # -----------------------------------------------------
    # Generate recommendation
    # -----------------------------------------------------

    outfit = generate_outfit(

        occasion=occasion,

        height=height_value,

        style=style,

        color=color,

        season=season

    )


    # -----------------------------------------------------
    # Save recommendation if logged in
    # -----------------------------------------------------

    user_id = session.get(
        "user_id"
    )


    if user_id:

        try:

            connection = get_db()

            cursor = connection.cursor()


            cursor.execute("""
                INSERT INTO recommendations
                (
                    user_id,
                    occasion,
                    height,
                    style,
                    color,
                    season,
                    outfit_title
                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (

                user_id,

                occasion,

                height_value,

                style,

                color,

                season,

                outfit["title"]

            ))


            connection.commit()

            connection.close()


        except Exception as e:

            print(
                "Recommendation save error:",
                e
            )


    # -----------------------------------------------------
    # Dataset status
    # -----------------------------------------------------

    if embeddings_df is not None:

        dataset_info = {

            "loaded": True,

            "items":
                len(embeddings_df),

            "features":
                embeddings_df.shape[1] - 1

        }

    else:

        dataset_info = {

            "loaded": False,

            "items": 0,

            "features": 0

        }


    # -----------------------------------------------------
    # Final response
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "occasion": occasion,

        "height": height_value,

        "style": style,

        "color": color,

        "season": season,

        "outfit": outfit,

        "dataset": dataset_info

    })


# =========================================================
# 13. BACKEND STATUS
# =========================================================

@app.route("/status")
def status():

    return jsonify({

        "backend":
            "StyleAI backend is running",

        "database":
            os.path.exists(DATABASE),

        "embeddings":
            embeddings_df is not None,

        "embedding_items":
            len(embeddings_df)
            if embeddings_df is not None
            else 0,

        "embedding_features":
            embeddings_df.shape[1] - 1
            if embeddings_df is not None
            else 0

    })


# =========================================================
# 14. START APPLICATION
# =========================================================

if __name__ == "__main__":

    # Create database
    create_database()


    print()
    print("=" * 45)
    print("           STYLEAI BACKEND")
    print("=" * 45)

    print(
        f"Database: {DATABASE}"
    )

    print(
        f"Embeddings loaded: "
        f"{embeddings_df is not None}"
    )

    if embeddings_df is not None:

        print(
            f"Items: {len(embeddings_df)}"
        )

        print(
            f"Features: "
            f"{embeddings_df.shape[1] - 1}"
        )

    print("=" * 45)
    print()


    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )