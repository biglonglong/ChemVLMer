## Overview

这是一个基于 [Intern-S1](https://chat.intern-ai.org.cn/) 的封装部署演示，通过海康威视 MV-CS200-10GM 工业相机捕获高质量图像，并利用 Intern-S1 多模态模型进行实时异常检测。



## Installation and Usage

### Prerequisites

- Python 3.x or Miniconda

### Installation

1. 创建并激活虚拟环境

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   which python
   which pip
   ```

2. 安装依赖：openai、python-dotenv、opencv-python

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. 根据说明书安装海康工业相机，设置静态 IP，如：

   ```txt
   PC: 169.254.80.61
   Camera: 169.254.128.195
   Mask: 255.255.0.0
   ```

1. 调整代码中的相机 TODO 部分，适配自己的项目

3. 配置环境变量

   获取[书生大模型 - Intern - token](https://internlm.intern-ai.org.cn/api/tokens)，获取海康工业相机IP地址，请在项目根目录下创建 `.env` 文件，并添加相关密钥，例如：

   ```env
   OPENAI_API_KEY=your_openai_api_key
   CameraIp=your_camera_ip 
   ```

3. 运行主程序

   ```bash
   python main.py
   ```



## Todo List

- [ ] 曝光调整



## References

- [书生大模型 - Intern](https://chat.intern-ai.org.cn/)
- [书生大模型 - Intern - API](https://internlm.intern-ai.org.cn/api/document)
- [海康机器人工业相机客户端MVS](https://pinfo.hikrobotics.com/hkws/unzip/20250220113533_17407_doc/)
- [Python对接海康威视机器视觉工业相机_海康相机 python-CSDN博客](https://blog.csdn.net/wenxingchen/article/details/133805272)
