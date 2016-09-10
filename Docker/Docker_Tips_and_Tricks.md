# Docker Tips & Tricks

Here, we'll cover the language of Docker (what's an image? what's a container?) and some **common use cases** with Docker. [If you'd like to request additional documentation, please make a GitHub issue :)]

## Docker semantics:

**IMAGE**

- e.g. `rfranklin/rstatsdev`
- has an <IMAGE_ID>
- a read-only Docker image that you can pull and run 
- can have a TAG (e.g. `rfranklin/rstatsdev:0.1`)
- default TAG is `latest`
- identified by `<repository>/<name>[:<tag>]`

**CONTAINER**

- a running instance of an image that you can read and write to
- each instance has a unique *CONTAINER_ID*

**COMMAND**

- a command that you can set when first running a container
- e.g. `/bin/bash`

**REGISTRY**

- a place online for storing and/or managing Docker images
- e.g. Docker Hub or the CGC Image Registry

##Modify a container, commit the changes to an image, and push the image to DockerHub:
1. Fire up the Docker command line interface. If you're not on Linux, start with the Docker Quickstart Terminal.

2. `docker login`
 - Enter your username and password. Docker will use stored credentials if they exist.

3. `docker images`
 - Get a list of all your Docker images

4. `docker run -ti <IMAGE>`
 - e.g `docker run -ti rfranklin/pythondev`
 - the `-i` flag allows you to use your new container interactively
 - the `-t` flag allocates a pseudo-TTY or pseudoterminal (to execute commands!)
 - When run, your command line prompt will become `root@<CONTAINER_ID>: `

5. `docker ps -a`
 - After exiting the container, you can retrieve its id with the above command, or use the ID from the container terminal prompt (see Step 4)

6. `docker commit <NEW CONTAINER_ID> <IMAGE>`
 - Commit the container to a new image
 - e.g `docker commit f692sd3s4e1b rfranklin/pythondev:v2`
 - e.g `docker commit f692sd3s4e1b cgc-images.sbgenomics.com/rfranklin/pythondev:v2`

7. `docker push <IMAGE:VERSION>`
 - Finally, push your new image to DockerHub!

##Run a local container interactively: 
`docker run -ti <IMAGE> /bin/bash`

## Look up info about container: 
`docker inspect <IMAGE>`

##Mount a local folder onto your container when running:
`docker run -v /foo:/bar <IMAGE>`

 - Takes /foo in your local machine and make available as /bar in your container

##Fix an error with the Docker Daemon: 
`docker-machine restart default`
`eval ($docker-machine env default)`

- Try this when you try and push a container and it hangs, or you get errors about network issues.

##Retag an image:

 - Get the IMAGE_ID for your image of interest
 - `docker tag <IMAGE_ID> <IMAGE>`
 - e.g. `docker tag sha:4141532 rfranklin/new_image`

The same <IMAGE_ID> can be associated with many repository or image names. This allows you to take a container that you have on DockerHub, for example, and simply retag to push to a Seven Bridges registry. 

**For example:**

1. `docker pull rfranklin/pythondev`
2. `docker tag <IMAGE_ID> images.sbgenomics.com/rfranklin/pythondev`
3. `docker login images.sbgenomics.com`
4. `docker push images.sbgenomics.com/rfranklin/pythondev`

##Copy local file into container: 
`docker cp <PATH/TO/FILE.EXT> <CONTAINER_ID>:</FILE.EXT>`

Example:
`docker cp test.py a4a27b7d1944:/`

- This will copy the files to that specific container

`docker commit a4a27b7d1944 rfranklin/rstatsdev:v2`

- Now the changes you made (copying the files over) will persist to this new image. You can run this image to test your analyses.