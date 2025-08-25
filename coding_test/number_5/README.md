# Create a platform with UI

## Approach

- Computer vision extraction using [easyocr](https://github.com/JaidedAI/EasyOCR)
- Vector database using from previous case (case number 4)
- Backend implementaion using [fastapi](https://fastapi.tiangolo.com/)
- Frontend implementation using [streamlit](https://streamlit.io/)
- Agentic framework using [google-adk](https://google.github.io/adk-docs/)
- Run LLM locally using [ollama](https://ollama.com/)

## How to run

### Prerequisite

- Install docker from docker official [page](https://docs.docker.com/get-started/get-docker/)
- (optional) Install [nvidia tool kit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### Build and run

Build docker image
```bash
docker build -t receipt_app .
```

Run app
```bash
docker run --rm -p 8000:8000 -p 11434:11434 -p 8501:8501 --gpus all -v {local/ollama/dir}:/root/.ollama --env-file {env_filename} receipt_app
```
Flags explanation
- `-p` for 3 (three) forwarded ports
    - 8000 for the backend app
    - 11434 for the ollama
    - 8501 for the frontend app
- `--gpus` gpus (if any) to allow docker access gpu (optional)
- `-v` to mount volume of ollama directory to avoid downloading model when container is restarted
- `--env-file` Local env file that has api key for agentic model
