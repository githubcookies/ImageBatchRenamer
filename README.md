# ImageBatchRenamer

一个简单易用的图片批量重命名工具，支持GUI界面操作。

## 功能特点

- 🖼️ 支持常见图片格式（JPG、JPEG、PNG、GIF、BMP）
- 📝 两种重命名模式：
  - 首字母模式：修改文件名首字母
  - 序号模式：按顺序重命名（如 flower_1, flower_2）
- 📁 支持文件夹导入或手动选择文件
- 🖱️ 支持拖放文件和文件夹
- 👀 支持双击预览图片
- ✨ 简洁直观的图形界面
- 🔄 实时预览重命名结果

## 安装说明

### 方式一：直接下载
1. 在 [Releases](https://github.com/githubcookies/ImageBatchRenamer/releases) 页面下载最新版本
2. 解压后双击运行 `ImageBatchRenamer.exe`

### 方式二：从源码运行
bash
克隆仓库
git clone https://github.com/githubcookies/ImageBatchRenamer.git
安装依赖
pip install tkinter
运行程序
python image_renamer.py
## 使用说明

1. 添加图片：
   - 点击"添加图片"按钮选择图片
   - 或直接输入文件夹路径按回车
   - 或拖放文件到程序窗口

2. 选择图片：
   - 点击复选框选择单个图片
   - 使用Shift或Ctrl进行多选
   - 点击"全选"或"取消全选"

3. 重命名：
   - 选择重命名模式
   - 输入相应参数
   - 点击"开始重命名"

## 开发环境

- Python 3.6+
- tkinter

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- GitHub: [@githubcookies](https://github.com/githubcookies)
- 问题反馈：请在 GitHub Issues 页面提交
