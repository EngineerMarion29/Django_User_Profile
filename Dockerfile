# Use CentOS 8 as the base image
FROM centos:8

# Install system dependencies
RUN yum -y update && \
    yum -y install python3 python3-pip

# Set the working directory inside the container
WORKDIR /userprofile_app

# Copy the Django app files into the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the Django development server port (change as needed)
EXPOSE 8000

# Run the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
