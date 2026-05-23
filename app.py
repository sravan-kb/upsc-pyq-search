import os
import re

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text

# Create FastAPI app
app = FastAPI()

# PostgreSQL connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:projectdata@localhost:5432/upsc_questions"
)

# Create database engine
engine = create_engine(DATABASE_URL)


# HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>

    <head>

        <title>UPSC PYQ Search Engine</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                font-family: Arial;
                background-color: #f5f5f5;
                text-align: center;
                margin-top: 100px;
                padding: 0 20px;
            }

            h1 {
                color: darkblue;
                margin-bottom: 10px;
                font-size: clamp(22px, 5vw, 36px);
            }

            .tagline {
                color: gray;
                margin-bottom: 40px;
                font-size: clamp(14px, 3vw, 18px);
            }

            .search-bar {
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }

            input {
                width: 100%;
                max-width: 600px;
                padding: 14px;
                font-size: 18px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }

            button {
                padding: 14px 22px;
                font-size: 18px;
                border-radius: 10px;
                border: none;
                background-color: darkblue;
                color: white;
                cursor: pointer;
                width: 100%;
                max-width: 600px;
            }

            @media (min-width: 600px) {
                button {
                    width: auto;
                    max-width: none;
                }
            }

            button:hover {
                background-color: navy;
            }

            .footer-text {
                margin-top: 80px;
                color: gray;
                font-size: 16px;
                padding: 0 10px;
            }

            .social-bar {
                position: fixed;
                top: 20px;
                right: 30px;
                display: flex;
                gap: 12px;
                align-items: center;
            }

            .social-bar a {
                display: flex;
                align-items: center;
                gap: 7px;
                text-decoration: none;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 9px 16px;
                border-radius: 8px;
                background-color: darkblue;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                transition: background-color 0.2s, box-shadow 0.2s;
            }

            .social-bar a:hover {
                background-color: navy;
                box-shadow: 0 4px 14px rgba(0,0,0,0.3);
            }

            .social-bar img {
                width: 18px;
                height: 18px;
                filter: brightness(0) invert(1);
            }

        </style>

    </head>

    <body>

        <div class="social-bar">
            <a href="https://www.linkedin.com/in/sravan-branwal" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
                LinkedIn
            </a>
            <a href="https://github.com/sravan-kb" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="white">
                    <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
                </svg>
                GitHub
            </a>
        </div>

        <h1>UPSC PYQ Search</h1>

        <p class="tagline">
            Search UPSC Previous Year Questions instantly
            <br>
            <span>Starting with Prelims Paper-1 — Mains on the way 🚀</span>
        </p>

        <form action="/search" method="get">
            <div class="search-bar">
                <input
                    type="text"
                    name="q"
                    placeholder="Search UPSC keywords..."
                >
                <button type="submit">
                    Search
                </button>
            </div>
        </form>

        <p class="footer-text">
            With 💖 for ALL the Aspirants
        </p>

    </body>

    </html>
    """


# SEARCH PAGE
@app.get("/search", response_class=HTMLResponse)
def search_questions(q: str):

    # Split search query into words
    words = q.split()

    # Common stop words
    stop_words = {
        "the",
        "is",
        "of",
        "and",
        "a",
        "an",
        "what",
        "which",
        "in",
        "on",
        "to",
        "for",
        "consider"
    }

    # Remove stop words
    words = [
        word
        for word in words
        if word.lower() not in stop_words
    ]

    # If all words removed
    if len(words) == 0:

        return """
        <h2>Please enter meaningful keywords.</h2>
        """

    # Store SQL conditions
    conditions = []

    # Store SQL parameters
    params = {}

    # Build SQL conditions
    for i, word in enumerate(words):

        conditions.append(
            f"full_text ILIKE :word{i}"
        )

        params[f"word{i}"] = f"%{word}%"

    # Join conditions with OR
    where_clause = " OR ".join(conditions)

    # Build relevance score
    score_parts = []

    for i, word in enumerate(words):

        score_parts.append(
            f"""
            CASE
                WHEN full_text ILIKE :word{i}
                THEN 1
                ELSE 0
            END
            """
        )

    score_sql = " + ".join(score_parts)

    # SQL query
    sql = f"""
        SELECT
            year,
            question_number,
            full_text,
            ({score_sql}) AS score

        FROM questions

        WHERE {where_clause}

        ORDER BY
            score DESC,
            question_number ASC

        LIMIT 20
    """

    query = text(sql)

    # Execute query
    with engine.connect() as connection:

        results = connection.execute(query, params)

        rows = results.fetchall()

    # Build HTML response
    html = f"""
    <html>

    <head>

        <title>Search Results</title>

        <style>

            body {{
                font-family: Arial;
                margin: 40px;
                line-height: 1.8;
                background-color: #f5f5f5;
            }}

            h1 {{
                color: darkblue;
                margin-bottom: 30px;
            }}

            .question {{
                background-color: white;
                margin-bottom: 40px;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}

            h2 {{
                color: darkblue;
            }}

            .score {{
                color: green;
                font-weight: bold;
                margin-bottom: 10px;
            }}

            a {{
                text-decoration: none;
                color: darkblue;
                font-weight: bold;
            }}

            mark {{
                background-color: yellow;
                padding: 2px;
            }}

        </style>

    </head>

    <body>

        <a href="/">← Back to Search</a>

        <h1>Search Results for: "{q}"</h1>
    """

    # Add search results
    for row in rows:

        question_text = row.full_text

        # Highlight search words
        for word in words:

            pattern = re.compile(
                re.escape(word),
                re.IGNORECASE
            )

            question_text = pattern.sub(
                lambda match:
                f"<mark>{match.group(0)}</mark>",
                question_text
            )

        # Convert line breaks
        question_text = question_text.replace(
            "\n",
            "<br>"
        )

        html += f"""
        <div class="question">

            <h2>
                {row.year} • Question {row.question_number}
            </h2>

            <div class="score">
                Match Score: {row.score}
            </div>

            <p>{question_text}</p>

        </div>
        """

    # No results case
    if len(rows) == 0:

        html += """
        <h2>No matching questions found.</h2>
        """

    html += """
    </body>
    </html>
    """

    return html