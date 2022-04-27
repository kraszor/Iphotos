# PAP21L-Z01

## Prototyp

### Uruchomienie

W celu uruchomienia prototypu aplikacji należy wejść w poniższy link:<br>
https://iphotos-pap.herokuapp.com<br>

### Sposób wykonania deploy'a

Prototyp aplikacji został postawiony na platformie churowej [Heroku](https://www.heroku.com). <br>

Przed udostępnieniem aplikacji należało stworzyć plik requirements.txt zawierający potrzebne biblioteki. <br>
    `pip freeze > requirements.txt` (w wirtualnym środowisku) <br>
Jako, że Herku wspiera Django, mogłem skorzystać z biblioteki django-heroku, skorzystałem również z gunicorna, dj-database-url oraz django-environ.<br>
Django-environ pozwoliło mi stowrzyć część zmiennych w ustawieniach jako zmienne środowiskowe, przez co w kodzie nie są widoczne takie elementy jak na przykład secret_key albo hasło do poczty mailowej.<br>
Gunicorn jest serwerem WWW możliwym do wykorzystania produkcyjnie. Jego wdrożenie zawarte jest w pliku Procfile.<br>
Django-heroku zawiera w sobie m.in takie pakiety jak whitenoise czy psycopg2. Pierwszy z nich pozwala na udostępnianie plików statycznych (Js, HTML, CSS) na serwer protokołem HTTP, natomiast drugi pozwala na obsługę PostgreSQL, ponieważ on jest używany na Heroku (W wersji lokalnej, bazowo w django używa się SQLite). <br>
Dj-database-url pozwala stworzyć odpowiednią konifgurację bazy danych na serwerze odpowiadającą tej lokalnej. <br>

Po odpowiednich konfiguracjach i zmianach w pliku settings.py należało w terminalu zalogować się do heroku: <br>
`heroku login`<br>   
Należy wtedy wcisnąć dowolny klawisz i zostaniemy przeniesieni na stronę heroku w celu zalogowania. <br>
Po zalogowaniu możemy stworzyć naszą aplikację w heroku:<br>
`heroku create <nazwa_aplikacji>`<br>
Po stowrzeniu aplikacji możemy zainicializować repozytorium lokale, dodać do niego potrzebne pliki aplikacji, zrobić commit i wrzucić do heroku.<br>
`git init`<br>
`git add .`<br>
`git commit -m <nazwa>`<br>
`git push heroku master`<br>
Heroku stworzy na podstawie naszych plików aplikacjie, jeżeli nie napotka błędów wygeneruje się link dizęki, któremu możemy z niej korzystać. Zarządzać aplikacją np. jej zmeinnymi środowiskowymi możemy w panelu na stronie internetowej lub poprzez terminal.




