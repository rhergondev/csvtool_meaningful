# CSV Pivot Tool

## Desciption

This is a full-stack web app developed as a technical exercise. It allows the authenticated users upload two CSV files with a specific format. The app then combines and pivots this data, generating a downloadable summary file.


**Tech Stack:**
* **Backend:** Django (Python) with Pandas for data processing.
* **Frontend:** Vue.js
* **D.B.:** SQLite
* **WSGI Server:** Waitress
* **Environment:** Designed to run on Ubuntu 24.04 (Deployed via Docker).
* **Served at:** Port 8000

** NOTES ** - Per exercise requirements no pip is used, all dependencies are retrieved using standard Ubuntu APT-GET

## Instalation instruction (Docker - Recommended)

The repository includes a Dockerfile that helps with deployement, it also installs all necesary dependencies. After docker build there is a mid step that needs to be runned manually to set up the DB and its superuser, after that all user management can be done via the web browser.

Este método utiliza Docker para encapsular la aplicación y sus dependencias, asegurando un entorno consistente. Se asume que Docker y Git están instalados en la máquina host (Ubuntu 24.04).

**1. Clone the repository:**

   On your terminal run the following commands:
   ```bash
   [git clone <URL_DE_TU_REPOSITORIO_GITHUB>](https://github.com/rhergondev/csvtool_meaningful)
   cd csvtool_meaningful>
