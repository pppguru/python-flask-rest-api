# MYIX Rest API

Repository with all MYIX Rest API related code. Including database schema and sample data.


## Continuous integration

We are running Jenkins which will create an environment from scratch every time there is a commit to this repository. Within 5 minutes the new environment should be up and running on http://10.20.21.237 (make sure you are connected to the VPN).

## API Documentation

Documentation is regenerated after every commit and is available at http://10.20.21.237/apidoc/ (again VPN is needed).

## 1 - Running a local environment on FreeBSD

I recommend using a throwaway system in a vm or a jail.

Make sure that your locale is set to UTF-8. Similar as in the example below.
```shell
LANG=en_US.UTF-8
LC_CTYPE="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_ALL=
```

You can achieve that by editing *"/etc/login.conf"* and changing the last two lines of the first entry
```shell
default:\
        :passwd_format=sha512:\
        :copyright=/etc/COPYRIGHT:\
        :welcome=/etc/motd:\
        :setenv=MAIL=/var/mail/$,BLOCKSIZE=K:\
        :path=/sbin /bin /usr/sbin /usr/bin /usr/local/sbin /usr/local/bin ~/bin:\
        :nologin=/var/run/nologin:\
        :cputime=unlimited:\
        :datasize=unlimited:\
        :stacksize=unlimited:\
        :memorylocked=64K:\
        :memoryuse=unlimited:\
        :filesize=unlimited:\
        :coredumpsize=unlimited:\
        :openfiles=unlimited:\
        :maxproc=unlimited:\
        :sbsize=unlimited:\
        :vmemoryuse=unlimited:\
        :swapuse=unlimited:\
        :pseudoterminals=unlimited:\
        :kqueues=unlimited:\
        :umtxp=unlimited:\
        :priority=0:\
        :ignoretime@:\
        :umask=022:
```
to
```shell
default:\
        :passwd_format=sha512:\
        :copyright=/etc/COPYRIGHT:\
        :welcome=/etc/motd:\
        :setenv=MAIL=/var/mail/$,BLOCKSIZE=K:\
        :path=/sbin /bin /usr/sbin /usr/bin /usr/local/sbin /usr/local/bin ~/bin:\
        :nologin=/var/run/nologin:\
        :cputime=unlimited:\
        :datasize=unlimited:\
        :stacksize=unlimited:\
        :memorylocked=64K:\
        :memoryuse=unlimited:\
        :filesize=unlimited:\
        :coredumpsize=unlimited:\
        :openfiles=unlimited:\
        :maxproc=unlimited:\
        :sbsize=unlimited:\
        :vmemoryuse=unlimited:\
        :swapuse=unlimited:\
        :pseudoterminals=unlimited:\
        :kqueues=unlimited:\
        :umtxp=unlimited:\
        :priority=0:\
        :ignoretime@:\
        :umask=022:\
        :charset=UTF-8:\
        :lang=en_US.UTF-8:
```
then running
```shell
cap_mkdb /etc/login.conf
```
and reloging.

Now you can start with installing the needed packages.
```shell
pkg install mariadb102-client mariadb102-server git py36-pip curl zsh
```

Then you need to enable MariaDB to run as a service and run it.
```shell
sysrc mysql_enable="YES"
sysrc mysql_enable="YES"
```

Go ahead and secure the MariaDB installation *(in the example password **abcd1234** is used)*.
```shell
mysql_secure_installation
```
Use the following sequence to secure the installation.
*empty, y, abcd1234, abcd1234, y, y, y, y*

Now it is time to create a database and its user.
```shell
mysql -u root -pabcd1234 -e "create database myix;"
mysql -u root -pabcd1234 -e "grant all privileges on myix.* to myixuser@'%' identified by 'myixpassword';"
mysql -u root -pabcd1234 -e "FLUSH PRIVILEGES;"
```

Use pip which we installed earlier to install pipenv to manage virtual environments.
```shell
pip-3.6 install pipenv
```

Make sure that you are in the root's home directory and run.
```shell
git clone https://[USERNAME]@github.com/iXsystems/myix-rest-api.git
```

Insert the myix database schema and sample data.
```shell
mysql -u root -pabcd1234 myix < /root/myix/db/schema.sql
mysql -u root -pabcd1234 myix < /root/myix/db/data.sql
```

You should be ready to go with manually running the app by executing ***bootstrap.sh***, or you can continue and create a **myix** service in *"/etc/rc.d/"*
```shell
#!/bin/sh

# PROVIDE: myix

. /etc/rc.subr

name="myix"
rcvar=`set_rcvar`
start_cmd="myix_start"
stop_cmd="myix_stop"


load_rc_config $name

myix_start()
{
    if checkyesno ${rcvar}; then
      echo "Starting MyiX"
      touch /var/log/myix.log
      echo "Starting MyiX" >> /var/log/myix.log

      cd /root/myix
      export LC_ALL="en_US.UTF-8"
      export PATH=/usr/local/sbin:/usr/local/bin:/root/bin:$PATH

      /usr/local/bin/zsh /root/myix/bootstrap.sh >> /var/log/myix.log 2>&1 &
      sleep 3

      LINECOUNT="$(wc -l /var/log/myix.log | awk '{print $1}')"
      LASTSTARTLINE="$(grep -n "Starting MyiX" /var/log/myix.log | tail -1 | cut -d : -f 1)"

      tail -$(echo "$LINECOUNT - $LASTSTARTLINE" | bc) /var/log/myix.log
    fi
}

myix_stop()
{
    kill -TERM $(sockstat -l | grep :5000 | awk '{print $3}' | uniq)
    sleep 1
}

run_rc_command "$1"
```

Dont forget to make it executable.
```shell
chmod 555 myix
```

Start myix service.
```shell
service myix onestart
```

And test it.
```shell
curl localhost:5000
```

For debugging the logfile lives conveniently at *"/var/log/myix.log"*

## 2 -  Running a local environment using Pipenv
It is very useful to use the Pipenv in order to keep the project environment consistent.

### Install Pipenv
```shell
$ pip install pipenv
```

### Setup the virtualenv and install the dependencies
```shell
$ pipenv install
```

### Start the API
```shell
$ ./bootstrap.sh
```

### Add new package
```shell
$ pipenv install package-name
```

### Remove the package
```shell
$ pipenv uninstall package-name
```



## 3 - Generate Documentation

For generating and serving Documentation files on the local machine you need to install:
```shell
pkg install npm nginx
npm install apidoc -g
```

Generate Documentation.
```shell
apidoc -i /root/myix/myix_api -o /root/myix/myixapidoc/ -f ".*\\.py"
```

Edit Nginx conf file in *"/usr/local/etc/nginx/nginx.conf"* from
```shell
...
...
        location / {
            root   /usr/local/www/nginx;
...
...
```
to
```shell
...
...
        location / {
            root   /root/myix/myixapidoc;
...
...
```

Make sure that the conf file is correct.
```shell
nginx -t
```

Enable Nginx as service and start it.
```shell
sysrc nginx_enable="YES"
service nginx start
```

Test it.
```shell
curl localhost
```



