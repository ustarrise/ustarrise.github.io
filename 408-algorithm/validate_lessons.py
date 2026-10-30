#!/usr/bin/env python3
"""编译并实际运行后备题库的每段 C 代码，防止错误题目自动发布。"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = {
    "lc622-20261107": ("1 20 40 3", "1 9 9 1"),
    "lc503-20261106": ("2 -1 2", "8 -1 8 2 3"),
    "lc169-20261105": ("2", "-1"),
    "lc88-20261012": ("1 2 3 4 5 6", "9 8 7 6 5"),
    "lc876-20261013": ("4", "1"),
    "lc104-20261014": ("3", "2"),
    "lc704-20261015": ("3", "1"),
    "original-insert-20261016": ("1 2 3 4 5 6", "5 4 3 2 1"),
    "original-graph-bfs-20261017": ("1", "2"),
    "lc232-20261018": ("1 2", "1"),
    "array-two-pointer-20261019": ("3\n1 2 3", "3\n1 2 3"),
    "list-reverse-20261020": ("4 3 2 1", "4 3 2 1"),
    "tree-leaves-20261021": ("2", "0\n1\n2"),
    "lc215-20261022": ("5", "2"),
    "lc141-20261023": ("1", "2"),
    "lc236-20261026": ("5", "3"),
    "lc217-20261027": ("1", "1"),
    "lc98-bst-20261104": ("0", "1"),
    "heap-sort-20261028": ("1 2 3 4 5 6", "6 5 4 3 2 1"),
    "lc207-20261029": ("1", "1"),
    "lc150-20261030": ("9", "6"),
    "lc121-20261031": ("5", "5"),
    "lc684-20261101": ("3 1", "4 1"),
    "lc160-20261103": ("8", "8"),
    "lc912-merge-20261102": ("1 2 3 4 5", "5 4 3 2 1"),
    "lc48-20261024": ("7 4 1\n8 5 2\n9 6 3", "3 6 9\n2 5 8\n1 4 7"),
}


def check_one(source, expected, key, stdin_data=""):
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "test.c"
        exe = Path(td) / "test"
        src.write_text(source, encoding="utf-8")
        cc = subprocess.run(
            ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic", str(src), "-o", str(exe)],
            capture_output=True, text=True, timeout=15
        )
        if cc.returncode:
            raise RuntimeError(f"{key}: 编译失败\n{cc.stderr[:2000]}")
        run = subprocess.run([str(exe)], input=stdin_data, capture_output=True, text=True, timeout=5)
        if run.returncode or run.stdout.strip() != expected:
            raise RuntimeError(
                f"{key}: 结果错误，预期 {expected!r}，实际 {run.stdout.strip()!r}，"
                f"返回码 {run.returncode}，错误 {run.stderr[:500]}"
            )


def main():
    queue = json.loads((ROOT / "pending-lessons.json").read_text(encoding="utf-8"))
    count = 0
    for x in queue:
        case = CASES.get(x["id"])
        if not case:
            raise ValueError(f"未给题目 {x['id']} 配置预期输出，请先审核")
        for variant in ("brute", "optimal"):
            check_one(x[variant]["code"], case[0], x["id"] + "." + variant, "4\n1 2 3 1\n" if x["id"] == "lc217-20261027" else "")
            count += 1
        check_one(x["variation"]["code"], case[1], x["id"] + ".variation")
        count += 1
    print(f"验证通过：{len(queue)} 道题，{count} 份C程序，全部编译运行且结果正确。")


if __name__ == "__main__":
    main()
