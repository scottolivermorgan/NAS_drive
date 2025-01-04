# Use the official Glances image as the base image
#FROM nicolargo/glances

# Set environment variable
#ENV GLANCES_OPT="-w"

# Any other customizations you need for your Glances container
# For example, installing additional software or copying configuration files
# RUN apt-get update && apt-get install -y <package-name>

# Expose necessary ports (if needed)
#EXPOSE 61208 61209 61210


FROM nicolargo/glances
COPY glances.conf /glances/conf/glances.conf 
# Set environment variable #"-w"
ENV GLANCES_OPT="-q --export influxdb2 --time 10" 
CMD python -m glances -C /glances/conf/glances.conf --export influxdb $GLANCES_OPT
#CMD python -m glances -C /glances/conf/glances.conf --export influxdb 

EXPOSE 61208 61209 61210