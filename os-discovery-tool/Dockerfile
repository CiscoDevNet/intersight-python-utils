FROM ubuntu

# Install necessary packages
RUN apt-get update && \
    apt-get update --fix-missing && \
    apt-get install -y lshw kmod hwinfo pciutils && \
    apt-get clean

# Create a volume for the code
VOLUME /app

# Copy the HCL Scripts to collect driver information
COPY ./netdriver.sh /app/
COPY ./rchosdockernetversions.sh /app/
COPY ./netdev.sh /app/
COPY ./storagedriver.sh /app/
COPY ./storagedev.sh /app/
COPY ./storagedevnames.sh /app/

# Set the working directory
WORKDIR /app