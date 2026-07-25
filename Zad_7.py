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
MAX_TOKENS = 200

CENA_INPUT_ZA_MILION = 3.0
CENA_OUTPUT_ZA_MILION = 15.0

historia = []


def wybierz_osobowosc():
    """Pyta użytkownika, jaką osobowość ma mieć bot, i zwraca system prompt."""
    print("Wybierz bota:")
    print(" 1) Poważny asystent")
    print(" 2) Zabawny kompan")
    print(" 3) Sarkastyczny korepetytor")
    print(" 4) Romantyczny poeta")

    wybor = input("Twój wybór (1/2/3/4): ").strip()

    if wybor == "1":
        return "Jesteś rzeczowym, formalnym asystentem. Odpowiadasz precyzyjnie i konkretnie."
    elif wybor == "2":
        return "Jesteś wesołym, energicznym asystentem, który uwielbia żarty i emotikony."
    elif wybor == "3":
        return "Jesteś sarkastycznym korepetytorem z ciętym językiem, ale zawsze pomagasz merytorycznie."
    elif wybor == "4":
        return "Jesteś romantycznym poetą, który lubi rymy, metafory i tym podobne ozdobniki."
    else:
        print("Nie rozpoznano żadnej osobowości - używam domyślnej, poważnej osobowości.\n")
        return "Jesteś rzeczowym, formalnym asystentem."


def zapytaj_claude(tresc_pytania, system_prompt):
    """Wysyła pytanie do modelu Claude razem z całą dotychczasową historią i zwraca odpowiedź."""
    historia.append({"role": "user", "content": tresc_pytania})

    try:
        odpowiedz = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=historia
        )

        tekst_odpowiedzi = odpowiedz.content[0].text
        historia.append({"role": "assistant", "content": tekst_odpowiedzi})
        return tekst_odpowiedzi

    except AuthenticationError:
        historia.pop()
        return "BŁĄD: nieprawidłowy klucz API. Sprawdź plik .env.", None

    except RateLimitError:
        historia.pop()
        return "BŁĄD: zbyt wiele zapytań w krótkim czasie. Poczekaj chwilę i spróbuj ponownie.", None

    except APIConnectionError:
        historia.pop()
        return "BŁĄD: problem z połączeniem internetowym. Sprawdź sieć i spróbuj ponownie.", None

    except APIError as blad:
        historia.pop()
        return f"BŁĄD: coś poszło nie tak po stronie serwera ({blad}).", None


def zapisz_rozmowe_do_pliku(nazwa_pliku="rozmowa.txt"):
    """Zapisuje całą historię rozmowy do pliku tekstowego."""
    with open(nazwa_pliku, "w", encoding="utf-8") as plik:
        for wpis in historia:
            kto = "Ty" if wpis["role"] == "user" else "Claude"
            plik.write(f"{kto}: {wpis['content']}\n\n")


def main():
    print("=" * 50)
    print(" CHATBOT AI — wpisz 'quit', żeby zakończyć lub 'menu', żeby zmienia bota")
    print("=" * 50)
    print()
    system_prompt = wybierz_osobowosc()
    licznik_zapytan = 0

    while True:
        pytanie_uzytkownika = input("\nTy: ").strip()

        # Warunek zakończenia — sprawdzany jako pierwszy
        if pytanie_uzytkownika.lower() == "quit":
            print(f"\nDo zobaczenia! \nLiczba wykonanych zapytań: {licznik_zapytan}. ")
            zapisz_rozmowe_do_pliku("zapis_rozmowy.txt")
            print("Rozmowa została zapisana do pliku rozmowa.txt.")
            break

        if pytanie_uzytkownika.lower() == "menu":
            print()
            system_prompt = wybierz_osobowosc()
            continue

        # Walidacja pustego pola — pomijamy ten przebieg, nie kończymy programu
        if pytanie_uzytkownika.strip() == "":
            print("Wpisz najpierw jakieś pytanie!")
            continue

        # Właściwe zapytanie do Claude'a
        odpowiedz = zapytaj_claude(pytanie_uzytkownika, system_prompt)
        print("\nClaude: ", odpowiedz)
        licznik_zapytan += 1


if __name__ == "__main__":
    main()
