curl -fsSL https://ollama.com/install.sh | sh

ollama serve

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

ollama run llama3:8b   (# it will need 4.7GB GPU RAM)


#ollama run llama3:70b ( it will need 40 GB GPU VRAM)