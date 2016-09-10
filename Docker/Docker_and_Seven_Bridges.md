#Using Docker on Seven Bridges

You can turn any command line tool packaged in a Docker container into an application on the [Seven Bridges platform](http://docs.sevenbridges.com/docs/sdk-overview) or the [Seven Bridges Cancer Genomics Cloud](http://docs.cancergenomicscloud.org/docs/sdk-overview). From a Docker perspective, all you need is a container on a online registry, the most common of which is [DockerHub](http://hub.docker.com). However, there is also the Seven Bridges and Cancer Genomics Cloud registries, which are optimized for use with each platform.

Here, we'll describe how to associate a Docker image with a Seven Bridges registry and push it. 

##Pushing a container to the Seven Bridges image registry

1. Start by firing up Docker at the terminal.
2. Enter `docker images` to get a list of images. Find the <IMAGE_ID> of the image you want to associated with the Seven Bridges image registry.
3. Tag the image with the new repository name: `docker tag <IMAGE_ID> images.sbgenomics.com/<IMAGE>`
4. Log into Seven Bridges: `docker login images.sbgenomics.com`. When prompted, enter your ***case-sensitive*** username and your authentication token (found under *Account settings > Developer* on the [platform](https://igor.sbgenomics.com)).
5. Push to the registry: `docker push images.sbgenomics.com/<IMAGE>`

##Pushing a container to the Cancer Genomics Cloud image registry

1. Start by firing up Docker at the terminal.
2. Enter `docker images` to get a list of images. Find the <IMAGE_ID> of the image you want to associated with the Seven Bridges image registry.
3. Tag the image with the new repository name: `docker tag <IMAGE_ID> cgc-images.sbgenomics.com/<IMAGE>`
4. Log into the Seven Bridges Cancer Genomics Cloud: `docker login images.sbgenomics.com`. When prompted, enter your ***case-sensitive*** username and your authentication token (found under *Account settings > Developer* on the [the Cancer Genomics Cloud](https://cgc.sbgenomics.com)).
5. Push to the registry: `docker push cgc-images.sbgenomics.com/<IMAGE>`