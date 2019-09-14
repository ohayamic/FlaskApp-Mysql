# FlaskApp-Mysql
Flask is a free and open source micro web framework for Python designed to help developers build secure, scalable and maintainable web applications. Flask is based on Werkzeug and uses Jinja2 as a template engine.

## How to run the application
Initially the application will crash because most of the imported application needed for it to run are not installed yet. To rectify this on ubuntu system the following application needs to be installed and the required tables created. 
Since this is a small application, the use of virtuall environment was not necessary. Below are the list of application that should be installed for the application to work.

### step 1 : Install necessary applications

* mkdir my_flask_app
* cd my_flask_app
* pip install Flask
* Mysql 

For an indepth guy on how to install mysql on ubuntu, follow these staps [How To Install MySQL on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04).


### step 2: Create the database
- Login to mysql 
* mysql -u root -p it will prompt you for a password as given here: ** Enter password:****** **
- Once logged in, it is adviceable to create your own database

In other to get started with this application, you will have to download it using these commands:
- git clone https://github.com/ohayamic/FlaskApp-Mysql.git
- cd "project name"
- python app.py

