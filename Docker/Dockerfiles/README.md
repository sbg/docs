# Dockerfiles

Dockerfiles that illustrate how to use existing base images and install new packages for personal use:
- Python2: Installing new packages in the continuumio/anaconda container (Python)
- R: Installing new packages in a rocker/r-base container (R)
- Bioconductor: Installing new Bioconductor packages from the base image (R)
- SamTools: Installing SamTools in an ubuntu container

If you have a request for examples on how to build different kinds of Bioconductor packages, please submit them using a GitHub issue. 

To build these containers:

1. Clone the repo with `git`

2. In the command line, navigate to the folder with the Dockerfile you wish to build 

3. Run `docker build -t <repo>/<image>:[tag] .` using the repo and image name you want

More information on Docker can be found at https://docs.docker.com and http://docs.sevenbridges.com/docs/docker-basics
