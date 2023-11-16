# Using lightweight alpine image
FROM python:3.9-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY ./ /usr/src/app

# Install API dependencies
RUN pipenv install --system --deploy
RUN pip install -r requirements.txt
RUN chmod +x /usr/src/app/bootstrap.sh
# Start app
EXPOSE 5000
