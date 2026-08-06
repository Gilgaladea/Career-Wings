from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from anthropic import (
    Anthropic,
    RateLimitError,
    APIConnectionError,
    AuthenticationError,
    APIError,
)

load_dotenv()
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 1024

app = Flask(__name__)


def zapytaj_claude(tresc_pytania, system_prompt):
    try:
        odpowiedz = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": tresc_pytania}],
        )
        return odpowiedz.content[0].text

    except AuthenticationError:
        return "BŁĄD: nieprawidłowy klucz API."
    except RateLimitError:
        return "BŁĄD: zbyt wiele zapytań. Spróbuj za chwilę."
    except APIConnectionError:
        return "BŁĄD: problem z połączeniem internetowym."
    except APIError as blad:
        return f"BŁĄD: {blad}"


def wybierz_osobowosc(wybor):
    if wybor == "1":
        return "Posiadasz praworządnie dobrą osobowość. Bądź pomocny, miły, uczciwy. Przestrzegaj zasad."
    elif wybor == "2":
        return "Jesteś chaotycznie złym doradcą. Odpowiadaj przewrotnie, z sarkazmem i lekceważeniem zasad."
    else:
        return "Posiadasz neutralną osobowość."


@app.route("/")
def strona_glowna():
    return render_template("index.html", odpowiedz=None)


@app.route("/zapytaj", methods=["POST"])
def zapytaj():
    tresc_pytania = request.form.get("pytanie", "").strip()
    wybor = request.form.get("wybor", "")

    if tresc_pytania == "":
        return render_template(
            "index.html",
            odpowiedz="Wpisz najpierw jakieś pytanie!",
        )

    system_prompt = wybierz_osobowosc(wybor)
    odpowiedz_claude = zapytaj_claude(tresc_pytania, system_prompt)
    return render_template(
        "index.html",
        odpowiedz=odpowiedz_claude,
        pytanie=tresc_pytania,
    )


if __name__ == "__main__":
    app.run(debug=True)
