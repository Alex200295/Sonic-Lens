# External DSP Microservice

This microservice provides true native audio DSP analysis using `librosa`, `numpy`, `scipy`, and `soundfile`.
It is designed to be hosted separately (e.g., in a Docker container on Cloud Run or a VPS) and called by the Node.js backend.

## Render Deployment

This service is pre-configured for deployment on Render.com using Docker.

1. Create a new GitHub repository and push this `dsp-microservice` folder to the root of the repository (or set the Root Directory in Render to `dsp-microservice`).
2. Log into Render (https://render.com).
3. Click "New" and select "Web Service".
4. Build and deploy from your GitHub repository.
5. In the service settings, ensure the **Environment** is set to **Docker**.
6. Render will automatically expose the `PORT` environment variable which `uvicorn` will map to securely using `sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"`.
7. **Environment Variables**: No additional environment variables are required for this microservice.

Once deployed on Render, update your Node.js application's environment variable:
`DSP_SERVICE_URL="https://your-render-app.onrender.com"`

## Integration

Set the `DSP_SERVICE_URL` environment variable on your Node.js backend to point to this service (e.g., `http://localhost:8000`). If it is not set, it defaults to `http://localhost:8000`.
