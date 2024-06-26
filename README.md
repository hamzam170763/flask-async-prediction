# Flask Asynchronous Prediction Service

This project demonstrates a Flask web application that provides synchronous and asynchronous prediction services. The application uses Redis for temporary storage of prediction results and RQ for background job processing.

## Project Structure
flask_app/
├── app.py
├── mock_functions.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env


## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Step-by-Step Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

2. **Build the Docker image:**
docker-compose build

3. **Run the Docker containers:**
docker-compose up

This command will start the Flask application, Redis, and RQ worker.

## Endpoints

1. **Synchronous Prediction:**

curl -X POST "http://127.0.0.1:8080/predict" -H "Content-Type: application/json" -d '{"input": "Sample input data for the model"}'

Response:

{
  "input": "Sample input data for the model",
  "result": "1234"
}

2. **Asynchronous Prediction:**
Request:

curl -X POST "http://127.0.0.1:8080/predict" -H "Content-Type: application/json" -H "Async-Mode: true" -d '{"input": "Sample input data for the model"}'

Response:

{
  "message": "Request received. Processing asynchronously.",
  "prediction_id": "abc123"
}

3. **Retrieve Asynchronous Prediction Result:**

Request:

curl -X GET "http://127.0.0.1:8080/predict/abc123"

Response (Processing):

{
  "error": "Prediction is still being processed."
}

Response (Completed):

{
  "prediction_id": "abc123",
  "output": {
    "input": "Sample input data for the model",
    "result": "5678"
  }
}

Response (Invalid ID):

{
  "error": "Prediction ID not found."
}

## File Descriptions

    app.py: Main Flask application file defining the endpoints.
    mock_functions.py: Contains the mock function mock_model_predict that simulates the prediction process.
    Dockerfile: Dockerfile for building the Flask application image.
    docker-compose.yml: Docker Compose file to setup the Flask application, Redis, and RQ worker.
    requirements.txt: Python dependencies required for the project.
    .env: Environment variables file (optional).

## Environment Variables
Add the following in the .env file 

FLASK_ENV=development

## Notes

    This project uses Redis for temporary storage of prediction results. If the server or Redis restarts, the results will be lost, which aligns with the requirement for temporary storage.
    The application runs on port 8080 and Redis runs on port 6379.
