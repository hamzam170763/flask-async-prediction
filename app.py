from flask import Flask, request, jsonify
from flask_cors import CORS
from rq import Queue
from rq.job import Job
from redis import Redis
import uuid
from mock_function import mock_model_predict  # Import the mock function

app = Flask(__name__)
CORS(app)

# Redis connection
redis_conn = Redis(host='redis', port=6379, db=0)
q = Queue(connection=redis_conn)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json.get('input')

    async_mode = request.headers.get('Async-Mode', '').lower() == 'true'

    if async_mode:
        # Generate a unique prediction ID
        prediction_id = str(uuid.uuid4())
        
        # Enqueue the prediction job
        job = q.enqueue(mock_model_predict, input_data, job_id=prediction_id)
        print("-------------------JOB-------------,",job)
        return jsonify({
            "message": "Request received. Processing asynchronously.",
            "prediction_id": prediction_id
        }), 202
    else:
        try:
            prediction = mock_model_predict(input_data)
            return jsonify(prediction)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/predict/<prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    try:
        job = Job.fetch(prediction_id, connection=redis_conn)
        if job.is_finished:
            return jsonify({"prediction_id": prediction_id, "output": job.result}), 200
        else:
            return jsonify({"error": "Prediction is still being processed."}), 400
    except Exception as e:
        return jsonify({"error": "Prediction ID not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
