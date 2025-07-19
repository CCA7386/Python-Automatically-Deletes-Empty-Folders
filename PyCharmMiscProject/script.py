import os
import sys
import argparse
from typing import List


def find_empty_folders(root_dir: str) -> List[str]:
    """查找所有空文件夹"""
    empty_folders = []

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # 如果当前目录没有子目录和文件，则是空文件夹
        if not dirnames and not filenames:
            empty_folders.append(dirpath)

    return empty_folders


def delete_empty_folders(folder_list: List[str]) -> None:
    """删除空文件夹列表"""
    for folder in folder_list:
        try:
            os.rmdir(folder)
            print(f"已删除空文件夹: {folder}")
        except OSError as e:
            print(f"删除文件夹 {folder} 失败: {e}")


def main():
    # 默认目录路径（可以在代码中修改）
    DEFAULT_DIRECTORY = "C:/"  # 修改为你常用的默认路径

    # 设置命令行参数
    parser = argparse.ArgumentParser(description="自动删除指定目录中的空文件夹")
    parser.add_argument("directory", nargs='?', default=DEFAULT_DIRECTORY,
                        help=f"要扫描的目录路径（默认为{DEFAULT_DIRECTORY}）")
    parser.add_argument("-d", "--dry-run", action="store_true",
                        help="仅显示空文件夹而不实际删除")

    args = parser.parse_args()

    # 检查目录是否存在
    if not os.path.isdir(args.directory):
        print(f"错误: 目录 {args.directory} 不存在")
        sys.exit(1)

    print(f"正在扫描目录: {args.directory}")
    empty_folders = find_empty_folders(args.directory)

    if not empty_folders:
        print("没有找到空文件夹")
        return

    print(f"找到 {len(empty_folders)} 个空文件夹:")
    for folder in empty_folders:
        print(f" - {folder}")

    if args.dry_run:
        print("干运行模式: 不会实际删除文件夹")
    else:
        confirm = input("确定要删除这些空文件夹吗? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_empty_folders(empty_folders)
            print("操作完成")
        else:
            print("操作已取消")


if __name__ == "__main__":
    main()