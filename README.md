# llmops-fractal-training

```sudo yum install libXcomposite libXcursor libXi libXtst libXrandr alsa-lib mesa-libEGL libXdamagemesa-libGL libXScrnSaver```
------------------------------------------------
sudo cp ZscalerRootCertificate.crt /etc/pki/ca-trust/source/anchors
sudo update-ca-trust
-----------------------
curl -fsSL https://ollama.com/install.sh | sh
-----------------------------------
curl -X POST http://localhost:11434/api/generate -d '{
  "model": "llama3:8b”,
  "prompt":"Why is the sky blue?"
}'

----------------------------------
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
------------------------------------
https://ronamosa.io/docs/engineer/AI/Mistral-7B-SageMaker/

----------------
```sudo yum install -y amazon-linux-extras
sudo amazon-linux-extras install epel -y
sudo yum-config-manager --enable epel
sudo yum install git-lfs
git lfs install
git clone  https://huggingface.co/lmsys/vicuna-7b-v1.5
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip3 install e .```
--------------------------
shelltitle "$ |bash"

# Create and name screens
screen -t "Screen 1"
screen -t "Screen 2"
screen -t "Screen 3"
screen -t "Screen 4"
screen -t "Screen 5"

Cntr + A leave both -> 1 switch between screens
Cntr+A leave both and D

-------------------
•First screen - python3 -m fastchat.serve.controller
•Second screen - python3 -m fastchat.serve.model_worker --model-path
•Third screen - python3 -m fastchat.serve.test_message --model-name vicuna-7b-v1.5
-------------------------

pip install transformers
pip install torch
pip install accelerate
pip install protobuf
pip install SentencePiece
-------------------------------

``curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64```

-----------------------------
```sudo sysctl net.core.bpf_jit_harden
sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
minikube start --driver docker --container-runtime docker --gpus all
Kubectl describe nodes```
-------------------
```kubectl describe nodes
Kubectl get namespaces
Kubectl create ns training
Kubectl apply –f deployment.yaml –n training
Kubectl apply –f service.yaml –n training
kubectl get pods -n testing
kubectl get events -n testing```
-----------------
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
            nvidia.com/gpu: 1 #
---------------
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
--------------
kubectl cp /home/ec2-user/ZscalerRootCertificate.crt <pod_name>:/tmp  -n training

cp /tmp/ZscalerRootCertificate.crt /usr/local/share/ca-certificates/
update-ca-certificates

minikube status

minikube start --driver docker --container-runtime docker --gpus all

docker pull ollama/ollama


docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama_new ollama/ollama![Uploading image.png…]()
