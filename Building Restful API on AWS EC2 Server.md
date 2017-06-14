# Building Restful APIs on AWS for Everyone

## Menu
- Definition of REST
- Software Architecture
- Hardware Architecture
- Set up a AWS EC2 server and install softwares
- REST API Development
  - Toy code examples
  - Example of a machine learning API service
- Notes

## Acknowledge 

At here, I would like to thank Prof. Tian Jie for allowing me to register a direct study with him and suggesting me to create web services on AWS. I explored and learned so much in this journey. I would also like to thank people that contributed their knowledge and time on the Internet for the public. I cannot know all of these and finish this tutorial without their efforts on stackoverflow, blogs and any development community.     ---- Jun.13, 2017

## Words ahead

###Thank you for reading this tutorial. When I read tech tutorials, I wished authors could explain each step as detailed as possible. Therefore, when I wrote this, a lot of details, even how I fixed some bugs I met, were included. I hope the readers can understand how to do it and theories that I understood. Moreover, this is also a archive for a direct study of mine, Yujie Wang, at Clark University. 

###If you have any suggestion for me, please leave me an message or create an issue on [the Github repository](https://github.com/eugeneYWang/RestAPI_flask) of this tutorial. 

###If this is useful to you, please <font color =red>like and spread out </font>a link of this article, so this article is more likely seen by someone who need this and I can more opinions about this topic. If you like my works, I might share more tutorials about using AWS EC2.

### There are my contact info: [Github](https://github.com/eugeneYWang/RestAPI_flask), [LinkedIn](http://linkedin.com/in/yujie-wang-61a129a0).

If you know someone or any company would be interested to hire people with geospatial and development background, please let me know. Thank you!

## Definition of REST API

> Representational state transfer (REST) or RESTful Web services are one way of providing interoperability between computer systems on the Internet. REST-compliant Web services allow requesting systems to access and manipulate textual representations of Web resources using a uniform and predefined set of stateless operations. Other forms of Web service exist, which expose their own arbitrary sets of operations such as WSDL and SOAP."Web resources" were first defined on the World Wide Web as documents or files identified by their URLs, but today they have a much more generic and abstract definition encompassing every thing or entity that can be identified, named, addressed or handled, in any way whatsoever, on the Web. In a RESTful Web service, requests made to a resource's URI will elicit a response that may be in XML, HTML, JSON or some other defined format. The response may confirm that some alteration has been made to the stored resource, and it may provide hypertext links to other related resources or collections of resources. Using HTTP, as is most common, the kind of operations available include those predefined by the HTTP verbs GET, POST, PUT, DELETE and so on. By making use of a stateless protocol and standard operations, REST systems aim for fast performance, reliability, and the ability to grow, by re-using components that can be managed and updated without affecting the system as a whole, even while it is running.

