#official Python 3.10 image
FROM python:3.10

#set the working directory 
WORKDIR /src

#add app.py and models directory
COPY app.py .
COPY main.py .
COPY common/ ./common/
COPY computation/ ./computation/

# add requirements file
COPY requirements.txt .

# install python libraries
RUN pip install --no-cache-dir -r requirements.txt

# specify default commands
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]

# docker build -t initial_betting_image .