import json
import os


def dodawanie_notatki(plik):
    nazwa_notatki = input("Podaj nazwę notatki: ")

    if os.path.exists(plik):
        with open(plik, "r", encoding="utf-8") as f:
            slownik_notatek = json.load(f)
    else:
        slownik_notatek = {}

    if nazwa_notatki in slownik_notatek.keys():
        print("Notatka o podanej nazwie już istnieje. Spróbuj ponownie.\n")
        return

    tresc_notatki = input("Podaj treść notatki: ")
    slownik_notatek[nazwa_notatki] = tresc_notatki

    with open(plik, "w", encoding="utf-8") as f:
        json.dump(slownik_notatek, f, ensure_ascii=False, indent=4)
        print(f"Notatka {nazwa_notatki} została zapisana prawidłowo\n")


def wyswietl_liste_notatek(plik):
    if os.path.exists(plik):
        with open(plik, "r", encoding="utf-8") as f:
            slownik_notatek = json.load(f)
    else:
        print("Brak notatek do wyświetlenia\n")
        return

    print("Lista notatek:")
    for klucz in slownik_notatek.keys():
        print(klucz)
    print("\n")


def otworz_notatke(plik):
    if os.path.exists(plik):
        with open(plik, "r", encoding="utf-8") as f:
            slownik_notatek = json.load(f)
    else:
        print("Brak notatek do wyświetlenia\n")
        return

    nazwa_notatki = input("Jaką notatkę chcesz przeczytać? ")
    if nazwa_notatki not in slownik_notatek.keys():
        print("Notatka o podanej nazwie nie istnieje. Spróbuj ponownie.\n")
    else:
        print(f"Nazwa notatki: {nazwa_notatki}\n"
              f"Treść: {slownik_notatek[nazwa_notatki]}\n")


def usun_notatke(plik):
    if os.path.exists(plik):
        with open(plik, "r", encoding="utf-8") as f:
            slownik_notatek = json.load(f)
    else:
        print("Brak notatek do usunięcia\n")
        return

    nazwa_notatki = input("Podaj nazwę notatki do usunięcia: ")
    if nazwa_notatki not in slownik_notatek.keys():
        print("Notatka o podanej nazwie nie istnieje. Spróbuj ponownie.\n")
    else:
        del slownik_notatek[nazwa_notatki]
        with open(plik, "w", encoding="utf-8") as f:
            json.dump(slownik_notatek, f, ensure_ascii=False, indent=4)
            print(f"Notatka {nazwa_notatki} została usunięta\n")


def main():
    czy_kontynuowac = True
    komunikat = "Nieprawdiłowy wybór. Spróbuj ponownie."
    print("Witaj w aplikacji Notatnik!")
    while czy_kontynuowac:
        print("Co chciałbyś/chciałabyś zrobić?\n"
              "1 - Dodaj notatkę\n"
              "2 - Wyświetl listę notatek\n"
              "3 - Otwórz notatkę\n"
              "4 - Usuń notatkę\n"
              "5 - Zakończ działanie programu\n")
        try:
            dzialanie = int(input())
        except ValueError:
            print(komunikat)
        else:
            plik = "notatnik.json"
            if dzialanie == 1:
                dodawanie_notatki(plik)
            elif dzialanie == 2:
                wyswietl_liste_notatek(plik)
            elif dzialanie == 3:
                otworz_notatke(plik)
            elif dzialanie == 4:
                usun_notatke(plik)
            elif dzialanie == 5:
                czy_kontynuowac = False
                print("Zakończono działanie programu")
            else:
                print(komunikat)


if __name__ == "__main__":
    main()
