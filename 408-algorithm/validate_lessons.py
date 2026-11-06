#!/usr/bin/env python3
"""编译并实际运行后备题库的每段 C 代码，防止错误题目自动发布。"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = {
    "kmp-20261111": ("5", "2"),
    "prim-20261112": ("16", "6"),
    "huffman-20261113": ("224", "38"),
    "lc994-20261110": ("4", "1"),
    "lc53-20261108": ("6", "-2"),
    "lc997-20261109": ("3", "-1"),
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
    "lc121-20261031": ("5", "0"),
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
    inputs = {
        "lc217-20261027": "4\n1 2 3 1\n",
        "lc997-20261109": "3 2\n1 3\n2 3\n",
        "lc994-20261110": "3 3\n2 1 1\n1 1 0\n0 1 1\n",
        "lc503-20261106": "3\n1 2 1\n",
    }
    variant_inputs = {"lc997-20261109": "3 3\n1 3\n2 3\n3 1\n",
                      "lc994-20261110": "2 2\n2 0\n0 1\n",
                      "lc503-20261106": "5\n3 8 4 1 2\n"}
    count = 0
    for x in queue:
        case = CASES.get(x["id"])
        if not case:
            raise ValueError(f"未给题目 {x['id']} 配置预期输出，请先审核")
        for variant in ("brute", "optimal"):
            check_one(x[variant]["code"], case[0], x["id"] + "." + variant,
                      inputs.get(x["id"], ""))
            count += 1
        check_one(x["variation"]["code"], case[1], x["id"] + ".variation",
                  variant_inputs.get(x["id"], ""))
        count += 1
        if x["id"] == "lc997-20261109":
            extra = [
                ("single", "1 0\n", "1"),
                ("empty", "3 0\n", "-1"),
                ("pair", "2 1\n1 2\n", "2"),
                ("star", "4 3\n1 3\n2 3\n4 3\n", "3"),
            ]
            for variant in ("brute", "optimal", "variation"):
                for label, data, expected in extra:
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1
        if x["id"] == "lc503-20261106":
            extra = [
                ("single", "1\\n5\\n", "-1"),
                ("equal", "3\\n2 2 2\\n", "-1 -1 -1"),
                ("increasing", "3\\n1 2 3\\n", "2 3 -1"),
                ("wrap", "3\\n3 1 2\\n", "-1 2 3"),
                ("negative", "3\\n-1 -2 -3\\n", "-1 -1 -1"),
                ("extreme", "3\\n1000000000 -1000000000 999999999\\n",
                 "-1 999999999 1000000000"),
                ("descending", "5\\n5 4 3 2 1\\n", "-1 5 5 5 5"),
                ("max_n", "10000\\n" + " ".join(map(str, range(1, 10001))) + "\\n",
                 " ".join(map(str, range(2, 10001))) + " -1"),
            ]
            for variant in ("brute", "optimal", "variation"):
                for label, data, expected in extra:
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1
        if x["id"] == "lc994-20261110":
            # 四邻域与八邻域使用相同输入时可能有不同答案。
            extra = [
                ("blocked", "3 3\n2 1 1\n0 1 1\n1 0 1\n", "-1", "2"),
                ("no_fresh", "1 2\n0 2\n", "0", "0"),
                ("all_fresh", "1 1\n1\n", "-1", "-1"),
                ("diagonal", "2 2\n2 0\n0 1\n", "-1", "1"),
                ("single_rotten", "1 1\n2\n", "0", "0"),
                ("full_10x10", "10 10\n" + ("2 " * 10 + "\n") * 10, "0", "0"),
            ]
            for variant in ("brute", "optimal", "variation"):
                for label, data, standard, eight in extra:
                    expected = eight if variant == "variation" else standard
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1
    # 历史正式题库中不在pending队列的题也要做回归，避免错误变式漏检。
    published = json.loads((ROOT / "lessons.json").read_text(encoding="utf-8"))
    historical_id = "lc200-20261025"
    historical = next((x for x in published if x["id"] == historical_id), None)
    if historical is None:
        raise ValueError(f"已发布历史题目 {historical_id} 不存在")
    for variant in ("brute", "optimal", "variation"):
        expected = "2" if variant == "variation" else "4"
        check_one(historical[variant]["code"], expected,
                  historical_id + "." + variant)
        count += 1
    print(f"验证通过：{len(queue)} 道题，{count} 次C程序编译运行测试。")


if __name__ == "__main__":
    main()
