# Shotgun

## Prerequisites

Before starting, we need to install the required system packages. On Ubuntu
we need to run the following commands.
```
sudo apt install python3 python3-pip python3-venv
sudo apt install mariadb-server libmysqlclient-dev
sudo mysql_secure_installation
```

To setup the database, use the MySQL command line to execute the provided SQL
scripts.
```
mysql
MariaDB [(none)]> source dbSetup/dbDump-28-12-20.sql;
MariaDB [(none)]> source dbSetup/Users.sql;
```

If MariaDB is not running, you can start it with the command
`sudo systemctl start mariadb`.

## Development

The following commands will create a virtual environment and will install the
required Python dependencies.
```
# Create a new virtualenv
python3 -m venv shotgunenv

# Activate the virtualenv
source shotgunenv/bin/activate

# Install dependencies
pip3 install wheel
pip3 install -r requirements.txt
```

To start the development server, activate the virtual environment and run
```
export FLASK_APP=shotgun.py
flask run
```
You can access the application at http://127.0.0.1:5000/.
