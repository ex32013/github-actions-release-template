# GitHub Actions 自动构建多平台 + 发布 Release 模板

一个通用 GitHub Actions workflow 模板：推送 tag 时自动把 Python 项目打包成 **Windows / Linux / macOS** 三平台可执行文件，并自动发布 Release。

## ✨ 功能

- **一键发布**：`git tag v1.0.0 && git push origin v1.0.0` → 全自动构建 + 发布
- **三平台并行构建**：官方 runner 同时跑 Windows / Linux / macOS
- **单文件可执行**：PyInstaller `--onefile` 打包，用户免装 Python
- **自动生成 Release**：三个平台的二进制 + README + 自动变更日志
- **支持手动触发**：Actions 页面「Run workflow」，填版本号即可

## 🚀 使用方法

### 1. 复制文件

把 `.github/workflows/release.yml` 复制到你的项目对应目录。

### 2. 修改占位符

| 占位符 | 说明 | 示例 |
|---|---|---|
| `<PROJECT>` | 项目名（生成 exe 文件名） | `mytool` |
| `<YOUR_DEPS>` | 打包时需要的 Python 依赖 | `requests beautifulsoup4` |
| `bili_server.py` | 你的入口脚本（替换成自己的） | `main.py` |
| `--add-data "index.html;."` | 附加的静态资源文件（不需要可删） | — |

### 3. 入口脚本兼容打包（仅当你用 `__file__` 定位资源/数据时）

打包后 `__file__` 指向临时目录，需区分资源目录与数据目录：

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

构建进度看仓库 **Actions** 页，发布结果看 **Releases** 页。

## ⚠️ 注意事项

1. **发布后勿移动 tag**：workflow 触发后若删除/重建/force-push 同名 tag，`Create Release` 会因「tag 指向的 commit ≠ 触发时记录的 commit」而失败（`softprops/action-gh-release` 防误发布保护）。修正方法：删掉失败 run，再推新 tag
2. **手动触发**：Actions 页面点「Run workflow」时，在 **version 输入框**填版本号（如 `v1.0.0`）即可发布；不填则不会发布
3. **macOS 架构**：`macos-latest` 是 ARM(Apple Silicon) 机器，产物标记为 `-arm64`；需 Intel 版请改用 `macos-26-intel` runner
4. **供应链加固**：第三方 action 已 pin 到 commit SHA、依赖已锁版本，勿改回可变标签
5. **杀毒误报**：PyInstaller 单文件 exe 偶被 Windows Defender 误报，属正常现象

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
