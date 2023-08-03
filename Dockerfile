# Use CentOS 8 as the base image
FROM centos:8
#FROM quay.io/centos/centos:stream9

#Support centos8 end of life
RUN cd /etc/yum.repos.d/ \
    && sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* \
    && sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

# Install system dependencies
RUN yum -y update \
    && yum -y install gcc openssl-devel bzip2-devel sqlite-devel make \
    && yum -y install wget \
    && wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz \
    && tar xzf Python-3.11.3.tgz \
    && cd Python-3.11.3 \
    && ./configure --enable-optimizations \
    && make altinstall

# Set the working directory inside the container
WORKDIR /userprofile_app

# Copy the Django app files into the container
COPY . .

# Install Python dependencies
RUN python3.11 -m ensurepip \
    && pip3.11 install -r requirements.txt

# Expose the Django development server port (change as needed)
EXPOSE 5000

# Run the Django development server
CMD ["/usr/local/bin/python3.11", "manage.py", "runserver", "0.0.0.0:5000"]
