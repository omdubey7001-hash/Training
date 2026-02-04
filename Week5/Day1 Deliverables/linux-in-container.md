# Linux Inside Docker Container

## Build images
- `docker build -t day1-demo .` -> This command is used to create the docker image.
- To run the container of the image that is generated from the Dockerfile `docker run -d --name day1_container -p 3000:3000 day1-demo`

## Process Management
- `ps` shows running processes
- PID 1 is Node app

![Process list inside container](images/Process.png)

## Filesystem
- Minimal Linux filesystem
- No systemd or cron

![File inside container](images/File.png)

## Users
- Default user is root
- Permissions still apply

![User inside container](images/Users.png)

## Logs
- Stdout/stderr captured by Docker
- Viewed using `docker logs`

![Logs outside container](images/Logs.png)

## Disk
- Container filesystem is ephemeral
- Volumes needed for persistence

![Disk inside container](images/FileSystem.png)

# Steps to complete Day1

### `docker build -t node-app .`

-> This will build the image first if image is not build.

### `docker run -d -p 3000:3000 --name node-container node-app .`

-> This will create a container named node-container from takingt instance from node-app image and in the current directory and it wil link your port 3000 to the container 3000 port.

### `docker ps`

-> This will show that your container is running 

### `docker exec -it node-container /bin/sh`

-> This will execute the container and take you into the container so that you can use it being inside it .
