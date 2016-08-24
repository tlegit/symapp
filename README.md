# My Solution to the Challenge

## Introduction

The solution provides a machanism to:
* authenticate the user against his/her `Google account` using `OAuth`, and
* allow the user to list `LCBO` artifacts such as stores, inventories and products in a tabulated format, through the publicly available `LCBO API`

There are two flavours to this solution:
* to directly start the application, or
* to deploy the application in a Docker container

Each flavour requires certain pre-requisite software components to run.

## Directly Starting the Application

### Installing the pre-requisite modules

Since this solution employs the `Flask` framework, the following modules are required:
* `Flask`
* `Flask-OAuth`

On a Ubuntu system, the following commands are used to install these modules:
```
apt-get update
apt-get -y install python-pip
pip install --upgrade pip
pip install flask flask_oauth
```

### Getting the application and related files/directories

You can obtain the application, and the related files and directories from GitHub:
```
# git clone https://github.com/tlegit/symapp.git
# cd symapp/
```

### Setting required environment variables

Ensure you have the following environment variables set before you run the application:
* GOOGLE_CLIENT_ID
* GOOGLE_CLIENT_SECRET
* LCBO_API_KEY
* APP_SECRET_KEY

Example:
```
# export GOOGLE_CLIENT_ID="<your-client-id>"
# export GOOGLE_CLIENT_SECRET="<your-client-secret>"
# export LCBO_API_KEY="<your-lcbo-api-key>"
# export APP_SECRET_KEY="<pick-a-random-string>"
```

* Follow the instructions [here](https://developers.google.com/identity/sign-in/web/devconsole-project) to get your Google client ID and Google client secret.

* To get your LCBO API key, go [here](https://lcboapi.com/manager/sign-up) to sign up then/or login and follow the instructions.

### Starting the application

Now you can run the application. Make sure your current directory is `symapp`:
```
# python app.py
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: nnn-nnn-nnn
```

### Using the application

Point your web browser to `http://localhost:5000`
* Initially, you will see the Google login screen, login with your google email address/password
* You may be prompted for one or more of the following messages:
  ```
  <project-name> would like to:
  1) Know who you are on Google
  2) View your email address 
  3) Have offline access
  ```
  Click the `Allow` button each time to proceed
* When the Google account authentication is completed, you will see the `Select Option List` where you can select to list the LCBO `stores`, `inventories` or `products` in tabulated format.

### Terminating the application

Simply press Control-C to terminate the application.

## Deploying the application in a Docker container

Although the Docker image for this solution is `tledocker/symapp`, downloadable from Docker Hub. as a user, you do not have to be concerned about it. This is only for your information.

Make sure you have already terminated the application from the previous section.

### Installing docker-compose

Follow the steps [here](https://docs.docker.com/compose/install/) to install docker-compose (and docker-engine as a prerequisite component).

### Preparing the environment variables

The same environment variables mentioned in the previous section must be defined in the `secrets.env` file in the `symapp` directory. Do not add double-quotes at the beginning and end of the string values or they will be considered part of the string values.

### Starting the Docker container that runs the application

Make sure your current directory is `symapp`. Issue the commands as in the following example:
```
# docker-compose up -d
Creating <container-name>
# docker logs <container-name>
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger pin code: 236-035-556
```
This runs the Docker container in the background. The second command above is to display the output of the first command in a container context.

### Using the application

Follow the same steps as in the previous section.

### Terminating the application

Issue the `docker-compose down` command to terminate and remove the application container:
```
# docker-compose down
Stopping <container-name> ... done
Removing <container-name> ... done
```

## Conclusion

The engineer use case is addressed in this implementation, however, the end-user use case is not, even though it is easier to implement. This is because of the security concern over having confidential information coded inside a publicly available Docker image (i.e., client ID, client secret and LCBO API key) that can be extracted by someone with a certain level of knowledge.

I trust that the engineer use case presented herein is adequate to also cover the end-user story in this case.
