FROM python:3.12-slim

# set a directory for the app
WORKDIR /usr/src/app

# copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy all remaining files to the container
COPY . .

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./app.py"]
