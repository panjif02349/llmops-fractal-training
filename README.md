# llmops-fractal-training

```
sudo yum install libXcomposite libXcursor libXi libXtst libXrandr alsa-lib mesa-libEGL libXdamagemesa-libGL libXScrnSaver
sudo cp ZscalerRootCertificate.crt /etc/pki/ca-trust/source/anchors
sudo update-ca-trust
```
# pulling ollana
```
curl -fsSL https://ollama.com/install.sh | sh

```
## Testing the model
```
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3:8b”,
  "prompt":"Why is the sky blue?"
}'
```
## Testing using python
```
import requests
def generate_text(model, prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Accept":"application/json","Content-Type":"application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream":False
    }

    response = requests.post(url, json=data,headers=headers)
    print (response)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

# Example usage
model = "llama3:8b"
prompt = "Why is the sky blue?"
result = generate_text(model, prompt)
print(result)
```
------------------------------------
# vicuna with FastChat 
-----------------------------------
```
sudo yum install -y amazon-linux-extras
sudo amazon-linux-extras install epel -y
sudo yum-config-manager --enable epel
sudo yum install git-lfs
git lfs install
git clone  https://huggingface.co/lmsys/vicuna-7b-v1.5
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip3 install e .```

# Utility - using the multiple windows
shelltitle "$ |bash"

# Create and name screens
screen -t "Screen 1"
screen -t "Screen 2"
screen -t "Screen 3"
screen -t "Screen 4"
screen -t "Screen 5"

Cntr + A leave both -> 1 switch between screens
Cntr+A leave both and D

## screens to maintain
First screen - python3 -m fastchat.serve.controller
Second screen - python3 -m fastchat.serve.model_worker --model-path
Third screen - python3 -m fastchat.serve.test_message --model-name vicuna-7b-v1.5
```
### running modules not found
```
pip install transformers
pip install torch
pip install accelerate
pip install protobuf
pip install SentencePiece
```
# install minikube
url -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64

sudo sysctl net.core.bpf_jit_harden
sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
minikube start --driver docker --container-runtime docker --gpus all
minikube kubectl describe nodes

```
# kubernetes commands
```
Kubectl get namespaces
Kubectl create ns training
```

# yaml files 
**deployment.yaml**

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: training
spec:
  replicas: 1
  selector:
    matchLabels:
      name: ollama
  template:
    metadata:
      labels:
        name: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - name: http
          containerPort: 11434
          protocol: TCP
        resources:
          requests:
            nvidia.com/gpu: 1 # Request 1 GPU
          limits:
            nvidia.com/gpu: 1
```

**service.yaml**
```
apiVersion: v1
kind: Service
metadata:
  name: ollama
  namespace: training
spec:
  type: ClusterIP
  selector:
    name: ollama
  ports:
  - port: 80
    name: http
    targetPort: http
    protocol: TCP
```
# applying the yaml files
```
kubectl apply -f deployment.yaml -n training
Kubectl apply –f service.yaml –n training
kubectl get pods -n testing
kubectl get events -n testing
```
# adding zscaler certificate to the deployment
```
kubectl cp /home/ec2-user/ZscalerRootCertificate.crt <pod_name>:/tmp  -n training
```
# inside the container <need to do this>
cp /tmp/ZscalerRootCertificate.crt /usr/local/share/ca-certificates/
update-ca-certificates
````
# starting minikube
```
minikube status
minikube start --driver docker --container-runtime docker --gpus all
docker pull ollama/ollama:7b
```
# not proper commands
```
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama_new ollama/ollama![Uploading image.png…]()

Pip install llama_index=0.8.5.post2
Pip uninstall pydantic
Pip install pydantic==1.10.14
Pip install ipywidgets

git clone https://github.com/jerryjliu/llama_index
git clone https://github.com/run-llama/finetune-embedding
cd finetune-embedding
pip install -r requirements.txt
----------------------------
conda create -n rag_env python=3.8
pip install langchain langchain_community faiss-cpu bs4 tiktoken chromadb sentence-transformers pypdf litellm trulens_eval

````
-----------------------------------------------------
# important references
```
https://ronamosa.io/docs/engineer/AI/Mistral-7B-SageMaker/

cookbook
https://github.com/langchain-ai/langchain/blob/master/cookbook/Semi_Structured_RAG.ipynb?ref=blog.langchain.dev
```
