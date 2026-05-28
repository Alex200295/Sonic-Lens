# External DSP Microservice

This microservice provides true native audio DSP analysis using `librosa`, `numpy`, `scipy`, and `soundfile`.
It is designed to be hosted separately (e.g., in a Docker container on Cloud Run or a VPS) and called by the Node.js backend.

## Deployment

1. Build the Docker image:
   ```bash
   docker build -t dsp-service .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 dsp-service
   ```

The service will be available at `http://localhost:8000`.

## Integration

Set the `DSP_SERVICE_URL` environment variable on your Node.js backend to point to this service (e.g., `http://localhost:8000`). If it is not set, it defaults to `http://localhost:8000`.
