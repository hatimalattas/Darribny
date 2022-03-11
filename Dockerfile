# FROM allows us to build our required image over a base image. The base image we choose here is buster, which is a
# Docker’s own “official” python image. This image itself is large, but these packages are installed via common image
# layers that other official Docker images will use, so the overall disk usage would be low.
FROM python:3.8.9-buster

# Set the present working directory.
WORKDIR /app

# Copy the dependencies file from your host to the present working directory.
COPY requirements.txt .

# To install all dependencies or pip packages.
RUN pip install -r requirements.txt

# Copy the rest of your app’s source code from your machine to the present working directory of the container.
COPY . .

# CMD is the command to run on container start. It specifies some metadata in your image that describes how to run a
# container based on this image. In this case, it’s saying that the containerized process that this image is meant to
# support is python app.py. There can be only one CMD command per Dockerfile, if in case there is more, the last CMD
# command will take effect.
CMD ["python", "app.py"]
