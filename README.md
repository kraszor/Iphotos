# PAP21L-Z01

## Zespół Z01

- Igor Kraszewski
- Krystian Grela
- Mateusz Gurdała

## Tematyka

Desktopowa przeglądarka graficzna z możliwością tagowania zdjęć oraz tworzenia prywatnych grup ze zdjęciami tylko dla wybranych użytkowników.<br/> Do tworzenia kont, zarządzania nimi oraz zarządzania grupami służy aplikacja webowa.

## Technologie

- .NET/WPF
- Python/Django
- CSS/HTML/JS
- SQLite
- RestAPI
- Baza postgreSQL stworzona na Heroku

## Możliwości

- Pobieranie aplikacji desktopowej ze strony internetowej
- Udostępnianie zdjęć między użytkownikami
- Grupowanie i tagowanie zdjęć, powiązana z tym wyszukiwarka
- Tworzenie grup, dodwania do nich zdjęć i użytkowników (Albumy online)
- Aplikacja desktopowa zgodna z konwencją MVVM, a webowa z konwecją MVT

### Diagram Warstw
![Screenshot](images/DiagramWarstw.png)

### Relacje encji w bazie danych SQLite

![Screenshot](images/Diagram_.png)

## Aplikacja desktopowa

### Uruchomienie

Do działania aplikacji wymagane są następujące Nuget Packages:
- Microsoft.EntityFrameworkCore 6.0.4
- Microsoft.EntityFrameworkCore.Sqlite 6.0.4
- Microsoft.EntityFrameworkCore.Tools 6.0.4
- Microsoft.Xaml.Behaviors.Wpf 1.1.39
- GMap.NET.Core
- GMap.NET.WinPresentation
- Google.Apis.Drive.v3

Aplikacje można włączyć za pomomocą pliku .exe znajdującego się pod podaną ścieżką repozytorium:
iPhoto\bin\Debug\net6.0-windows\iPhoto.exe

### Podstawowe Funkcjonalności Aplikacji desktopowej

Program dzieli się na podstrony oznaczone odpowiednimi ikonami:

- Strona startowa - strona zawierająca ...

- Albumy - strona zawierająca listę albumów, użytkownik może dodawać albumy z wybraną przez
        siebie nazwą i kolorem. Albumy można edytować i usuwać po utworzeniu. Album wyświetla
        informacje o ilości zdjęć, rozmiarze i hashtagach jakie posiadają zdjęcia wewnątrz albumu.
        Zawartość albumu posiada taką samą funkcjonalność jak wyszukiwarka zdjęć opisania poniżej
        z tą różnicą że wyszukiwanie występuje w obrębie albumu.

- Wyszukiwarka zdjęć - główny element naszej aplikacji desktopowej. Odpowiada za CRUD zdjęć.
        Do dodania zdjęć do lokalnej bazy danych służy przycisk kartki z plusem
        znajdująca się w prawym górnym rogu ekranu. W celu wypisania wszystkich zdjęć
        należy w polu *Title wpisać %ALL i nacisnąć przyicsk lupy powyżej.
        Powiekszyć zdjęcie można poprzez podwójne naciśnięcie na zdjęcie.
        Po kliknięciu przycisku listy w prawym górnym rogu i wybraniu zdjęcia jest możliwość
        sprawdzenia szczegółów zdjęcia. Kliknięcie prawym przyciskiem na zdjęcie umożliwia
        zmianę szczegółów zdjęcia lub jego usunięcie. Z prawej strony można rozwinąć panel odpowiedzialny
        za informowanie użytkownika o szczegółach zdjęcia.

- Miejsca - zawiera mapę na której można tworzyć miejsca w których zostały utworzone miejsca. Każde miejsce
        posiada informacje o ilości zdjęć tam wykonanych. Zmianę widoku z dodawania miejsc do listy miejsc
        można wykonać za pomocą przycisku strzałki w górnej części aplikacji.


- Profil - Zawiera informacje o części online naszej aplikacji. Posiada informacje o albumach stworzonych
        online dla grup użytkowników. Umożliwia też przeniesienie na stronę rejestracji w webowej części
        aplikacji.
  
## Prezentacja

### Aplikacja desktopowa

![Screenshot](images/prototipe1.png)
![Screenshot](images/prototipe2.png)
![Screenshot](images/prototipe3.png)
![Screenshot](images/prototipe4.png)

### Aplikacja webowa

![Screenshot](images/275003850_697706734911582_2164206151481655743_n.png)
![Screenshot](images/275350178_246071544326431_271352954379807537_n.png)
![Screenshot](images/275482231_690834268895824_6326811759053373111_n.png)
![Screenshot](images/275645700_371907327939747_3411847957607684256_n.png)
![Screenshot](images/276172909_384364279913047_7058174483221134755_n.png)
