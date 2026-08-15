from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import pandas as pd
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
ROZSZERZENIA_DOZWOLONE = {".csv", ".xlsx"}

app = Flask(__name__)


def zapytaj_claude(tresc_pytania):
    try:
        odpowiedz = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
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


@app.route("/")
def strona_glowna():
    return render_template("index.html", odpowiedz=None)


@app.route("/zapytaj", methods=["POST"])
def zapytaj():
    tresc_pytania = request.form.get("pytanie", "").strip()

    if tresc_pytania == "":
        return render_template(
            "index.html",
            odpowiedz="Wpisz najpierw jakieś pytanie!",
        )

    odpowiedz_claude = zapytaj_claude(tresc_pytania)
    return render_template("index.html", odpowiedz=odpowiedz_claude, pytanie=tresc_pytania)


@app.route("/analiza-strona")
def analiza_strona():
    return render_template("analiza.html")


@app.route("/analizuj", methods=["POST"])
def analizuj():
    plik = request.files.get("plik")

    if not plik or plik.filename == "":
        return render_template("analiza.html", blad="Nie wybrano pliku. Spróbuj ponownie.")

    rozszerzenie = os.path.splitext(plik.filename)[1]
    if rozszerzenie not in ROZSZERZENIA_DOZWOLONE:
        return render_template("analiza.html", blad=f"Błędny format pliku. Prześlij plik w jednym z formatów: {', '.join(str(x) for x in ROZSZERZENIA_DOZWOLONE)}")

    try:
        if rozszerzenie == ".csv":
            df = pd.read_csv(plik.stream)
        else:
            df = pd.read_excel(plik.stream)
    except Exception as e:
        return render_template("analiza.html", blad=f"Nie udało się wczytać pliku: {e}")

    liczba_wierszy, liczba_kolumn = df.shape
    podglad = df.head(5).to_string(index=False)
    kolumny = ", ".join(df.columns.tolist())
    prompt = f"""Mam plik CSV lub XLSX z danymi. Oto podstawowe informacje:
- Liczba wierszy: {liczba_wierszy}
- Liczba kolumn: {liczba_kolumn}
- Nazwy kolumn: {kolumny}
- Pierwsze 5 wierszy:
{podglad}

Napisz krótkie podsumowanie tych danych po polsku. Co to może
być za zbiór danych? Co można z niego wyczytać?"""

    podsumowanie = zapytaj_claude(prompt)

    return render_template(
        "analiza.html",
        nazwa_pliku=plik.filename,
        liczba_wierszy=liczba_wierszy,
        liczba_kolumn=liczba_kolumn,
        podsumowanie_ai=podsumowanie,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
