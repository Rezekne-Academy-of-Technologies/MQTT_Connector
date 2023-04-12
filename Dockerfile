# getting base image / python /.
FROM python:3.11.1

# is used to set the Author field of the generated images.
MAINTAINER Armands

# this code line will create a directory where the code will be stored.
#mkdir = make directory
RUN mkdir -p /app/src

# is used to define/set the working directory.
WORKDIR /app/src

# is used for copying all the dependencies and adding them in pre-set WORKDIR.
COPY requirements.txt .

# Install the requirements/dependencies inside of the container.
RUN pip install -r requirements.txt

# here all the files in "flaskProject1" are being copied and pasted in a newly created working directory.
COPY . .

# tells Docker that a container listens for traffic on the specified port in order to view our project in a browser.
EXPOSE 8887

# CMD is the command the container executes by default when you launch the built image.
CMD ["python", "app.py"]