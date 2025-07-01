 # Use a base Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy pyproject.toml and poetry.lock (or requirements.txt if using pip)
#COPY pyproject.toml poetry.lock ./
COPY pyproject.toml ./

# Install dependencies using poetry (or pip install -r requirements.txt)
RUN #pip install poetry && poetry install --no-root

# Copy your application code
COPY . .

RUN pip install .
# Define the ENTRYPOINT
# Option 1: Using a defined script from pyproject.toml
#ENTRYPOINT ["run-bot"]

# Option 2: Explicitly running a Python file
#ENTRYPOINT ["ls", "-al"]
ENTRYPOINT ["python", "src/main.py"]

# CMD can provide default arguments to the ENTRYPOINT
#CMD ["--some-default-arg"]