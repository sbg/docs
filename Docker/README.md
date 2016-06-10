# Getting Started with Docker 
![Docker logo](https://secure.gravatar.com/avatar/26da7b36ff8bb5db4211400358dc7c4e.jpg?s=128&r=g&d=mm)

In this repo, you will find a series of guides and examples on how to use Docker. These include building custom containers for specific programming use cases (e.g. Python, Bioconductor). 

## What is Docker?
[Docker](http://www.docker.com) is an open-source software that allows users to deploy software in discrete, lightweight runtime environments, called “containers.” Essentially, it means that any software can be containerized with its own unique requirements/dependencies and deployed on any infrastructure that supports Docker. This includes your laptop, certain computing clusters, and cloud platforms such as Seven Bridges. Using Docker makes your code portable -- easily sharable with others and runnable in many places. 

## Getting Started
Try walking through the steps outlined below. In sum, they will give you an **excellent understanding** of Docker through hands-on experience.

1. Install the [Docker Toolbox](https://www.docker.com/products/docker-toolbox) (Mac or Windows) or get [Docker for Linux](https://docs.docker.com/linux/). The Docker Quickstart Terminal is *especially* handy!

2. Read up on Docker containers and images and how to use them ([Docker docs](https://docs.docker.com/mac/step_two/) or [CGC docs](http://docs.cancergenomicscloud.org/docs/docker-basics)).

3. Complete the [whalesay tutorial](https://docs.docker.com/mac/step_three/), which will show you how to pull a Docker image to your laptop and run it as a container.

4. Pull the [rfranklin/rstatsdev](https://hub.docker.com/r/rfranklin/rstatsdev/) or [rfranklin/pythondev](https://hub.docker.com/r/rfranklin/pythondev/) image using the Docker CLI and run it.

5. Try mounting some code and test files from your local machine to the container. Replicate an analysis you've done before.

6. Commit the changes from a container to a new image and push it to DockerHub or a Seven Bridges Registry.

7. Write a [Dockerfile](https://docs.docker.com/engine/reference/builder/) and use it to build a new container.

**All done? Now you’re a Docker expert and in great shape to do portable software development.**