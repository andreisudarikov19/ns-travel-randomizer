FROM python:3.9-slim

WORKDIR /app

# Install pip libraries
RUN pip install pandas pyyaml

# Copy the Python code, station dastaset and list of visited stations
COPY ns-randomizer.py .
COPY stations-2023-09.csv .

# Run app
CMD ["python3", "ns-randomizer.py"]
