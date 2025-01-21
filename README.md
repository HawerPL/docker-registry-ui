# Docker Registry UI

---
<b>Prosta aplikacja umożliwiająca logowanie się do wielu rejestrów Dockera. Projekt powstał jako praca inżynierska pod 
tytułem <i> Projekt i implementacja interfejsu graficznego aplikacji webowej do przeglądania i zarządzania rejestrem 
Dockera wraz z wdrożeniem. Głównym założeniem była sama aplikacja, dlatego testy automatyczne nie są rozbudowane.</i>
</b>

## Spis treści
* [Podstawowe informacje](#podstawowe-informacje)
* [Technologie](#technologie)
* [Instalacja](#instalacja)
* [Konfiguracja](#konfiguracja)
* [Uruchomienie](#uruchomienie)

## Podstawowe informacje

---
Celem aplikacji jest umożliwienie użytkownikom w prosty sposób wydobyć informacje z rejestru Dockera za pomocą interfesju graficznego.
Aplikacja daje dostęp do wielu rejestrów korzystających z uwierzytelniania Basic Auth.

## Technologie

---
Projekt został zrealizowany z użyciem techonologii:
* Flask
* Jinja2
* Bootstrap 5
* Babel
* Docker
* pytest

## Budowa obrazu

---
Do zbudowania obrazu Dockera można skorzystać z komend:

Linux
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ docker compose build
```

Windows
```
$ python3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ docker compose build
```
---

## Konfiguracja

---

| Environment                      | Description                                                                                            | Default value      |
|----------------------------------|--------------------------------------------------------------------------------------------------------|--------------------|
| APP_NAME                         | Nazwa aplikacja, która ma być widoczna w interfejsie użytkownika                                       | Docker Registry UI |
| DEFAULT_LOCALE                   | Domyślny język aplikacji                                                                               | pl                 |
| DOCKER_REGISTRY_URL_X            | Adres URL rejestru X                                                                                   |                    |
| DOCKER_REGISTRY_NAME_X           | Nazwa rejestru X                                                                                       |                    |
| DOCKER_REGISTRY_IS_DELETABLE_X   | Definuje czy w rejestrze X jest możliwe usuwanie obiektów                                              |                    |
| DOCKER_REGISTRY_LOGIN_X          | Nazwa użytkownika rejestru X                                                                           |                    |
| DOCKER_REGISTRY_PASSWORD_X       | Hasło dla podanego użytkownika rejestru X                                                              |                    |
| ENABLED_LOGO                     | Włączenie loga aplikacji <br/> ```docker run -it -v /path/to/logo:/app/static/logo.png image:latest``` | False              |
| SESSION_TIME                     | Czas trwania sesji dla zalogowanego użytkownika                                                        | 60                 |
| SUPER_USER_ENABLED               | Włączenie super użytkownika - posiadający dostęp do wszystkich rejestrów                               | True               |
| SUPER_USER_LOGIN                 | Nazwa super użytkownika                                                                                | -                  |
| SUPER_USER_PASSWORD              | Hasło dla super użytkownika                                                                            | -                  |
| LOG_LEVEL                        | Poziom logowania aplikacji                                                                             | INFO               |
| ENABLED_AUTH                     | Włącza autoryzację w aplikacji                                                                         | True               |
| COUNT_TAGS                       | Włącza wyświetlanie ilości tagów obrazu                                                                | False              |
| PAGINATION_FOR_REQUEST_CATALOG   | Jaka wartość paginacji ma zostać użyta w zapytaniach do rejestru w celu uzyskania repozytoriów         | 1000               |
| PAGINATION_FOR_REQUEST_TAGS_LIST | Jaka wartość paginacji ma zostać użyta w zapytaniach do rejestru w celu uzyskania tagów                | 1000               |
| MINIMAL_REPOSITORY_INFO          | Włącza wyświetlanie tylko nazwy tagu i repozytorium przy jego informacjach w zakładce repozytoriów     | True               |


## Uruchomienie

Aplikację można uruchomić bezpośrednio narzędziem docker compose po zbudowaniu paczki wg wcześniejszej instrukcji: 
```
$ docker compose up -d
```

Adres domyślny do uruchomienia w przeglądarce: http://127.0.0.1:5555/

## Przegląd aplikacji
### Logowanie (dwa motwywy)

![alt text](https://github.com/HawerPL/docker-registry-ui/blob/main/assets/Docker%20Registry%20UI.png)
### Przegląd rejestru
![alt text](https://github.com/HawerPL/docker-registry-ui/blob/main/assets/Docker%20Registry%20UI%201.png)
### Przegląd repozytorium
![alt text](https://github.com/HawerPL/docker-registry-ui/blob/main/assets/Docker%20Registry%20UI%203.png)
### Szczegóły obrazu
![alt text](https://github.com/HawerPL/docker-registry-ui/blob/main/assets/Docker%20Registry%20UI%202.png)