from [WIKI](https://en.wikipedia.org/wiki/Representational_state_transfer)

> API consumers are capable of sending GET, POST, PUT, and DELETE verbs, which greatly enhance the clarity of a given request.
Generally, the four primary HTTP verbs are used as follows:

	GET
		Read a specific resource (by an identifier) or a collection of resources.
	PUT
		Update a specific resource (by an identifier) or a collection of resources. 
		Can also be used to create a specific resource if the resource identifier is know before-hand.
	DELETE
		Remove/delete a specific resource by an identifier.
	POST
		Create a new resource. Also a catch-all verb for operations that don't fit into the other categories.
> Note :
GET requests must not change any underlying resource data. Measurements and tracking which update data may still occur, but the resource data identified by the URI should not change.

From [Rest API Tutorial](http://www.restapitutorial.com/lessons/restquicktips.html)

## Software Architecture
![](https://www.fullstackpython.com/img/visuals/web-browser-server-wsgi.png)

**Web Server** : Nginx

**WSGI Server** : GUnicorn

**Python Framework** : Flask

**Database for Python REST API**: PostgreSQL (optional)

**Other software(s)** : Supervisor

### Reasons to design architecture
#### Nginx

Being used as a web server to communicate between the web request and WSGI server.
> I personally use Nginx more frequently than Apache because Nginx's configuration feel easier to write, with less boilerplate than alternatives.
There's also a bit of laziness in the usage: Nginx works well, it never causes me problems. So I stick with my battle-tested Ansible configuration management files that set up Nginx with HTTPS and SSL/TLS certificates

[Reference](http://www.fullstackpython.com/nginx.html)

#### GUnicorn

A Web Server Gateway Interface (WSGI) server implements the web server side of the WSGI interface for running Python web applications.

![](https://www.fullstackpython.com/img/visuals/wsgi-interface.png)
As shown in the above diagram, a WSGI server simply invokes a callable object on the WSGI application as defined by the PEP 3333 standard.

> A traditional web server does not understand or have any way to run Python applications. A Web Server Gateway Interface (WSGI) server implements the web server side of the WSGI interface for running Python web applications.
			
> Pick a WSGI server based on available documentation and tutorials. Green Unicorn is a good one to start with since it's been around for awhile.

[Reference](http://www.fullstackpython.com/wsgi-servers.html)

#### Flask
Flask is a Python web framework built with a small core and easy-to-extend philosophy.
![](https://www.fullstackpython.com/img/logos/flask.jpg)

Flask is considered more Pythonic than Django because Flask web application code is in most cases more explicit. [Reference](http://www.fullstackpython.com/flask.html)

#####Compare Flask to Django
1. ***Flask > Django for APIs***. For example, a nested api resource in Flask is @app.route('/users/<string:user_id>/teams/<string:team_id>', methods=['GET', 'POST']) while with Django REST framework this is impossible. (drf-nested-routers helps but breaks unless you use only the most basic Django REST framework features.
2. 	Will not primarily have dynamic HTML pages. This is the opposite of an API heavy site. Django makes building HTML websites easier.
3. Need external library to use SQL database. Most people use SQLAlchemy with Flask, which is powerful but not as easy to use as Django's ORM. Complicated SQL queries are a piece of cake with Django's built-in ORM.

#####Summary of the comparison
Flask is great for developers working on small projects that need a fast way to make a **simple, Python-powered** web site. It powers loads of small one-off tools, or simple web interfaces built over existing APIs. Backend projects that need a simple web interface that is fast to develop and will require little configuration often benefit from Flask on the frontend, like jitviewer which provides a web interface for inspecting PyPy just-in-time compiler logs.
				
By far the most popular framework is Django, and the list of sites that use it is impressive. Bitbucket, Pinterest, Instagram, and The Onion use Django for all or part of their sites. For sites that have common requirements, Django chooses very sane defaults and because of this it has become a popular choice for mid- to large-sized web applications.

#### Choice of Database(just FYI) : PostgreSQL

PostgreSQL is the default database choice for many Python developers, including the Django team when testing the Django ORM. PostgreSQL is often viewed as more feature robust and stable when compared to MySQL, SQLServer and Oracle. All of those databases are reasonable choices. However, because PostgreSQL tends to be used by Python developers the drivers and example code for using the database tend to be better documented and contain fewer bugs for typical usage scenarios. If you try to use an Oracle database with Django, you'll see there is far less example code for that setup compared to PostgreSQL backend setups.

## Server Architecture
**Computation**: CPU of AWS EC2 Instance (In this case, t2-micro instance is used because of free-tier's limit.)

**Storage**: Amazon EBS, SSD.(In this case, storage is only extended to 30G because of free-tier's limit) 

**System**: Amazon Image (AMI), modified Red hat distribution of Linux

This Restful API was designed to implement on AWS. For the following reasons:

- Server on AWS will be secured by Amazon.
- Linux system is ready to use.
- No need to set up public domain.
- A lot of resources are available,  even you are a free-tier user. At least the first year, most services are available to free-tier users.


## Set up a AWS EC2 server and install softwares

- Follow [this tutorial](https://aws.amazon.com/getting-started/tutorials/launch-a-virtual-machine/?nc1=h_ls) to establish your EC2 instance running AMI Linux, and keep logging in the remote system.

- install softwares

```
$ sudo yum install git nginx
$ sudo pip install supervisor
// make sure python27-devel, 
// python27-virtualenv, python27-pip is installed
```

- As for the python packages we’ll need to create and virtual environment and install all of our packages once it is activated. We can do this via the following code:

```
$ mkdir ~/.virtualenvs 
$ cd ~/.virtualenvs
$ virtualenv flaskdeploy  //create a virtual environment
$ source ~/.virtualenvs/flaskdeploy/bin/activate 
```

- Next step is to get test code from GitHub by cloning the repository and installing the necessary packages via git with our virtual environment activated (which we just did).

	Again, this ```(flaskdeploy)``` indicates whatever command entered in the same line with it will be executed with this individual python environment using packages available in this environment.

```
(flaskdeploy)$ mkdir ~/sites && cd ~/sites
(flaskdeploy)$ git clone https://github.com/alexandersimoes/flaskdeploy.git
(flaskdeploy)$ cd flaskdeploy
(flaskdeploy)$ pip install -r requirements.txt
```
### Install and configure Nginx

For our next trick we’ll be configuring Nginx to work with our setup. We use Nginx as our routing manager, serving static files and reverse proxying to Gunicorn for our Flask views.

We will make sure port 80 has been opened.

- Visit [AWS console](https://console.aws.amazon.com/console/home) and log in your AWS account.
- Click Instances on the left panel, and check the security group.
- Click that group or click **Security Groups** on the left panel  
- highlight that group being used by our instance, click its **inbound** tag and click **Edit** button.
- Click **Add Rule** button.
- Choose the new rule to be HTTP type, Port as 80, and leave Source there.
- Click **Save**

- And then, start nginx service.

```
(flaskdeploy)$ sudo service nginx restart
```
Now, the default welcome page of nginx should be available as the front page in our public domain for the running server instance, which you can obtain from the info panel of AWS console. If you found the public domain of your running server on AWS console, you can use web browser to visit it. A welcome page from Nginx should be opened.

![](http://tomroy.github.io/uploads/NginxWelcomePage.png)

Now, we have tested the functionality of Nginx. It is time to let it do something more than directing to the welcome page. **We need to customize the configuration file in it.**

- Open the default configuration file. 

  *If you are new to nano, the text editor, here is [a how-to documentation](https://www.howtogeek.com/howto/42980/the-beginners-guide-to-nano-the-linux-command-line-text-editor/) to help you.*

```
(flaskdeploy)$ sudo nano /etc/nginx/nginx.conf
```

- Delete the **Server block** in the default configuration file because we will refer external modular configuration files from a specific folder instead of keep editing this default file. **Server block** is a section that starts with the word **Server**, continues with a ```{``` and ends with a ```}```.

-  Include a line in **HTTP block**.

```
include /etc/nginx/sites-enabled/*
```
Eventually, the default configuration will look like this.

```
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2 default_server;
#        listen       [::]:443 ssl http2 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        # It is *strongly* recommended to generate unique DH parameters
#        # Generate them with: openssl dhparam -out /etc/pki/nginx/dhparams.pem 2048
#        #ssl_dhparam "/etc/pki/nginx/dhparams.pem";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
#        ssl_ciphers HIGH:SEED:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!RSAPSK:!aDH:!aECDH:!EDH-DSS-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA:!SRP;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}
```

- Save the file. Click ```Ctrl``` +  ```X``` to exit nano and save the file.

#### Create modular configuration files

If you would like to know more details about configuring NginX. This article will be helpful: [
How to Configure nginx](https://www.linode.com/docs/websites/nginx/how-to-configure-nginx).

- create folders to place modular configuration files.

```
(flaskdeploy)$ sudo mkdir /etc/nginx/sites-available
(flaskdeploy)$ sudo mkdir /etc/nginx/sites-enabled
```
*Names of these two folders follow the convention of NginX in Ubuntu. Installed in Ubuntu, NginX have these two folders automatically so it knows where to find modular configuration files. However, NginX does not follow this convention when it was installed in AMI or Red hat, so we add such two folders and a rule in the default configuration file to follow this convention.*

- create a modular configuration file **flaskdeploy**

```
(flaskdeploy)$ sudo nano /etc/nginx/sites-available/flaskdeploy
```

- Add these into the content of **flaskdeploy**, then save this file.

<font color=red>!! Replace ```default_server``` into your public domain</font>

```
server {
    listen 80 default_server;
    # listen [::]:80 default_server;  
    server_name localhost;

    root /home/ec2-user/sites/flaskdeploy;

    access_log /home/ec2-user/sites/flaskdeploy/logs/nginx/access.log;
    error_log /home/ec2-user/sites/flaskdeploy/logs/nginx/error.log;

    location / {
        proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
        }
    }

    location /static {
        alias  /home/ec2-user/sites/flaskdeploy/static/;
        autoindex on;
    }
}
```

- symlike this file to sites-enabled

```
(flaskdeploy)$ sudo ln -s /etc/nginx/sites-available/flaskdeploy /etc/nginx/sites-enabled/
```
- create the directory for our nginx logs, test our configuration and restart to allow our changes to take place.

```
(flaskdeploy)$ mkdir -p ~/sites/flaskdeploy/logs/nginx
(flaskdeploy)$ sudo nginx -t 
(flaskdeploy)$ sudo service nginx restart
```

- activate the application

```
(flaskdeploy)$ cd ~/sites/flaskdeploy
(flaskdeploy)$ gunicorn sample:app
```
In the example application, the Python script is named sample.py. If you open that script, you will see there is a variable called app.

So to activate this application with gunicorn, type this command under the application directory.

- open the public domain via a web browser

See we changed a web page without juggling HTML!

#### Let Supervisor manage process

You may notice that once we started our gunicorn server we’ve lost access to the command line. We would have to haul the server to run any other commands. One solution to this would be to run the server in a screen or in the background, giving control back to the user. But this still wouldn’t help us if the server ever needs to reboot. Preferably we could find a solution the run our gunicorn server in the background and also start it automatically on reboot. Enter supervisor.

Supervisor is a software that allows users to manage multiple processes, so we could actually have multiple gunicorn sites running with different configurations. Now we’ll write a configuration file for our flaskdeploy site: (note that this file MUST end with a .conf extension)

- Create a configuration file in a customized place  /etc/supervisor/conf.d/flaskdeploy.conf

```
(flaskdeploy)[ec2-user etc]$ cd /etc
(flaskdeploy)[ec2-user etc]$ sudo mkdir supervisor
(flaskdeploy)[ec2-user etc]$ cd supervisor
(flaskdeploy)[ec2-user supervisor]$ sudo mkdir conf.d
(flaskdeploy)[ec2-user supervisor]$ cd conf.d
(flaskdeploy)[ec2-user conf.d]$ sudo nano flaskdeploy.conf
```

- Fill content below

```
[program:flaskdeploy]
command = /home/ec2-user/.virtualenvs/flaskdeploy/bin/gunicorn sample:app
directory = /home/ec2-user/sites/flaskdeploy
user = ec2-user
stdout_logfile = /home/ec2-user/sites/flaskdeploy/logs/gunicorn/gunicorn_stdout.log
stderr_logfile = /home/ec2-user/sites/flaskdeploy/logs/gunicorn/gunicorn_stderr.log
redirect_stderr = True
environment = PRODUCTION=1

[supervisord]
```
- Create folders for logs

```
(flaskdeploy)[ec2-user init.d]$ cd ~/sites/flaskdeploy/logs/
(flaskdeploy)[ec2-user logs]$ mkdir gunicorn
(flaskdeploy)[ec2-user logs]$ cd gunicorn
```

- Create empty log files

```
(flaskdeploy)[ec2-user gunicorn]$ sudo nano gunicorn_stdout.log
(flaskdeploy)[ec2-user gunicorn]$ sudo nano gunicorn_stderr.log
```
After entering editing mode in nano, press ```ctrl``` + ```0``` immediately to create an empty file.

Since supervisor is installed under the bin folder of python. In order to check the folder of supervisord, do this:

```
(flaskdeploy)[ec2-user ~]$ which python
~/.virtualenvs/flaskdeploy/bin/python
```
So supervisord is ```~/.virtualenvs/flaskdeploy/bin/supervisord```. If supervisord does not exist, use pip to install supervisor.

- Daemonize gunicorn process

```	
(flaskdeploy)[ec2-user ~]$ sudo ~/.virtualenvs/flaskdeploy/bin/supervisord -c /etc/supervisor/conf.d/flaskdeploy.conf
```
Now the example application has been run by supervisord.

*<font color = red>But Wait. Wouldn't you want to manage these processes by supervisor as easy as pressing a switch button?</font>*

Here is the few steps to make our works perfect. We are going to run supervisor as a service.

- Before we begin, close supervisord process.

check process related to python

```
$ ps aux| grep python
```

If you are following this documentation exactly, we only monitored a flask application with supervisor. What you have should be similar to this.

![](https://sites.google.com/site/eugenekmlwebmap/whatever/pythonprocess.png?attredirects=0&d=1)

To kill the supervisor process and the application.

```
//$ sudo kill -9 [pid number]  (e.g. sudo kill -9 16155)
// these examples kill services with id numbers as shown in the example picture
$ sudo kill -9 16155 
$ sudo kill -9 16156
$ sudo kill -9 16161
```
Check public DNS of this ec2 instance. Open a browser, input the public DNS, we should have 502 error.

- setup supervisord on a AMI Linux server. Please follow the first answer on this post to do it. Here is the link: [Setting up supervisord on a AWS AMI Linux server](http://stackoverflow.com/questions/28702780/setting-up-supervisord-on-a-aws-ami-linux-server) 

 
**Now, we can use the service *Supervisord* to manage GUnicorn, instead of running Supervisor alone as a application.**

The configuration file of supervisord for gunicorn should be used as an addition to the major configuration file of supervisord, instead of an individual configuration file to run.

	$ sudo nano /etc/supervisor/conf.d/flaskdeploy.conf
	
- delete ```[supervisord]``` section from this configuration file, and save it. 

- open the main configuration file of supervisor  ```/etc/supervisord.conf```

```
$ sudo nano /etc/supervisord.conf
```
- add content below to the end of file, and save it.

```
[include]
files = supervisor/conf.d/*.conf
```
Let us see if gunicorn has been managed by supervisord service. Because we followed the answer of [a stackoverflow post](http://stackoverflow.com/questions/28702780/setting-up-supervisord-on-a-aws-ami-linux-server) to set up supervisor, your service supervisord should be turned on. 

- You can restart to load all configuration files.

```
$ sudo  service supervisord restart
```

**In order to turn on and off a process as easy as turn a button, supervisorctl could offer the control we like.**

Theoretically, you can use supervisorctl to control program processes. However, if you call it, you will get a denial info. 

```
error: <class 'socket.error'>, [Errno 13] Permission denied: 
file: /usr/lib/python2.7/socket.py line: 224
```

The permission error stems from access permissions to supervisord’s socket file, which by default is owned by root, and not writable by other users. We can make supervisord chown and chmod the file to a particular user or group on startup, granting the user or group permission to stop and start the services we’ve configured without requiring sudo.

- Lets create a group, add ourselves to it by doing the following.

```
ec2-user$ sudo su -        // log in root
root$ groupadd supervisor   // this supervisor is the new group
root$ usermod -a -G supervisor <myusername>
```

- After logging-out/logging-in (so that the new group membership takes effect), edit the supervisord configuration file to make the ```unix_http_server``` section look as following content.

```
ec2-user$ sudo nano /etc/supervisord.conf
```

```
[unix_http_server]
file=/tmp/supervisor.sock   ; (the path to the socket file)
chmod=0770                       ; socket file mode (default 0700)
chown=root:supervisor
```
- Save the conf file and restart supervisord service.

```
$ sudo service supervisord restart
```


Now we can use supervisorctl to manage wsgi programs.
	
For example:

```
$ supervisorctl start flaskdeploy
$ supervisorctl stop flaskdeploy
```
## REST APIs Development

In this section, I will provide a few samples to show you how to design, code, test and deploy REST APIs on local machine and on the server when codes are ready for production. If you would like to develop advanced REST APIs, official site of Flask has a good documentation to help you. 

In order to move our flask applications to server, we can create a git repository on Github.

- If you do not have a Github account, register one.
- if you do not have git installed on your development machine (AKA your local machine), use google to search how to install git on your development machine.
- Create a Github repository on Github website. Its name could be anyone you like.
- Create a local repository on your development machine, so our flask applications could be placed there.

These commands below are suitable for MacOS and Linux. If you are using a Windows machine, you can run these commands in a Git Bash prompt installed along with Git.

```
$ mkdir ~/flask_api_ec2
$ cd ~/flask_api_ec2
$ git init
$ echo "# flask_api_ec2" >> README.md
$ git add README.md
$ git commit -m "first commit"
$ git remote add origin https://github.com/(yourgithubaccount)/(your_github_repo).git     
//replace the content inside the services 
$ git push -u origin master

```

After this, we could develop and test our Rest API services in a local machine. After ensuring it is suitable for production, we could deploy it to our server.


###Toy code samples

***Hello world service***

- create a python script with this content.

```
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"
    
if __name__ == '__main__':
    app.run(debug = True)
```

Save this script as helloworld.py.

- Push the python script to Github repo

```
$ cd ~/flask_api_ec2
$ git status
```

You can see new file in this local git repo. Now we add this file in order to commit it to git repo and so we can push this repo to our Github repo.

```
$ git add helloworld.py
$ git commit -m 'upload flask application'
$ git push
```

Test on local machine.

- Create a virtualenv on your local machine (e.g. mac)

Note: create this virtualenv under anywhere you like by replacing the path in parenthesis and the parenthesis.

```
$ cd (the location of a folder of the new virtualenv)
$ virtualenv restflask
```

- Pip install flask under this virtualenv.
			
- Run this flask application on local machine
    
```
(restflask)flask_api_ec2 username$ python helloworld.py
```
If this flask application is running successfully, the terminal of mac will show content like:

```
* Running on http://127.0.0.1:5000/ (Press CTRL + C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 100-727-256
```
Now we could open a web browser with this address, then you can see hello world. This indicates this application is running successfully, otherwise the familiar error message will be shown on the browser instead. 

***JSON result services***

Rather than returning text message as plain text, it is more often that a REST service will return result in JSON format or other text formats. Let us develop a basic Rest API returning JSON services.

- Create a new python script with this content

```
from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
```
Save as restapi.py under ```flask_api_ec2``` folder

- execute it on terminal of the local machine.

```
... username$ cd ~/flask_api_ec2
flask_api_ec2 username$ python restapi.py
```

This rest api is activated on our local machine. We could use it directly with a browser, but there is a tool specifically for testing web services. 

It is Postman. 

![](http://blog.getpostman.com/wp-content/uploads/2014/07/logo.png)

<center>Logo of Postman</center>

![](http://blog.getpostman.com/wp-content/uploads/2015/05/postman-2.png?x38712)

<center>User Interface of Postman</center>

You can get it as a Chrome Extension from Chrome or an application from its official website. When your REST APIs become complicated, they could have multiple parameters and more methods than just GET. Postman could help you test your REST APIs in a convenient and organized way. 

###Example of a machine learning API service

You may be interested to REST at the very first point only because you saw it somewhere and people talked about it like it is something really good, but when this topic becomes realistic, a question is inevitable: Why do we choose REST or REST APIs as the form to develop for the backend? Specific questions following include questions about its advantages, design principles, etc.. Therefore, I would like to show you at least an advantage of REST APIs and a link to a brief introduction of REST. 

In today, computer is not the only type of devices to connect you to the Internet. Mobile devices, smart televisions or even smart furnitures are capable of connecting to the Internet. The variety of clients of web services needs a design of web services that provides services in a standard form.

REST style requests all resources should be identified with unique URI, a global ID. For resources, I will understand them as objects you are dealing with. Each resource will have up to 4 standard methods (GET, POST, PUT, DELETE) to handle all its requests.

A section in [A Brief Introduction to REST](https://www.infoq.com/articles/rest-introduction) explains the advantage of using standard methods.
> Essentially, it makes your application part of the Web — its contribution to what has turned the Web into the most successful application of the Internet is proportional to the number of resources it adds to it. In a RESTful approach, an application might add a few million customer URIs to the Web; if it’s designed the same way applications have been designed in CORBA times, its contribution usually is a single “endpoint” — comparable to a very small door that provides entry to a universe of resource only for those who have the key.

>The uniform interface also enables every component that understands the HTTP application protocol to interact with your application. Examples of components that benefit from this are generic clients such as curl and wget, proxies, caches, HTTP servers, gateways, even Google/Yahoo!/MSN, and many more.

>To summarize: For clients to be able to interact with your resources, they should implement the default application protocol (HTTP) correctly, i.e. make use of the standard methods GET, PUT, POST, DELETE.

Anyway, REST is such a large topic that its author, Roy T. Fielding, used his PhD dissertation to introduce and explain it. If you want to know the design principles of REST and reasons behind them, please read this article, [A Brief Introduction to REST](https://www.infoq.com/articles/rest-introduction), to get some ideas quickly.

I will show you how I design, code, test this REST API example. Eventually, we will move on to the next section to show you how to deploy this REST application on AWS EC2 instance. The part of machine leanring is a code example from Trask. You can click [this link](https://iamtrask.github.io/2015/11/15/anyone-can-code-lstm/) to see it and understand more about Recurrent Neural Network (RNN), one of Deep Learning methods.

***Design***

In this example, I will make a practical example using a code example of machine learning. This code example of machine learning trained the machine to do the adding operation. I will make a RESTful web service to use the trained model to do the adding of two given numbers at the binary level. The result will be a JSON text containing the adding result in decimal notation and two input numbers.

This practical example of a web service will be a chance for me to design REST APIs and associated standard HTTP methods. Since this is not complex, I create only one resource. In terms of standard methods, POST method will be used to take two input numbers as parameters to perform adding operation because POST takes parameters and has a role as the 'catch-all' verb for operations even through this method will not create a resource. Moreover, Using the other methods(GET, PUT, DELETE) for adding can violate the meaning of these HTTP verbs/methods. Eventually, this web service will only implement one method POST and it is okay to decide which verb to use.

***Code***

**I will suggest you to clone a prepared Github repo for this tutorial exclusively to your local machine. All examples, including the code sample from Trask, are there.**

```
$ cd ~
$ mkdir RESTexample
$ cd RESTexample
$ git clone https://github.com/eugeneYWang/RestAPI_flask.git
```

The code of REST application. RNNadd.py

```
from flask import Flask, jsonify, request
import RNNcodeexample  # import ML code sample
import numpy as np
import copy

app = Flask(__name__)

# resource name is RNNaddition. Used to be a noun.
# Method POST.
@app.route('/RNNaddition', methods = ['POST'])
def calculate():
    num1 = request.args.get('number1')
    num2 = request.args.get('number2')

    if isinstance(num1,basestring):
        num1 = int(num1)
        num2 = int(num2)

    num1_bin = RNNcodeexample.int2binary[num1]
    num2_bin = RNNcodeexample.int2binary[num2]

    c = num1+num2
    c_bin = RNNcodeexample.int2binary[c]

    d = np.zeros_like(num2_bin)
    overallError = 0  # initial error

    binary_dim = RNNcodeexample.binary_dim

    # to store hidden value at each timestamp
    layer_1_values = list()
    #initial values are 0 	
    layer_1_values.append(np.zeros(RNNcodeexample.hidden_dim))  

    synapse_0 = RNNcodeexample.synapse_0
    synapse_h = RNNcodeexample.synapse_h
    synapse_1 = RNNcodeexample.synapse_1

	# use the trained model to predict each binary value of the adding result.
    for position in range(binary_dim):
        X = np.array([[num1_bin[binary_dim - position - 1], num2_bin[binary_dim - position - 1]]]) 
        layer_1 = RNNcodeexample.sigmoid(np.dot(X, synapse_0) + np.dot(layer_1_values[-1], synapse_h))  
        layer_2 = RNNcodeexample.sigmoid(np.dot(layer_1, synapse_1))  

        d[binary_dim - position - 1] = np.round(layer_2[0][0])  
        layer_1_values.append(copy.deepcopy(layer_1)) 
        
    out = 0
    for index,x in enumerate(reversed(d)):
        out += x*pow(2,index)

    return_result = {'num1':num1, 'num2':num2, 'pred_bin':str(d), 'pred_num':out, 'true_bin':str(c_bin), 'true_num':c}

    return jsonify(return_result)

if __name__ == '__main__':
    app.run(debug=True)
```

***Test***

- in Terminal of local machine, use python to execute RNNadd.py

```
$ cd ~/RESTexample
$ python RNNadd.py
```
Wait for the training process to be done, then we can use postman to test our REST API.

***Backup***

This section is for those who have never used Git and Github. This is just to show you how to update or add files to your Github repo. You may copy RNNadd.py to your local repo ```~/flask_api_ec2``` to follow this process.

- upload RNNadd.py to Github repository

```
$ cd ~/flask_api_ec2
$ git status
```

You should see RNNadd.py is not tracked. 

```
$ git add RNNadd.py
$ git commit -m 'upload REST app'
$ git push
```


## Deploy on AWS cloud

All operations in this section is on AWS EC2 instance.

- Close supervisor at first, then we test if our REST application can run successfully.

Make sure that previous supervised program FLASKDEPLOY is stopped. 

```
$ supervisorctl status
```
if it is not, stop it.

```
$ supervisorctl stop flaskdeploy
```
Unlink the sock file and stop supervisor, otherwise errors might happen when we shutdown supervisor.

```
$ sudo unlink /tmp/supervisor.sock
$ sudo service supervisord stop
```
- download the Github repo with REST API application.

```
$ cd ~/sites
$ git clone https://github.com/eugeneYWang/RestAPI_flask.git
```

- test REST API application by running it with GUnicorn

```
$ source ~/.virtualenvs/flaskdeploy/bin/activate
(flaskdeploy)$ gunicorn RNNadd:app
```
You may find errors because numpy is not installed in this virualenv.

```
(flaskdeploy)$ pip install numpy
```
If you execute this code again, you should notice CRITICAL message ```[CRITICAL] WORKER TIMEOUT```, then the compiling process will just keep running. Press CTRL + C to stop it.

- extend TIMEOUT value of GUnicorn.

```
(flaskdeploy)$ gunicorn RNNadd:app --timeout 300
```

Now the value is 300 seconds for the process to start. if it need more times to compile, please extend the value and try more.

- Create a supervisor configuration file in ```/etc/supervisor/conf.d/``` which is a folder we created. 

  The command to execute our Python APIs will be included in it.
  
```
$ cd /etc/supervisor/conf.d/
$ sudo nano RNNaddition.conf
```

```
[program:RNNaddition]
command = /home/ec2-user/.virtualenvs/flaskdeploy/bin/gunicorn --timeout 300 RNNadd:app
directory = /home/ec2-user/sites/RestAPI_flask
stdout_logfile = /home/ec2-user/sites/flaskdeploy/logs/gunicorn/gunicorn_stdout.log
stderr_logfile = /home/ec2-user/sites/flaskdeploy/logs/gunicorn/gunicorn_stderr.log
redirect_stderr = True
environment = PRODUCTION=1
```

- start supervisord service and stop all programs immediately to avoid the conflict of port 8000.

```
$ sudo service supervisord start
$ supervisorctl stop flaskdeploy
$ supervisorctl stop RNNaddition
$ supervisorctl start RNNaddition
```

At my Micro EC2 instance, I waited 5 minutes to ensure REST API is compiled. You can test it with Postman to see if it works. Even through you do not see prompting lines after hitting ```supervisor start RNNaddition```, you can check them in ```/tmp/supervisord.log``` with nano.



## Notes:
Some parts of this section are extracted from [Deploying a Flask Site Using NGINX Gunicorn, Supervisor and Virtualenv on Ubuntu](http://alexandersimoes.com/hints/2015/10/28/deploying-flask-with-nginx-gunicorn-supervisor-virtualenv-on-ubuntu.html). 

The rest of the article illustrates the ways of 'Init server', 'Create Deploy User', 'Lock down SSH'. Since this steps is to 

>Jordan Adams: "The reason to opt for a secondary deploy user is purely security. Normally you'd go ahead and root (limit) this user to the app's location on the server. That way if the deploy account is compromised by for example a disgruntled developer, the rest of the server is safe.

>The reason for setting up passwordless auth for this deploy user is so that you don't have to enter a password for each deployment. Instead you're authenticating by a private key on your machine."

[Reference](https://gist.github.com/learncodeacademy/3cdb928c9314f98404d0)

It also illustrates a section of "Update Aptitude (Package Manager)", which is ignored in this section, since Amazon Linux (AMI) uses Yellowdog Updater, Modified (YUM), instead of Aptitude, to manage packages.
 






