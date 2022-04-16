# Darribny
Darribny is a platform where trainers can connect with trainees. As a trainee, you can request a training session. When a nearby trainer accepts your request, the app displays the reservation time and location.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **Flask-Script** to provide support for writing external scripts in Flask
* **Flask-Login** to be our user session management library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 4] for our website's frontend

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory of this project and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python app.py
```