# Street Parking Toronto

WIP/Proof of concept app to display street parking location data on a map. The intention of this app
is to make it easier for folks to find valid street parking near where they want to go.

## Setup

Run the following commands to get this project working locally:

```
git clone https://github.com/asharp02/street-parking-toronto.git
```

Build the Docker image specified within the Dockerfile:

```
docker build -t parking . --no-cache
```

Run the container with this image (port 8000 is accessible on the host machine at port 8080):

```
docker run --name parking -p 8080:8000 parking
```

Visit http://localhost:8080 to view the app (currently No FE but can run docker exec + add django mgmt commands to import data)
