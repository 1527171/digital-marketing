---

# Marketing Project

环境配置

## Table of Contents
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Git 拉取代码](#1-git-%E6%8B%89%E5%8F%96%E4%BB%A3%E7%A0%81pull)
- [Git 推送代码](#2-git-%E6%8E%A8%E9%80%81%E4%BB%A3%E7%A0%81push)
- [文件结构](#文件结构)
---

## Installation

### 1. Clone the Project

打开终端下载文件

```bash
git clone https://github.com/1527171/digital-marketing.git
```

## Environment Setup

### 2. Create a Virtual Environment with Conda

创建虚拟环境名为 `marketing` with Python 3.10:

```bash
conda create -n marketing python=3.10
```

Activate the environment:

```bash
conda activate marketing
```

### 3. Set the Virtual Environment in Your IDE

在您的 IDE 中，将 Python 解释器配置为使用您刚刚创建的 'marketing' 环境。

### 4. Install Required Libraries

从 'requirements.txt' 文件安装必要的 Python 库：

```bash
pip install -r requirements.txt
```

---

## Usage

设置完成后，您可以开始使用环境并根据项目的需要运行代码。

---

## **1. Git 拉取代码（Pull）**
`git pull` 是从远程仓库获取最新更改并合并到本地分支。
### **整体代码**
```bash
git pull
git add .
git commit -m "更新内容"
git push
```
### **基本命令**
```bash
git pull <远程仓库名> <分支名>
```

### **步骤**
1. **确保当前在正确的分支**：
   ```bash
   git branch
   ```
   输出带 `*` 的分支是当前分支。切换分支用：
   ```bash
   git checkout <分支名>
   ```

2. **拉取远程更新**：
   ```bash
   git pull origin main
   ```
   - `origin` 是远程仓库的默认名称。
   - `main` 是主分支名称（旧项目可能用 `master`）。

3. **解决冲突（如有）**：
   如果你的本地代码和远程代码有冲突，Git 会提示手动解决冲突：
   - 修改冲突文件。
   - 标记冲突已解决：
     ```bash
     git add <冲突文件>
     ```
   - 提交合并结果：
     ```bash
     git commit -m "Resolved merge conflict"
     ```

---

## **2. Git 推送代码（Push）**
`git push` 是将本地分支的提交推送到远程仓库。

### **基本命令**
```bash
git push <远程仓库名> <分支名>
```

### **步骤**
1. **确保代码已提交**：
   检查是否有未提交的更改：
   ```bash
   git status
   ```
   如果有更改，提交它们：
   ```bash
   git add .
   git commit -m "提交说明"
   ```

2. **推送到远程仓库**：
   ```bash
   git push origin main
   ```
   - `origin` 是远程仓库。
   - `main` 是分支名称。

3. **首次推送新分支**：
   如果是第一次推送新分支，需要显式设置 `--set-upstream`：
   ```bash
   git push --set-upstream origin <分支名>
   ```

---

## **常见场景和命令**

### **1. 克隆远程仓库**
如果你没有本地代码，可以通过 `git clone` 拉取整个项目：
```bash
git clone <远程仓库URL>
```

### **2. 查看远程仓库地址**
查看已连接的远程仓库：
```bash
git remote -v
```

### **3. 检查和切换分支**
- 查看本地分支：
  ```bash
  git branch
  ```
- 查看远程分支：
  ```bash
  git branch -r
  ```
- 切换到其他分支：
  ```bash
  git checkout <分支名>
  ```

### **4. 拉取和推送指定分支**
- 拉取更新：
  ```bash
  git pull origin <分支名>
  ```
- 推送代码：
  ```bash
  git push origin <分支名>
  ```

### **5. 强制推送（谨慎使用）**
如果远程代码与你的本地代码冲突且你确定本地版本覆盖远程是正确的：
```bash
git push origin <分支名> --force
```

---

## **常见问题**

### **问题 1: 推送时报错 `rejected`**
说明远程分支比本地分支更新，需先拉取远程更新：
```bash
git pull origin <分支名> --rebase
```
然后再推送：
```bash
git push origin <分支名>
```

### **问题 2: 拉取时报错 `conflict`**
Git 提示冲突时，你需要手动解决冲突，参见**解决冲突步骤**。

### **问题 3: 无法连接远程仓库**
检查是否配置了 SSH 或 HTTPS：
- 使用 HTTPS：
  ```bash
  git remote set-url origin https://github.com/username/repo.git
  ```
- 使用 SSH：
  ```bash
  git remote set-url origin git@github.com:username/repo.git
  ```
## **文件结构**
---

### 文件夹和代码文件结构

```plaintext
project/
├── data/                                # 数据目录
│   ├── raw/                             # 原始数据
│   └── processed/                       # 处理后的数据
├── src/                                 # 核心代码目录
│   ├── aggregated_keywords
│   │   ├── __init__.py                      # 包初始化文件
│   │   ├── keyword_extraction.py            # 关键词提取模块
│   │   ├── data_processing.py               # 数据加载与预处理模块
│   │   └── aggregation.py                   # 数据聚合模块
│   │
│   └── score_calculator
│       └── traffic_score_calculator.py      # 流量值分数计算模块
│
├── requirements.txt                     # 项目依赖
└── main.py                              # 主程序入口
```

---

### 新增模块文件说明
1. **`keyword_extraction.py`**：
   - 负责从商品标题提取关键词。
   - 使用 NLTK 等自然语言处理工具。
   - 包含停用词去除、关键词提取功能。

2. **`data_processing.py`**：
   - 负责加载 SQL 数据。
   - 数据预处理，例如数据清洗、格式化等。

3. **`aggregation.py`**：
   - 根据商品一级类目名称对关键词进行二级聚合。
   - 输出聚合后的数据。


4. **`traffic_score_calculator.py`**
- **作用**：计算每个关键词和类目对应的流量值分数。
- **输入**：聚合后的数据，包括关键词、类目和支付金额。
- **输出**：添加了“流量值分数”字段的新数据。


---

