# CSV Pivot Tool

## Description

This is a full-stack web app developed as a technical exercise. It allows the authenticated users upload two CSV files with a specific format. The app then combines and pivots this data, generating a downloadable summary file.


**Tech Stack:**
* **Backend:** Django (Python) with Pandas for data processing.
* **Frontend:** Vue.js
* **D.B.:** SQLite
* **WSGI Server:** Waitress
* **Environment:** Designed to run on Ubuntu 24.04 (Deployed via Docker).
* **Served at:** Port 8000

** NOTES ** 
   - Per exercise requirements no pip is used, all dependencies are retrieved using standard Ubuntu APT-GET
   - There are attached testing files in the repository, feel free to download them

## Installation Instructions (Docker - Recommended)

The repository includes a Dockerfile that helps with deployment, it also installs all necessary dependencies. After docker build there is a mid step that needs to be run manually to set up the DB and its superuser, after that all user management can be done via the web browser.

This method users Docker to encapsulate the App and its dependenciesm it assumes that Docker and Git are instaled in the hots machine.

**Prerequisites:**
* Git installed (`sudo apt update && sudo apt install -y git`)
* Docker Engine installed (Follow official Docker guide for Ubuntu: https://docs.docker.com/engine/install/ubuntu/)
* User added to the `docker` group or use `sudo` for Docker commands (as shown below).

On your terminal run the following commands (Note some of these commands might require superuser access or the sudo command):

**1. Clone the repository:**
   
   ```bash
   git clone https://github.com/rhergondev/csvtool_meaningful
   cd csvtool_meaningful
   ```

**2. Build the docker image:**

   ```bash
   docker build -t csv_pivot_tool .
   ```

**3. Run the Container for the first time:**

   ```bash
   docker run -d -p 8000:8000 --name csv_tool_app csv_pivot_tool
   ```

**4. With the container running setup the user DB and create a superuser:**
   * Access the container shell
   ```bash
   docker exec -it csv_tool_app bash
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

**5. You should now have access to the App on port 8000:**
   Visit http://localhost:8000

## Installation Instructions (Ubuntu - Local)

**Prerequisites:**
* Git installed (`sudo apt update && sudo apt install -y git`)

On your terminal run the following commands (Note some of these commands might require superuser access or the sudo command):

**1. Clone the repository:**
   
   ```bash
   git clone https://github.com/rhergondev/csvtool_meaningful
   cd csvtool_meaningful
   ```

**2. Install the first dependencies:**

   ```bash
   sudo apt-get update && sudo apt-get install -y --no-install-recommends \
    python3 \
    python-is-python3 \
    python3-django \
    python3-django-cors-headers \
    python3-pandas \
    python3-whitenoise \
    libjs-jquery \
    python3-waitress
   ```

**3. Add the necessary folders:**

   ```bash
   cd backend
   mkdir -p staticfiles temp_csv_files
   ```

**4. Generate the static files for django:**
   ```bash
   python3 manage.py collectstatic --noinput --clear
   ```

**5. Setup the user DB and create a superuser:**
   * Create the DB tables
   ```bash
   python3 manage.py migrate
   ```
   * Create a superuser
   ```bash
   python3 manage.py createsuperuser
   ```

**6. Serve the app on port 8000:**
   ```bash
   waitress-serve --host=0.0.0.0 --port=8000 csvtool_backend.wsgi:application
   ```

**7. You should now have access to the App on port 8000:**
   Visit http://localhost:8000
