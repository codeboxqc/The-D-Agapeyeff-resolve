#!/bin/bash
set -e

echo "=== Updating system ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing essentials ==="
sudo apt install -y git python3 python3-pip python3-venv cmake build-essential wget unzip

echo "=== Installing OpenCL GPU drivers (Mali G610) ==="
sudo apt install -y mali-g610-firmware rockchip-multimedia-config clinfo
echo "Testing OpenCL..."
clinfo | head

echo "=== Creating Python venv ==="
python3 -m venv ~/ai
source ~/ai/bin/activate
pip install --upgrade pip

echo "=== Installing AI Python packages ==="
pip install numpy scipy onnx onnxruntime-gpu pillow

echo "=== Installing RKNN Toolkit 2 (NPU support) ==="
wget https://github.com/rockchip-linux/rknn-toolkit2/releases/download/v2.0.0/rknn-toolkit2-2.0.0-cp310-cp310-linux_aarch64.whl
pip install rknn-toolkit2-2.0.0-cp310-cp310-linux_aarch64.whl

echo "=== Installing llm-rk3588 (GPU-accelerated LLM runner) ==="
git clone https://github.com/airockchip/llm-rk3588.git
cd llm-rk3588
pip install -r requirements.txt
cd ~

echo "=== Installing llama.cpp with OpenCL ==="
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j4 LLAMA_CLBLAST=1
cd ~

echo "=== Setup complete! ==="
echo "You can now run:"
echo " - GPU LLMs via: llm-rk3588"
echo " - NPU models via: rknn-toolkit2"
echo " - OpenCL apps via: llama.cpp or custom kernels"

