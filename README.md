# GitHub Actions 自动构建多平台 + 发布 Release 模板

一个通用的 GitHub Actions workflow 模板：推送 tag 时自动将你的 Python 项目打包成 **Windows / Linux / macOS** 三个平台的可执行文件，并自动发布 Release。

## ✨ 功能

- **一键发布**：`git tag v1.0.0 && git push origin v1.0.0` → 全自动
- **三平台并行构建**：Windows / Linux / macOS（GitHub 官方 runner）
- **单文件可执行**：用 PyInstaller `--onefile` 打包，用户免装 Python
- **自动生成 Release**：三个平台的二进制 + README + 自动变更日志
- **支持手动触发**：Actions 页面点「Run workflow」即可

## 🚀 使用方法

### 1. 复制文件

把 `.github/workflows/release.yml` 复制到你的项目对应目录。

### 2. 修改占位符

按你的项目情况替换 workflow 里的这些内容：

| 占位符 | 说明 | 示例 |
|---|---|---|
| `<PROJECT>` | 项目名（生成 exe 文件名） | `mytool` |
| `<YOUR_DEPS>` | 打包时需要的 Python 依赖 | `requests beautifulsoup4` |
| `<YOUR_MODULE1>` | PyInstaller 需要显式引入的模块 | `yt_dlp` |
| `bili_server.py` | 你的**入口脚本**（替换成自己的） | `main.py` |
| `--add-data "index.html;."` | 附加的静态资源文件（不需要可删） | — |

### 3. 保证入口脚本兼容打包

打包后 `__file__` 指向临时目录，需要区分**资源目录**和**数据目录**：

```python
import sys, os

def resource_dir():
    """打包后静态资源位置(sys._MEIPASS)"""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))

def data_dir():
    """运行时数据(cookies/配置)位置: exe 同目录"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
```

- **资源**（只读，如模板、图标）→ 用 `resource_dir()`
- **数据**（可写，如配置、下载记录）→ 用 `data_dir()`

### 4. 推 tag 触发

```bash
git add -A && git commit -m "v1.0.0"
git tag v1.0.0
git push origin v1.0.0        # 自动开始构建
```

### 5. 查看结果

- 构建进度：项目仓库 → **Actions** 标签页
- 发布结果：项目仓库 → **Releases** 标签页

## ⏱ 构建耗时参考

| 平台 | 耗时 |
|---|---|
| Linux | ~2 分钟 |
| macOS | ~3 分钟 |
| Windows | ~4 分钟 |
| **总计（并行）** | **约 3-6 分钟** |

三平台并行，总时间 ≈ 最慢的 Windows 档。

## ⚠️ 注意事项

1. **Release 权限**：workflow 需要 `contents: write` 权限（已在 release job 单独授予）
2. **PyInstaller 体积**：Python 打包的 exe 较大（几十~100MB），因为内含解释器和依赖库
3. **杀毒软件误报**：PyInstaller 单文件 exe 偶尔会被 Windows Defender 误报，属正常现象
4. **tag 与 Release 对应**：删除/重建同名 tag 后，Release 需要手动清理旧的
5. **macOS 架构**：`macos-latest` 是 ARM(Apple Silicon) 机器，产物标记为 `-arm64`；如需 Intel(x64) 请改用 `macos-26-intel` runner 或额外 job
6. **供应链加固**：第三方 action 已 pin 到 commit SHA、依赖已锁版本，请勿随意改回可变标签
7. **手动触发**：Actions 页面点「Run workflow」也可触发，但不会发布新 tag（会用当前分支名作 Release 名），推荐用 tag 推送

## 📁 项目结构

```
github-actions-release-template/
└── .github/
    └── workflows/
        └── release.yml     # 主 workflow（复制到你的项目即可）
```

## 参考

- [GitHub Actions 官方文档](https://docs.github.com/actions)
- [PyInstaller 官方文档](https://pyinstaller.org/)
