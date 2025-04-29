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

On your terminal run the following commands:

**1. Clone the repository:**
   
   ```bash
   git clone https://github.com/rhergondev/csvtool_meaningful
   cd csvtool_meaningful>
   ```

**2. Build the docker image

   ```bash
   docker build -t csv_pivot_tool .
   ```

**3. Run the Container for the first time

   ```bash
   docker run -d -p 8000:8000 --name csv_tool_app csv_pivot_tool
   ```

**4. With the container running setup the user DB and create a superuser
   * Access the container shell
   ```bash
   docker exec -it csv_tool_app bash
   ```
   * Access the backend directory
   ```bash
   cd /app/backend
   ```
   * Create the DB tables
   ```bash
   python3 manage.py migrate
   ```
   * Create a superuser
   ```bash
   python3 manage.py createsuperuser
   ```
   * Exit the shell
   ```bash
   exit
   ```

**5. You should now have access to the App on port 8000
   Visit http://localhost:8000
