# Linux Inside Docker Container

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