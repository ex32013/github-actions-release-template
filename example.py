#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""示例入口程序: 用来自测模板 workflow 的打包与发布流程。
真实使用时, 把本文件替换成你的项目入口(并同步修改 release.yml 中的入口名)。"""
import sys


def main():
    print("Hello from github-actions-release-template!")
    print("Python:", sys.version.split()[0])
    print("This binary was built and released automatically by GitHub Actions.")


if __name__ == "__main__":
    main()
