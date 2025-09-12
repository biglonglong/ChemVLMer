## Overview

这是一个基于 [Intern-S1](https://chat.intern-ai.org.cn/) 的封装部署演示



## Installation and Usage

### Prerequisites

- Python 3.x

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

1. 配置环境变量

   获取[书生大模型 - Intern - token](https://internlm.intern-ai.org.cn/api/tokens)，请在项目根目录下创建 `.env` 文件，并添加相关密钥，例如：

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

2. 运行主程序

   ```bash
   python main.py
   ```



## References

- [书生大模型 - Intern](https://chat.intern-ai.org.cn/)
- [书生大模型 - Intern - API](https://internlm.intern-ai.org.cn/api/document)
