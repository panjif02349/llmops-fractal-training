model=meta-llama/Meta-Llama-3-8B-Instruct
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run
token=

docker run --gpus all --shm-size 1g -e HUGGING_FACE_HUB_TOKEN=$token -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:2.0 --model-id $model



model=meta-llama/Meta-Llama-3-8B-Instruct
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run
token=<token>

docker run --gpus all --shm-size 1g -e HUGGING_FACE_HUB_TOKEN=$token -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:2.0 --model-id $model