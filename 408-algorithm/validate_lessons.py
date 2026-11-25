#!/usr/bin/env python3
"""编译并实际运行后备题库的每段 C 代码，防止错误题目自动发布。"""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = {
    "aoe-critical-20261115": ("9\n1->3->4->6", "8\n1->2->4->6"),
    "quick-sort-20261117": ("1 2 3 4 5 6 7 8", "-1 -1 0 2 3 3"),
    "radix-sort-20261124": ("2 24 45 66 75 90 170 802", "2 24 45 66 75 90 170 802", "初始：329 457 657 839 436 720 355\n第1趟（exp=1）：720 355 436 457 657 329 839\n第2趟（exp=10）：720 329 436 839 355 457 657\n第3趟（exp=100）：329 355 436 457 657 720 839"),
    "shell-sort-20261125": ("4 13 27 38 49 49 55 65 76 97", "13 27 49 55 4 49 38 65 97 76\n4 27 13 49 38 55 49 65 97 76\n4 13 27 38 49 49 55 65 76 97", "(2,A) (2,B) (3,Y) (3,X)"),
    "floyd-20261118": ("0 5 8 9\n-1 0 3 4\n-1 -1 0 1\n-1 -1 -1 0", "0 4 2\n-1 0 -2\n-1 -1 0"),
    "kmp-20261111": ("5", "2"),
    "prim-20261112": ("16", "6"),
    "tree-level-order-20261119": ("A B C D E F", "3"),
    "huffman-20261113": ("224", "38"),
    "dijkstra-20261114": ("0 8 9 5 7", "0 3 1 4"),
    "lc994-20261110": ("4", "1"),
    "lc53-20261108": ("6", "-2"),
    "lc997-20261109": ("3", "-1"),
    "lc-hash-linear-20261116": ("3\n1\n-1\n6\n5", "3\n1\n1\n1\n2"),
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
    "two-stacks-one-array-20261120": ("固定分区：栈1溢出，但栈2一侧仍有空位\ntop1=3, top2=4, mid=4", "数组：10 20 30 40 50 70 80 90\ntop1=4, top2=5\n共享空间：两个栈顶相邻，整个数组已满", "Pop2=9\nPop1=3\nPop2=8\n栈1自底向顶：1 2\n栈2为空：是"),
    "sliding-window-max-20261121": ("3 3 5 5 6 7", "3 3 5 5 6 7", "3 3 5 5 6 7"),
    "sparse-fast-transpose-20261122": (
        "0 1 3 3 4\n5 4 5\n0 2 -3\n1 0 12\n1 3 24\n3 0 9\n4 2 14",
        "0 1 3 3 4\n5 4 5\n0 2 -3\n1 0 12\n1 3 24\n3 0 9\n4 2 14",
        "0 1 3 3\n4 3 4\n0 1 -2\n1 0 5\n1 2 7\n3 1 8",
    ),
    "lc94-inorder-iterative-20261123": (
        "4 2 5 1 3 6",
        "4 2 5 1 3 6",
        "FOUND 5",
    ),
    "tree-reconstruct-pre-in-20261126": (
        "后序遍历：D E B F C A",
        "后序遍历：D E B F C A",
        "先序遍历：A B D E C F",
    ),
    "dll-delete-known-20261127": (
        "删除前：10 20 30 40\n删除后：10 20 40",
        "删除前：10 20 30 40\n删除后：10 20 40",
        "插入前：10 20 30\n插入后：10 20 25 30",
    ),
    "complete-tree-bfs-20261128": ("朴素法：YES", "优化法：YES", "YES"),
    "selection-sort-20261129": ("11 12 22 25 64", "11 12 22 25 64", "1:2 1:4 2:1 2:3"),
    "avl-insert-20261130": ("5\n10 20 25 27 28 30", "3\n10 20 25 27 28 30", "YES"),
    "threaded-binary-tree-20261201": ("1 2 3 4 5 6 7", "1 2 3 4 5 6 7", "4"),    "btree-search-20261202": ("3 2", "3 2", "-1 -1"),
    "linear-search-sentinel-20261203": ("5", "5", "3 1"),

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
        actual = run.stdout.rstrip()
        expected_output = expected.rstrip()
        if run.returncode or actual != expected_output:
            raise RuntimeError(
                f"{key}: 结果错误，预期 {expected_output!r}，实际 {actual!r}，"
                f"返回码 {run.returncode}，错误 {run.stderr[:500]}"
            )

def check_rejected(source, key, stdin_data=""):
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
        if run.returncode == 0:
            raise RuntimeError(f"{key}: 非法输入被程序错误接受")


def main():
    queue = json.loads((ROOT / "pending-lessons.json").read_text(encoding="utf-8"))
    expected_sources = {
        "huffman-20261113": "https://oi-wiki.org/ds/huffman-tree/",
        "dijkstra-20261114": "https://cp-algorithms.com/graph/dijkstra.html",
        "aoe-critical-20261115": "https://m.biancheng.net/view/3417.html",
        "lc-hash-linear-20261116": "https://www.cs.hmc.edu/courses/current.then/cs70/lessons/week12/lesson2/linearprobing/",
        "quick-sort-20261117": "https://www.geeksforgeeks.org/dsa/hoare-s-partition-algorithm/",
        "floyd-20261118": "https://oi-wiki.org/graph/shortest-path/",
        "tree-level-order-20261119": "https://leetcode.cn/problems/binary-tree-level-order-traversal/description/",
        "two-stacks-one-array-20261120": "https://www.geeksforgeeks.org/dsa/implement-two-stacks-in-an-array/",
        "sliding-window-max-20261121": "https://leetcode.cn/problems/sliding-window-maximum/",
        "sparse-fast-transpose-20261122": "https://blog.nerom.wang/2015/02/02/sparse-matrix",
        "lc94-inorder-iterative-20261123": "https://leetcode.com/problems/binary-tree-inorder-traversal/",
        "radix-sort-20261124": "https://oi-wiki.org/basic/radix-sort/",
        "shell-sort-20261125": "https://oi-wiki.org/basic/shell-sort/",
        "tree-reconstruct-pre-in-20261126": "https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/",
        "dll-delete-known-20261127": "https://www.geeksforgeeks.org/dsa/when-is-doubly-linked-list-more-efficient-than-singly-linked-list/",
        "original-insert-20261016": "https://en.oi-wiki.org/basic/insertion-sort/",
        "original-graph-bfs-20261017": "https://oi-wiki.org/graph/bfs/",
        "array-two-pointer-20261019": "https://leetcode.cn/problems/remove-duplicates-from-sorted-array/",
        "list-reverse-20261020": "https://leetcode.cn/problems/reverse-linked-list/",
        "tree-leaves-20261021": "https://www.geeksforgeeks.org/dsa/write-a-c-program-to-get-count-of-leaf-nodes-in-a-binary-tree/",
        "complete-tree-bfs-20261128": "https://www.geeksforgeeks.org/dsa/check-if-a-given-binary-tree-is-complete-tree-or-not/",
        "selection-sort-20261129": "https://oi.wiki/basic/selection-sort/",
        "threaded-binary-tree-20261201": "https://sercankulcu.github.io/files/dsa_c/notes/Chapter_12_Threaded_Binary_Trees_Lecture_Notes.html",        "btree-search-20261202": "https://www.cs.cmu.edu/~christos/courses/721.S03/LECTURES-PDF/0330-CC_Btrees.PDF",
        "linear-search-sentinel-20261203": "https://www.geeksforgeeks.org/dsa/sentinel-linear-search/",

    }
    for lesson in queue:
        source = lesson.get("source")
        if not isinstance(source, str) or not source.startswith(("http://", "https://")):
            raise ValueError("{}: 缺少真实HTTP来源链接".format(lesson.get("id")))
        expected_source = expected_sources.get(lesson["id"])
        if expected_source and source != expected_source:
            raise ValueError("{}: 来源链接与已核验资料不一致".format(lesson.get("id")))


    # 关键课程的逐帧动画回归：避免只有结论、缺少指针/状态的粗略动画。
    animation_minimum = {
        "lc53-20261108": {"brute": 8, "optimal": 9},
        "lc997-20261109": {"brute": 6, "optimal": 6},
        "lc-hash-linear-20261116": {"brute": 10, "optimal": 10, "variation": 5},
        "lc622-20261107": {"brute": 5, "optimal": 7},
        "prim-20261112": {"brute": 4, "optimal": 5},
        "tree-level-order-20261119": {"brute": 4, "optimal": 5, "variation": 4},
        "huffman-20261113": {"brute": 5, "optimal": 5},
        "kmp-20261111": {"brute": 12, "optimal": 17},
        "dijkstra-20261114": {"brute": 5, "optimal": 6, "variation": 5},
        "aoe-critical-20261115": {"brute": 5, "optimal": 9, "variation": 8},
        "quick-sort-20261117": {"brute": 6, "optimal": 10, "variation": 7},
        "floyd-20261118": {"brute": 5, "optimal": 5, "variation": 4},
        "two-stacks-one-array-20261120": {"brute": 4, "optimal": 5, "variation": 9},
        "sliding-window-max-20261121": {"brute": 18, "optimal": 8, "variation": 8},
        "sparse-fast-transpose-20261122": {"brute": 7, "optimal": 8, "variation": 12},
        "lc94-inorder-iterative-20261123": {"brute": 7, "optimal": 8, "variation": 5},
        "radix-sort-20261124": {"brute": 4, "optimal": 10, "variation": 10},
        "shell-sort-20261125": {"brute": 10, "optimal": 9, "variation": 5},
        "tree-reconstruct-pre-in-20261126": {"brute": 4, "optimal": 4, "variation": 4},
        "dll-delete-known-20261127": {"brute": 4, "optimal": 4, "variation": 3},
        "threaded-binary-tree-20261201": {"brute": 5, "optimal": 8, "variation": 4},        "btree-search-20261202": {"brute": 2, "optimal": 2, "variation": 2},
        "linear-search-sentinel-20261203": {"brute": 5, "optimal": 6, "variation": 6},

    }
    diagram_minimum = {
        "lc997-20261109": {"brute": 6, "optimal": 6},
        "lc-hash-linear-20261116": {"brute": 10, "optimal": 10, "variation": 5},
        "prim-20261112": {"brute": 4, "optimal": 5},
        "huffman-20261113": {"brute": 5, "optimal": 5},
        "dijkstra-20261114": {"brute": 5, "optimal": 6, "variation": 5},
        "aoe-critical-20261115": {"brute": 5, "optimal": 9, "variation": 8},
        "quick-sort-20261117": {"brute": 6, "optimal": 10, "variation": 7},
        "floyd-20261118": {"brute": 5, "optimal": 5, "variation": 4},
        "two-stacks-one-array-20261120": {"brute": 4, "optimal": 5, "variation": 9},
        "sparse-fast-transpose-20261122": {"brute": 7, "optimal": 8, "variation": 12},
        "lc94-inorder-iterative-20261123": {"brute": 7, "optimal": 8, "variation": 5},
        "radix-sort-20261124": {"brute": 4, "optimal": 10, "variation": 10},
        "shell-sort-20261125": {"brute": 10, "optimal": 9, "variation": 5},
        "tree-reconstruct-pre-in-20261126": {"brute": 4, "optimal": 4, "variation": 4},
        "threaded-binary-tree-20261201": {"brute": 5, "optimal": 8, "variation": 4},        "btree-search-20261202": {"brute": 2, "optimal": 2, "variation": 2},
        "linear-search-sentinel-20261203": {"brute": 5, "optimal": 6, "variation": 6},

    }
    for lesson in queue:
        for method, minimum in diagram_minimum.get(lesson["id"], {}).items():
            frames = lesson.get("animation", {}).get(method, [])
            if len(frames) < minimum:
                raise ValueError(
                    f"{lesson['id']}.{method}: 图/树动画帧数不足，至少需要{minimum}帧"
                )
            for index, frame in enumerate(frames):
                if not frame.get("diagram") or not frame.get("text"):
                    raise ValueError(
                        f"{lesson['id']}.{method}: 第{index + 1}帧缺少图/树连线说明"
                    )

    radix_lesson = next((x for x in queue if x["id"] == "radix-sort-20261124"), None)
    if radix_lesson is None:
        raise ValueError("缺少radix-sort-20261124")
    if radix_lesson.get("source") != "https://oi-wiki.org/basic/radix-sort/":
        raise ValueError("radix-sort-20261124: 来源必须直接覆盖LSD基数排序")
    if not all(term in radix_lesson.get("question", "") for term in ("输入格式：", "输出格式：")):
        raise ValueError("radix-sort-20261124: 输入/输出格式不完整")
    if not all(term in radix_lesson.get("sample", "") for term in ("边界：", "反例：")):
        raise ValueError("radix-sort-20261124: 缺少边界或稳定性反例")
    expected_radix_pointers = {
        "brute": [
            {"i": 1, "j": 0, "key": 45},
            {"i": 1, "j": -1, "key": 45},
            {"i": 5, "j": -1, "key": 24},
            {"i": 7, "j": 2, "key": 66},
        ],
        "optimal": [
            {"pass": 1, "exp": 1, "phase": "count", "i": 0, "digit": 0, "writeIndex": None},
            {"pass": 1, "exp": 1, "phase": "place", "i": 7, "digit": 6, "writeIndex": 7},
            {"pass": 1, "exp": 1, "phase": "copy", "i": -1, "digit": None, "writeIndex": 0},
            {"pass": 1, "exp": 10, "phase": "count", "i": 0, "digit": 7, "writeIndex": None},
            {"pass": 2, "exp": 10, "phase": "place", "i": 7, "digit": 6, "writeIndex": 4},
            {"pass": 2, "exp": 10, "phase": "copy", "i": -1, "digit": None, "writeIndex": 0},
            {"pass": 2, "exp": 100, "phase": "count", "i": 0, "digit": 8, "writeIndex": None},
            {"pass": 3, "exp": 100, "phase": "place", "i": 7, "digit": 0, "writeIndex": 5},
            {"pass": 3, "exp": 100, "phase": "copy", "i": -1, "digit": None, "writeIndex": 0},
            {"pass": 3, "exp": 1000, "phase": "done", "i": 8, "digit": None, "writeIndex": None},
        ],
        "variation": [
            {"pass": 1, "exp": 1, "phase": "count", "i": 0, "digit": 9, "writeIndex": None},
            {"pass": 1, "exp": 1, "phase": "place", "i": 6, "digit": 5, "writeIndex": 1},
            {"pass": 1, "exp": 1, "phase": "print", "i": 7, "digit": None, "writeIndex": None},
            {"pass": 1, "exp": 10, "phase": "print-complete", "i": 7, "digit": None, "writeIndex": None},
            {"pass": 2, "exp": 10, "phase": "place", "i": 6, "digit": 3, "writeIndex": 3},
            {"pass": 2, "exp": 10, "phase": "print", "i": 7, "digit": None, "writeIndex": None},
            {"pass": 2, "exp": 100, "phase": "print-complete", "i": 7, "digit": None, "writeIndex": None},
            {"pass": 3, "exp": 100, "phase": "place", "i": 6, "digit": 6, "writeIndex": 4},
            {"pass": 3, "exp": 100, "phase": "print", "i": 7, "digit": None, "writeIndex": None},
            {"pass": 3, "exp": 1000, "phase": "done", "i": 7, "digit": None, "writeIndex": None},
        ],
    }
    expected_radix_arrays = {
        "brute": [
            [170, 45, 75, 90, 802, 24, 2, 66],
            [45, 170, 75, 90, 802, 24, 2, 66],
            [24, 45, 75, 90, 170, 802, 2, 66],
            [2, 24, 45, 66, 75, 90, 170, 802],
        ],
        "optimal": [
            [170, 45, 75, 90, 802, 24, 2, 66],
            [170, 45, 75, 90, 802, 24, 2, 66],
            [170, 45, 75, 90, 802, 24, 2, 66],
            [170, 90, 802, 2, 24, 45, 75, 66],
            [170, 90, 802, 2, 24, 45, 75, 66],
            [170, 90, 802, 2, 24, 45, 75, 66],
            [802, 2, 24, 45, 66, 170, 75, 90],
            [802, 2, 24, 45, 66, 170, 75, 90],
            [802, 2, 24, 45, 66, 170, 75, 90],
            [2, 24, 45, 66, 75, 90, 170, 802],
        ],
        "variation": [
            [329, 457, 657, 839, 436, 720, 355],
            [329, 457, 657, 839, 436, 720, 355],
            [720, 355, 436, 457, 657, 329, 839],
            [720, 355, 436, 457, 657, 329, 839],
            [720, 355, 436, 457, 657, 329, 839],
            [720, 329, 436, 839, 355, 457, 657],
            [720, 329, 436, 839, 355, 457, 657],
            [720, 329, 436, 839, 355, 457, 657],
            [329, 355, 436, 457, 657, 720, 839],
            [329, 355, 436, 457, 657, 720, 839],
        ],
    }
    for method, expected in expected_radix_pointers.items():
        frames = radix_lesson.get("animation", {}).get(method, [])
        if [frame.get("pointers") for frame in frames] != expected:
            raise ValueError(f"radix-sort-20261124.{method}: 指针、数位或写入位置与实际循环不一致")
        if [frame.get("array") for frame in frames] != expected_radix_arrays[method]:
            raise ValueError(f"radix-sort-20261124.{method}: 数组状态与逐趟排序结果不一致")
        for index, frame in enumerate(frames):
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"radix-sort-20261124.{method}: 第{index + 1}帧缺少状态连线或操作高亮")


    shell_lesson = next((x for x in queue if x["id"] == "shell-sort-20261125"), None)
    if shell_lesson is None:
        raise ValueError("缺少shell-sort-20261125")
    if shell_lesson.get("source") != "https://oi-wiki.org/basic/shell-sort/":
        raise ValueError("shell-sort-20261125: 来源必须直接覆盖希尔排序与增量插入")
    if not all(term in shell_lesson.get("question", "") for term in ("输入格式：", "输出格式：", "n=1")):
        raise ValueError("shell-sort-20261125: 输入/输出或单元素处理说明不完整")
    if not all(term in shell_lesson.get("sample", "") for term in ("负数与重复值：", "边界：", "反例：")):
        raise ValueError("shell-sort-20261125: 缺少负数、边界或稳定性反例")
    if "最坏时间 O(n²)" not in shell_lesson["optimal"].get("complexity", ""):
        raise ValueError("shell-sort-20261125: 折半增量最坏复杂度说明不准确")
    if "if (n == 1)" not in shell_lesson["optimal"]["code"]:
        raise ValueError("shell-sort-20261125: n=1时必须输出唯一元素")
    expected_shell_brute_pointers = [
        {"i": 1, "j": 0, "key": 38, "phase": "compare"},
        {"i": 1, "j": -1, "key": 38, "phase": "inserted"},
        {"i": 2, "j": 1, "key": 65, "phase": "inserted"},
        {"i": 3, "j": 2, "key": 97, "phase": "inserted"},
        {"i": 4, "j": 2, "key": 76, "phase": "inserted"},
        {"i": 5, "j": -1, "key": 13, "phase": "inserted"},
        {"i": 6, "j": 0, "key": 27, "phase": "inserted"},
        {"i": 7, "j": 3, "key": 49, "phase": "inserted"},
        {"i": 8, "j": 4, "key": 55, "phase": "inserted"},
        {"i": 9, "j": -1, "key": 4, "phase": "inserted"},
    ]
    expected_shell_brute_arrays = [
        [49,38,65,97,76,13,27,49,55,4],
        [38,49,65,97,76,13,27,49,55,4],
        [38,49,65,97,76,13,27,49,55,4],
        [38,49,65,97,76,13,27,49,55,4],
        [38,49,65,76,97,13,27,49,55,4],
        [13,38,49,65,76,97,27,49,55,4],
        [13,27,38,49,65,76,97,49,55,4],
        [13,27,38,49,49,65,76,97,55,4],
        [13,27,38,49,49,55,65,76,97,4],
        [4,13,27,38,49,49,55,65,76,97],
    ]
    shell_brute_frames = shell_lesson["animation"]["brute"]
    if [f.get("pointers") for f in shell_brute_frames] != expected_shell_brute_pointers:
        raise ValueError("shell-sort-20261125.brute: i/j/key指针与直接插入排序步骤不一致")
    if [f.get("array") for f in shell_brute_frames] != expected_shell_brute_arrays:
        raise ValueError("shell-sort-20261125.brute: 逐帧数组状态错误")

    expected_shell_optimal_pointers = [
        {"gap":5,"i":5,"j":0,"key":13,"phase":"compare"},
        {"gap":5,"i":5,"j":-5,"key":13,"phase":"inserted"},
        {"gap":5,"i":10,"j":-1,"key":4,"phase":"pass_done"},
        {"gap":2,"i":2,"j":0,"key":49,"phase":"compare"},
        {"gap":2,"i":4,"j":-2,"key":4,"phase":"inserted"},
        {"gap":2,"i":10,"j":7,"key":76,"phase":"pass_done"},
        {"gap":1,"i":1,"j":0,"key":27,"phase":"compare"},
        {"gap":1,"i":2,"j":0,"key":13,"phase":"inserted"},
        {"gap":1,"i":10,"j":7,"key":76,"phase":"pass_done"},
    ]
    expected_shell_optimal_arrays = [
        [49,38,65,97,76,13,27,49,55,4],
        [13,38,65,97,76,49,27,49,55,4],
        [13,27,49,55,4,49,38,65,97,76],
        [13,27,49,55,4,49,38,65,97,76],
        [4,27,13,55,49,49,38,65,97,76],
        [4,27,13,49,38,55,49,65,97,76],
        [4,27,13,49,38,55,49,65,97,76],
        [4,13,27,49,38,55,49,65,97,76],
        [4,13,27,38,49,49,55,65,76,97],
    ]
    shell_optimal_frames = shell_lesson["animation"]["optimal"]
    if [f.get("pointers") for f in shell_optimal_frames] != expected_shell_optimal_pointers:
        raise ValueError("shell-sort-20261125.optimal: gap/i/j/key指针与实际增量趟不一致")
    if [f.get("array") for f in shell_optimal_frames] != expected_shell_optimal_arrays:
        raise ValueError("shell-sort-20261125.optimal: 每趟及中间数组状态错误")

    expected_shell_variation_pointers = [
        {"gap":2,"i":2,"j":0,"key":"(3,Y)","phase":"compare"},
        {"gap":2,"i":3,"j":1,"key":"(2,B)","phase":"compare"},
        {"gap":2,"i":3,"j":-1,"key":"(2,B)","phase":"shifted"},
        {"gap":2,"i":3,"j":-1,"key":"(2,B)","phase":"inserted"},
        {"gap":1,"i":4,"j":2,"key":"(3,X)","phase":"pass_done"},
    ]
    expected_shell_variation_arrays = [
        [2,3,3,2],
        [2,3,3,2],
        [2,3,3,3],
        [2,2,3,3],
        [2,2,3,3],
    ]
    shell_variation_frames = shell_lesson["animation"]["variation"]
    if [f.get("pointers") for f in shell_variation_frames] != expected_shell_variation_pointers:
        raise ValueError("shell-sort-20261125.variation: 标签记录的i/j/key指针不准确")
    if [f.get("array") for f in shell_variation_frames] != expected_shell_variation_arrays:
        raise ValueError("shell-sort-20261125.variation: 不稳定性演示的记录状态错误")
    for method in ("brute", "optimal", "variation"):
        for index, frame in enumerate(shell_lesson["animation"][method]):
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"shell-sort-20261125.{method}: 第{index + 1}帧缺少图示/说明/操作高亮")
            if any(i < 0 or i >= len(frame.get("array", [])) for i in frame["active"]):
                raise ValueError(f"shell-sort-20261125.{method}: 第{index + 1}帧高亮下标越界")

    inorder_lesson = next((x for x in queue if x["id"] == "lc94-inorder-iterative-20261123"), None)
    if inorder_lesson is None:
        raise ValueError("缺少lc94-inorder-iterative-20261123")
    if inorder_lesson.get("source") != "https://leetcode.com/problems/binary-tree-inorder-traversal/":
        raise ValueError("lc94-inorder-iterative-20261123: 来源必须指向力扣94官方题面")
    if not all(term in inorder_lesson.get("question", "") for term in ("输入格式：", "输出格式：")):
        raise ValueError("lc94-inorder-iterative-20261123: 输入/输出格式不完整")
    if not all(term in inorder_lesson.get("sample", "") for term in ("边界：", "反例：")):
        raise ValueError("lc94-inorder-iterative-20261123: 缺少边界或错误遍历顺序反例")
    expected_inorder_pointers = {
        "brute": [
            {"current": 1, "output": []}, {"current": 4, "output": []},
            {"current": 4, "output": [4]}, {"current": 2, "output": [4, 2]},
            {"current": 1, "output": [4, 2, 5, 1]},
            {"current": 3, "output": [4, 2, 5, 1, 3]},
            {"current": 0, "output": [4, 2, 5, 1, 3, 6]},
        ],
        "optimal": [
            {"current": 1, "stack": [], "output": []},
            {"current": 0, "stack": [1, 2, 4], "output": []},
            {"current": 0, "stack": [1, 2], "output": [4]},
            {"current": 5, "stack": [1], "output": [4, 2]},
            {"current": 0, "stack": [1], "output": [4, 2, 5]},
            {"current": 3, "stack": [], "output": [4, 2, 5, 1]},
            {"current": 6, "stack": [], "output": [4, 2, 5, 1, 3]},
            {"current": 0, "stack": [], "output": [4, 2, 5, 1, 3, 6]},
        ],
        "variation": [
            {"current": 1, "stack": [], "count": 0, "k": 3, "found": False, "result": None},
            {"current": 0, "stack": [1, 2, 4], "count": 0, "k": 3, "found": False, "result": None},
            {"current": 0, "stack": [1, 2], "count": 1, "k": 3, "found": False, "result": None},
            {"current": 5, "stack": [1], "count": 2, "k": 3, "found": False, "result": None},
            {"current": 5, "stack": [1], "count": 3, "k": 3, "found": True, "result": 5},
        ],
    }
    for method, expected in expected_inorder_pointers.items():
        frames = inorder_lesson.get("animation", {}).get(method, [])
        if [frame.get("pointers") for frame in frames] != expected:
            raise ValueError(f"lc94-inorder-iterative-20261123.{method}: 指针/栈/访问序列与中序执行步骤不一致")
        for index, frame in enumerate(frames):
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"lc94-inorder-iterative-20261123.{method}: 第{index + 1}帧缺少连线、说明或操作高亮")

    for lesson in queue:
        if lesson["id"] == "lc994-20261110":
            frames = lesson.get("animation", {}).get("optimal", [])
            expected_head = [0, 1, 2, 3, 5, 6]
            expected_tail = [1, 3, 4, 5, 6, 7]
            actual_head = [f.get("pointers", {}).get("head") for f in frames]
            actual_tail = [f.get("pointers", {}).get("tail") for f in frames]
            if actual_head != expected_head or actual_tail != expected_tail:
                raise ValueError(
                    f"{lesson['id']}: BFS动画head/tail与逐层出队、入队次数不符："
                    f"head={actual_head}, tail={actual_tail}"
                )
        if lesson["id"] == "aoe-critical-20261115":
            required = "每个事件都位于从源点1到汇点6的某条路径上"
            if required not in lesson.get("constraint", ""):
                raise ValueError(f"{lesson['id']}: 未说明ve/vl逆推所需的源汇可达约束")
        numeric_bounds = {
            "prim-20261112": "1≤w≤10^8",
            "huffman-20261113": "1≤w_i≤10^9",
            "dijkstra-20261114": "0≤w≤10^8",
        }
        required_bound = numeric_bounds.get(lesson["id"])
        if required_bound and required_bound not in lesson.get("constraint", ""):
            raise ValueError(f"{lesson['id']}: 缺少与INF/整数范围匹配的权值约束")
        if lesson["id"] in ("prim-20261112", "dijkstra-20261114"):
            for method in ("brute", "optimal", "variation"):
                if "#define INF 1000000000" not in lesson[method]["code"]:
                    raise ValueError(f"{lesson['id']}.{method}: INF与题目约束不一致")
        if lesson["id"] == "huffman-20261113":
            for method in ("brute", "optimal", "variation"):
                if "long long" not in lesson[method]["code"]:
                    raise ValueError(f"{lesson['id']}.{method}: 合并权值/WPL应使用long long")
        if lesson["id"] == "lc622-20261107":
            # 力扣622的完整接口还必须包含判空和判满，且三份C程序的main内有状态断言。
            for method in ("brute", "optimal", "variation"):
                code = lesson[method]["code"]
                if "int isEmpty(" not in code or "int isFull(" not in code:
                    raise ValueError(f"{lesson['id']}.{method}: 缺少isEmpty/isFull接口")
                if "Front(&q) != -1" not in code or "Rear(&q) != -1" not in code:
                    raise ValueError(f"{lesson['id']}.{method}: 缺少空队列Front/Rear边界断言")
        requirements = animation_minimum.get(lesson["id"], {})
        for method, minimum in requirements.items():
            frames = lesson.get("animation", {}).get(method, [])
            if len(frames) < minimum:
                raise ValueError(
                    f"{lesson['id']}.{method}: 动画只有{len(frames)}帧，至少需要{minimum}帧"
                )
            for index, frame in enumerate(frames):
                if not frame.get("text") or not (
                    frame.get("pointers") or frame.get("diagram") or frame.get("array")
                ):
                    raise ValueError(
                        f"{lesson['id']}.{method}: 第{index + 1}帧缺少说明或状态/指针"
                    )
    # 本轮重点题目的逐帧动画必须同时保留指针位置与操作高亮。
    controlled_animation = {
        "lc997-20261109": ("brute", "optimal"),
        "lc994-20261110": ("brute", "optimal"),
        "dijkstra-20261114": ("brute", "optimal", "variation"),
        "aoe-critical-20261115": ("brute", "optimal", "variation"),
        "quick-sort-20261117": ("brute", "optimal", "variation"),
        "floyd-20261118": ("brute", "optimal", "variation"),
        "tree-level-order-20261119": ("brute", "optimal", "variation"),
        "lc-hash-linear-20261116": ("brute", "optimal", "variation"),
        "two-stacks-one-array-20261120": ("brute", "optimal", "variation"),
        "sliding-window-max-20261121": ("brute", "optimal", "variation"),
        "sparse-fast-transpose-20261122": ("brute", "optimal", "variation"),
        "lc94-inorder-iterative-20261123": ("brute", "optimal", "variation"),
        "radix-sort-20261124": ("brute", "optimal", "variation"),
        "shell-sort-20261125": ("brute", "optimal", "variation"),
        "tree-reconstruct-pre-in-20261126": ("brute", "optimal", "variation"),
    }
    reviewed_variations = {
        "lc997-20261109", "lc994-20261110", "kmp-20261111",
        "prim-20261112", "huffman-20261113", "dijkstra-20261114",
        "tree-level-order-20261119",
        "aoe-critical-20261115", "lc-hash-linear-20261116",
        "quick-sort-20261117", "floyd-20261118",
        "two-stacks-one-array-20261120", "sliding-window-max-20261121",
        "sparse-fast-transpose-20261122",
        "lc94-inorder-iterative-20261123", "radix-sort-20261124",
        "shell-sort-20261125", "tree-reconstruct-pre-in-20261126",
    }
    for lesson in queue:
        if lesson["id"] in reviewed_variations and not lesson.get("variation", {}).get("complexity"):
            raise ValueError(f"{lesson['id']}: 变式缺少时间/空间复杂度")
        for method in controlled_animation.get(lesson["id"], ()):
            frames = lesson.get("animation", {}).get(method, [])
            for index, frame in enumerate(frames):
                if not isinstance(frame.get("pointers"), dict) or not isinstance(frame.get("active"), list):
                    raise ValueError(
                        f"{lesson['id']}.{method}: 第{index + 1}帧缺少指针或操作高亮"
                    )
    huffman_lesson = next((x for x in queue if x["id"] == "huffman-20261113"), None)
    if huffman_lesson is None:
        raise ValueError("缺少huffman-20261113")
    huffman_brute = huffman_lesson["animation"]["brute"]
    expected_huffman_active = [[0, 1], [0, 1], [0, 2], [1, 2], [0, 1]]
    if [f.get("active") for f in huffman_brute] != expected_huffman_active:
        raise ValueError("huffman-20261113.brute: 第3轮合并14和16时必须高亮数组下标2和0")
    if huffman_brute[2].get("array") != [16, 45, 14, 25]:
        raise ValueError("huffman-20261113.brute: 第3轮活动森林数组状态错误")
    if huffman_brute[2].get("pointers") != {
        "left": 14, "right": 16, "parent": 30, "leftIndex": 2, "rightIndex": 0
    }:
        raise ValueError("huffman-20261113.brute: 第3轮左右最小权值指针错误")
    if "WPL=416" not in huffman_lesson.get("sample", ""):
        raise ValueError("huffman-20261113: 缺少取最大权值的具体错误反例")
    dijkstra_lesson = next((x for x in queue if x["id"] == "dijkstra-20261114"), None)
    if dijkstra_lesson is None or "0 4 -1" not in dijkstra_lesson.get("sample", ""):
        raise ValueError("dijkstra-20261114: 缺少不可达顶点输出-1的具体边界")
    hash_lesson = next((x for x in queue if x["id"] == "lc-hash-linear-20261116"), None)
    if hash_lesson is None or hash_lesson.get("source") != "https://www.cs.hmc.edu/courses/current.then/cs70/lessons/week12/lesson2/linearprobing/":
        raise ValueError("lc-hash-linear-20261116: 来源必须直接讲解线性探测")
    if not all(term in hash_lesson.get("question", "") for term in ("输入格式：", "输出格式：")):
        raise ValueError("lc-hash-linear-20261116: 缺少明确输入/输出格式")
    if "反例：" not in hash_lesson.get("sample", "") or "边界：" not in hash_lesson.get("sample", ""):
        raise ValueError("lc-hash-linear-20261116: 缺少负例或边界样例")
    floyd_lesson = next((x for x in queue if x["id"] == "floyd-20261118"), None)
    if floyd_lesson is None or "0 4 2" not in floyd_lesson.get("sample", ""):
        raise ValueError("floyd-20261118: 缺少负权边且无负环的具体样例")
    if "反例：" not in floyd_lesson.get("sample", "") or "负权回路" not in floyd_lesson.get("sample", ""):
        raise ValueError("floyd-20261118: 缺少负权回路非法输入反例")

    variation_traces = {
        "dijkstra-20261114": (
            [
                {"u": 0, "v": -1, "visited": []},
                {"u": 0, "v": 2, "visited": [0]},
                {"u": 2, "v": 3, "visited": [0, 2]},
                {"u": 1, "v": 3, "visited": [0, 2, 1]},
                {"u": 3, "v": -1, "visited": [0, 2, 1, 3]},
            ],
            [
                [0, "∞", "∞", "∞"],
                [0, 4, 1, "∞"],
                [0, 3, 1, 6],
                [0, 3, 1, 4],
                [0, 3, 1, 4],
            ],
        ),
        "aoe-critical-20261115": (
            [
                {"u": 1, "front": 0, "rear": 1},
                {"u": 1, "v": 3, "front": 1, "rear": 3},
                {"u": 2, "v": 5, "front": 2, "rear": 3},
                {"u": 3, "v": 4, "front": 3, "rear": 5},
                {"u": 4, "v": 6, "front": 4, "rear": 5},
                {"u": 5, "v": 6, "front": 5, "rear": 6},
                {"u": 1, "phase": "reverse"},
                {"u": 1, "v": 4, "path": [1, 2, 4, 6]},
            ],
            [
                [0, 0, 0, 0, 0, 0],
                [0, 3, 2, 0, 0, 0],
                [0, 3, 2, 5, 6, 0],
                [0, 3, 2, 5, 6, 0],
                [0, 3, 2, 5, 6, 8],
                [0, 3, 2, 5, 6, 8],
                [0, 3, 2, 5, 6, 8],
                [0, 3, 2, 5, 6, 8],
            ],
        ),
        "quick-sort-20261117": (
            [
                {"low": 0, "high": 5, "pivot": 3, "i": 0, "j": 5},
                {"low": 0, "high": 5, "pivot": 3, "i": 1, "j": 4},
                {"low": 0, "high": 5, "pivot": 3, "i": 3, "j": 3},
                {"low": 0, "high": 3, "pivot": -1, "i": 1, "j": 1},
                {"low": 0, "high": 3, "pivot": -1, "i": 2, "j": 0},
                {"low": 2, "high": 3, "pivot": 2, "i": 3, "j": 2},
                {"low": 4, "high": 5, "pivot": 3, "i": 5, "j": 4},
            ],
            [
                [3, -1, 3, 0, -1, 2],
                [2, -1, 3, 0, -1, 3],
                [2, -1, -1, 0, 3, 3],
                [-1, -1, 2, 0, 3, 3],
                [-1, -1, 2, 0, 3, 3],
                [-1, -1, 0, 2, 3, 3],
                [-1, -1, 0, 2, 3, 3],
            ],
        ),
        "floyd-20261118": (
            [
                {"k": -1, "i": -1, "j": -1},
                {"k": 0, "i": 0, "j": 0},
                {"k": 1, "i": 0, "j": 2},
                {"k": 2, "i": 0, "j": 2},
            ],
            [
                [[0, 4, 5], ["∞", 0, -2], ["∞", "∞", 0]],
                [[0, 4, 5], ["∞", 0, -2], ["∞", "∞", 0]],
                [[0, 4, 2], ["∞", 0, -2], ["∞", "∞", 0]],
                [[0, 4, 2], ["∞", 0, -2], ["∞", "∞", 0]],
            ],
        ),
    }
    for lesson_id, (expected_pointers, expected_arrays) in variation_traces.items():
        lesson = next((x for x in queue if x["id"] == lesson_id), None)
        frames = lesson.get("animation", {}).get("variation", []) if lesson else []
        if [f.get("pointers") for f in frames] != expected_pointers:
            raise ValueError(f"{lesson_id}.variation: 指针轨迹与真实执行顺序不一致")
        if [f.get("array") for f in frames] != expected_arrays:
            raise ValueError(f"{lesson_id}.variation: 数组/矩阵状态与真实执行结果不一致")
        for index, frame in enumerate(frames):
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"{lesson_id}.variation: 第{index + 1}帧缺少连线/说明/操作高亮")

    stacks_lesson = next((x for x in queue if x["id"] == "two-stacks-one-array-20261120"), None)
    if stacks_lesson is None:
        raise ValueError("缺少two-stacks-one-array-20261120")
    stack_variation = stacks_lesson.get("animation", {}).get("variation", [])
    expected_stack_tops = [
        {"top1": -1, "top2": 6},
        {"top1": 0, "top2": 6},
        {"top1": 0, "top2": 5},
        {"top1": 1, "top2": 5},
        {"top1": 1, "top2": 6, "popped": 9},
        {"top1": 1, "top2": 5},
        {"top1": 2, "top2": 5},
        {"top1": 1, "top2": 5, "popped": 3},
        {"top1": 1, "top2": 6, "popped": 8},
    ]
    if [f.get("pointers") for f in stack_variation] != expected_stack_tops:
        raise ValueError("two-stacks-one-array-20261120.variation: top1/top2与Push/Pop顺序不一致")
    if "\\n" in stacks_lesson.get("sample", ""):
        raise ValueError("two-stacks-one-array-20261120: 示例文本含字面\\n，换行应为真实换行")
    for index, frame in enumerate(stack_variation):
        if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
            raise ValueError(f"two-stacks-one-array-20261120.variation: 第{index + 1}帧缺少连线/高亮")

    sliding_lesson = next((x for x in queue if x["id"] == "sliding-window-max-20261121"), None)
    if sliding_lesson is None:
        raise ValueError("缺少sliding-window-max-20261121")
    if sliding_lesson.get("source") != "https://leetcode.cn/problems/sliding-window-maximum/":
        raise ValueError("sliding-window-max-20261121: 来源必须指向力扣239官方题面")
    if not all(term in sliding_lesson.get("question", "") for term in ("输入格式：", "输出格式：")):
        raise ValueError("sliding-window-max-20261121: 缺少输入/输出格式")
    if "边界1：" not in sliding_lesson.get("sample", "") or "反例：" not in sliding_lesson.get("sample", ""):
        raise ValueError("sliding-window-max-20261121: 缺少边界或反例")
    sliding_frames = sliding_lesson.get("animation", {})
    if [f.get("pointers", {}).get("i") for f in sliding_frames.get("optimal", [])] != list(range(8)):
        raise ValueError("sliding-window-max-20261121.optimal: i指针轨迹错误")
    expected_deques = [[0], [1], [1, 2], [1, 2, 3], [4], [4, 5], [6], [7]]
    if [f.get("pointers", {}).get("deque") for f in sliding_frames.get("optimal", [])] != expected_deques:
        raise ValueError("sliding-window-max-20261121.optimal: 单调队列状态错误")
    if [f.get("pointers", {}).get("topIndex") for f in sliding_frames.get("variation", [])] != [0, 1, 1, 1, 4, 4, 6, 7]:
        raise ValueError("sliding-window-max-20261121.variation: 最大堆堆顶下标轨迹错误")
    expected_brute = []
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    for left in range(len(nums) - k + 1):
        max_index = left
        for j in range(left, left + k):
            if nums[j] > nums[max_index]:
                max_index = j
            expected_brute.append({"left": left, "right": left + k - 1,
                                   "j": j, "maxIndex": max_index})
    if [f.get("pointers") for f in sliding_frames.get("brute", [])] != expected_brute:
        raise ValueError("sliding-window-max-20261121.brute: 窗口扫描指针或最大值位置错误")
    expected_head = [0, 0, 0, 0, 1, 1, 1, 1]
    expected_tail = [1, 1, 2, 3, 2, 3, 2, 2]
    expected_expired = [[], [], [], [], [1], [], [], []]
    expected_removed = [[], [0], [], [], [3, 2], [], [5, 4], [6]]
    for key, expected in (("head", expected_head), ("tail", expected_tail),
                          ("expired", expected_expired), ("removedBack", expected_removed)):
        if [f.get("pointers", {}).get(key) for f in sliding_frames.get("optimal", [])] != expected:
            raise ValueError(f"sliding-window-max-20261121.optimal: {key}轨迹错误")
    for method in ("brute", "optimal", "variation"):
        for index, frame in enumerate(sliding_frames.get(method, [])):
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"sliding-window-max-20261121.{method}: 第{index + 1}帧缺少数组连线/操作高亮")
    quick_lesson = next((x for x in queue if x["id"] == "quick-sort-20261117"), None)
    if quick_lesson is None:
        raise ValueError("缺少quick-sort-20261117，无法审核快速排序动画")
    expected_quick_brute = [
        {"array": [5,1,8,3,2,7,4,6], "pointers": {"end":7,"j":0,"swapped":False}},
        {"array": [1,5,3,2,7,4,6,8], "pointers": {"end":7,"j":6,"swapped":True}},
        {"array": [1,3,2,5,4,6,7,8], "pointers": {"end":6,"j":5,"swapped":True}},
        {"array": [1,2,3,4,5,6,7,8], "pointers": {"end":5,"j":4,"swapped":True}},
        {"array": [1,2,3,4,5,6,7,8], "pointers": {"end":4,"j":3,"swapped":False}},
        {"array": [1,2,3,4,5,6,7,8], "pointers": {"end":4,"j":3,"swapped":False}},
    ]
    expected_quick_optimal = [
        {"array": [5,1,8,3,2,7,4,6], "pointers": {"low":0,"high":7,"pivot":3,"i":0,"j":4}},
        {"array": [2,1,8,3,5,7,4,6], "pointers": {"low":0,"high":7,"pivot":3,"i":1,"j":3}},
        {"array": [2,1,3,8,5,7,4,6], "pointers": {"low":0,"high":7,"pivot":3,"i":3,"j":2}},
        {"array": [1,2,3,8,5,7,4,6], "pointers": {"low":0,"high":2,"pivot":1,"i":1,"j":0}},
        {"array": [1,2,3,8,5,7,4,6], "pointers": {"low":1,"high":2,"pivot":2,"i":2,"j":0}},
        {"array": [1,2,3,6,5,7,4,8], "pointers": {"low":3,"high":7,"pivot":7,"i":4,"j":6}},
        {"array": [1,2,3,6,5,4,7,8], "pointers": {"low":3,"high":7,"pivot":7,"i":6,"j":5}},
        {"array": [1,2,3,4,5,6,7,8], "pointers": {"low":3,"high":5,"pivot":5,"i":4,"j":4}},
        {"array": [1,2,3,4,5,6,7,8], "pointers": {"low":3,"high":5,"pivot":5,"i":5,"j":3}},
        {"array": [1,2,3,4,5,6,7,8], "pointers": {"low":6,"high":7,"pivot":7,"i":7,"j":5}},
    ]
    expected_quick_variation = [
        {"array": [3,-1,3,0,-1,2], "pointers": {"low":0,"high":5,"pivot":3,"i":0,"j":5}},
        {"array": [2,-1,3,0,-1,3], "pointers": {"low":0,"high":5,"pivot":3,"i":1,"j":4}},
        {"array": [2,-1,-1,0,3,3], "pointers": {"low":0,"high":5,"pivot":3,"i":3,"j":3}},
        {"array": [-1,-1,2,0,3,3], "pointers": {"low":0,"high":3,"pivot":-1,"i":1,"j":1}},
        {"array": [-1,-1,2,0,3,3], "pointers": {"low":0,"high":3,"pivot":-1,"i":2,"j":0}},
        {"array": [-1,-1,0,2,3,3], "pointers": {"low":2,"high":3,"pivot":2,"i":3,"j":2}},
        {"array": [-1,-1,0,2,3,3], "pointers": {"low":4,"high":5,"pivot":3,"i":5,"j":4}},
    ]
    for method, expected in (("brute", expected_quick_brute), ("optimal", expected_quick_optimal), ("variation", expected_quick_variation)):
        frames = quick_lesson.get("animation", {}).get(method, [])
        actual = [{"array": frame.get("array"), "pointers": frame.get("pointers")} for frame in frames]
        if actual != expected:
            raise ValueError(f"quick-sort-20261117.{method}: 动画数组或指针与真实排序步骤不一致")
        for index, frame in enumerate(frames):
            if not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"quick-sort-20261117.{method}: 第{index + 1}帧缺少说明或操作高亮")
            if any(pos < 0 or pos >= len(frame["array"]) for pos in frame["active"]):
                raise ValueError(f"quick-sort-20261117.{method}: 第{index + 1}帧高亮下标越界")
    for method in ("optimal", "variation"):
        code = quick_lesson[method]["code"]
        for required in ("if (low >= high)", "pivot", "相等", "i++;", "j--;"):
            if required not in code:
                raise ValueError(f"quick-sort-20261117.{method}: 缺少关键边界/重复值解释 {required!r}")
    aoe_lesson = next((x for x in queue if x["id"] == "aoe-critical-20261115"), None)
    if aoe_lesson is None or aoe_lesson.get("source") != "https://m.biancheng.net/view/3417.html":
        raise ValueError("aoe-critical-20261115: 来源必须直达AOE网与关键路径讲解")
    kmp_lesson = next((x for x in queue if x["id"] == "kmp-20261111"), None)
    if kmp_lesson is None or "输入格式" not in kmp_lesson.get("question", "") or "输出格式" not in kmp_lesson.get("question", ""):
        raise ValueError("kmp-20261111: 缺少明确输入/输出格式")
    for method in ("brute", "optimal", "variation"):
        code = kmp_lesson[method]["code"]
        if 'scanf("%1000s %1000s"' not in code:
            raise ValueError(f"kmp-20261111.{method}: 必须从标准输入读取主串和模式串")
    # 近期静态演示题必须明确写出“无输入”和输出格式，不能只暗示数据内置。
    for lesson_id in (
        "prim-20261112", "huffman-20261113", "dijkstra-20261114",
        "aoe-critical-20261115", "tree-level-order-20261119",
    ):
        item = next((x for x in queue if x["id"] == lesson_id), None)
        if item is None or "输入格式：" not in item.get("question", "") or "输出格式：" not in item.get("question", ""):
            raise ValueError(f"{lesson_id}: 缺少明确输入/输出格式")
    tree_lesson = next((x for x in queue if x["id"] == "tree-level-order-20261119"), None)
    if tree_lesson is None or tree_lesson.get("source") != "https://leetcode.cn/problems/binary-tree-level-order-traversal/description/":
        raise ValueError("tree-level-order-20261119: 必须链接力扣102官方题面")
    if "边界：" not in tree_lesson.get("sample", "") or "反例：" not in tree_lesson.get("sample", ""):
        raise ValueError("tree-level-order-20261119: 缺少单结点/空树边界或DFS反例")
    tree_animation = tree_lesson.get("animation", {})
    expected_tree_pointers = {
        "brute": [{"level": 1, "node": 0}, {"level": 2, "node": 1},
                  {"level": 3, "node": 3}, {"height": 3, "level": 3}],
        "optimal": [{"front": 0, "rear": 1}, {"front": 1, "rear": 3},
                    {"front": 2, "rear": 5}, {"front": 3, "rear": 6},
                    {"front": 6, "rear": 6}],
        "variation": [{"front": 0, "rear": 1, "maxWidth": 1},
                      {"front": 1, "rear": 3, "maxWidth": 2},
                      {"front": 3, "rear": 6, "maxWidth": 3},
                      {"front": 6, "rear": 6, "maxWidth": 3}],
    }
    for method, expected in expected_tree_pointers.items():
        frames = tree_animation.get(method, [])
        actual = [frame.get("pointers") for frame in frames]
        if actual != expected:
            raise ValueError(f"tree-level-order-20261119.{method}: 动画指针与递归/队列执行顺序不一致")
        for index, frame in enumerate(frames):
            if not frame.get("diagram") or not isinstance(frame.get("active"), list):
                raise ValueError(f"tree-level-order-20261119.{method}: 第{index + 1}帧缺少树连线或操作高亮")

    reconstruction_lesson = next((x for x in queue if x["id"] == "tree-reconstruct-pre-in-20261126"), None)
    if reconstruction_lesson is None:
        raise ValueError("缺少tree-reconstruct-pre-in-20261126")
    if reconstruction_lesson.get("source") != "https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/description/":
        raise ValueError("tree-reconstruct-pre-in-20261126: 来源必须指向力扣105官方题面")
    if not all(term in reconstruction_lesson.get("question", "") for term in ("输入格式：无", "输出格式：")):
        raise ValueError("tree-reconstruct-pre-in-20261126: 静态演示题必须明确输入/输出格式")
    if "1≤n≤26" not in reconstruction_lesson.get("constraint", ""):
        raise ValueError("tree-reconstruct-pre-in-20261126: 大写唯一字符集的n上限必须为26")
    if not all(term in reconstruction_lesson.get("sample", "") for term in ("正例：", "边界：", "反例：")):
        raise ValueError("tree-reconstruct-pre-in-20261126: 缺少正例、边界或仅凭先序无法定树形的反例")
    expected_reconstruction_pointers = {
        "brute": [
            {"preL": 0, "inL": 0, "inR": 5, "root": "A"},
            {"root": "A", "k": 3, "leftSize": 3},
            {"root": "B", "inL": 0, "inR": 2, "k": 1},
            {"phase": "complete"},
        ],
        "optimal": [
            {"phase": "index", "i": 5},
            {"preIndex": 1, "root": "A", "k": 3},
            {"root": "B", "posB": 1, "preIndex": 2, "phase": "recursive"},
            {"phase": "complete", "preIndex": 6},
        ],
        "variation": [
            {"postIndex": 5, "root": "A"},
            {"root": "C", "posC": 4, "phase": "right"},
            {"root": "B", "posB": 1, "phase": "left"},
            {"phase": "complete", "postIndex": -1},
        ],
    }
    expected_reconstruction_arrays = {
        "brute": [
            ["A", "B", "D", "E", "C", "F"],
            ["D", "B", "E", "A", "C", "F"],
            ["A", "B", "D", "E", "C", "F"],
            ["D", "E", "B", "F", "C", "A"],
        ],
        "optimal": [
            ["D", "B", "E", "A", "C", "F"],
            ["A", "B", "D", "E", "C", "F"],
            ["A", "B", "D", "E", "C", "F"],
            ["D", "E", "B", "F", "C", "A"],
        ],
        "variation": [
            ["D", "E", "B", "F", "C", "A"],
            ["C", "F"],
            ["D", "B", "E"],
            ["A", "B", "D", "E", "C", "F"],
        ],
    }
    for method, expected in expected_reconstruction_pointers.items():
        frames = reconstruction_lesson.get("animation", {}).get(method, [])
        if [frame.get("pointers") for frame in frames] != expected:
            raise ValueError(f"tree-reconstruct-pre-in-20261126.{method}: 递归区间/索引指针轨迹错误")
        if [frame.get("array") for frame in frames] != expected_reconstruction_arrays[method]:
            raise ValueError(f"tree-reconstruct-pre-in-20261126.{method}: 遍历序列状态错误")
        for index, frame in enumerate(frames):
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"tree-reconstruct-pre-in-20261126.{method}: 第{index + 1}帧缺少连线、说明或高亮")

    sparse_lesson = next((x for x in queue if x["id"] == "sparse-fast-transpose-20261122"), None)
    if sparse_lesson is None:
        raise ValueError("缺少sparse-fast-transpose-20261122")
    if sparse_lesson.get("source") != "https://blog.nerom.wang/2015/02/02/sparse-matrix":
        raise ValueError("sparse-fast-transpose-20261122: 来源链接错误")
    if not all(term in sparse_lesson.get("question", "") for term in ("输入格式：", "输出格式：")):
        raise ValueError("sparse-fast-transpose-20261122: 缺少输入/输出格式")
    if not all(term in sparse_lesson.get("sample", "") for term in ("正例：", "反例：", "边界：")):
        raise ValueError("sparse-fast-transpose-20261122: 缺少正例、反例或边界样例")
    if "cpot[0]=0" not in sparse_lesson.get("constraint", ""):
        raise ValueError("sparse-fast-transpose-20261122: 未明确0-based cpot定义")
    if not sparse_lesson.get("variation", {}).get("complexity"):
        raise ValueError("sparse-fast-transpose-20261122: 变式缺少复杂度")
    sparse_expected = {
        "brute": [
            {"column": 0, "scan": 0, "write": 0},
            {"column": 0, "scan": 2, "write": 0},
            {"column": 1, "scan": 0, "write": 1},
            {"column": 1, "scan": 4, "write": 2},
            {"column": 2, "scan": 5, "write": 3},
            {"column": 3, "scan": 1, "write": 3},
            {"column": 4, "scan": 3, "write": 4},
        ],
        "optimal": [
            {"phase": "count", "p": 4, "num": [1, 2, 0, 1, 1]},
            {"phase": "prefix", "p": 4, "cpot": [0, 1, 3, 3, 4]},
            {"phase": "copy", "p": -1, "nextPos": [0, 1, 3, 3, 4]},
            {"phase": "place", "p": 0, "column": 1, "writeIndex": 1, "nextPos": [0, 2, 3, 3, 4]},
            {"phase": "place", "p": 1, "column": 3, "writeIndex": 3, "nextPos": [0, 2, 3, 4, 4]},
            {"phase": "place", "p": 2, "column": 0, "writeIndex": 0, "nextPos": [1, 2, 3, 4, 4]},
            {"phase": "place", "p": 3, "column": 4, "writeIndex": 4, "nextPos": [1, 2, 3, 4, 5]},
            {"phase": "place", "p": 4, "column": 1, "writeIndex": 2, "nextPos": [1, 3, 3, 4, 5]},
        ],
        "variation": [
            {"phase": "init", "p": -1, "head": [-1, -1, -1, -1, -1], "tail": [-1, -1, -1, -1, -1]},
            {"phase": "append", "p": 0, "column": 1, "head": [-1, 0, -1, -1, -1], "tail": [-1, 0, -1, -1, -1], "next": [-1, -1, -1, -1, -1]},
            {"phase": "append", "p": 1, "column": 3, "head": [-1, 0, -1, 1, -1], "tail": [-1, 0, -1, 1, -1], "next": [-1, -1, -1, -1, -1]},
            {"phase": "append", "p": 2, "column": 0, "head": [2, 0, -1, 1, -1], "tail": [2, 0, -1, 1, -1], "next": [-1, -1, -1, -1, -1]},
            {"phase": "append", "p": 3, "column": 4, "head": [2, 0, -1, 1, 3], "tail": [2, 0, -1, 1, 3], "next": [-1, -1, -1, -1, -1]},
            {"phase": "append", "p": 4, "column": 1, "head": [2, 0, -1, 1, 3], "tail": [2, 4, -1, 1, 3], "next": [4, -1, -1, -1, -1]},
            {"phase": "collect", "column": 0, "p": 2, "write": 0},
            {"phase": "collect", "column": 1, "p": 0, "write": 1},
            {"phase": "collect", "column": 1, "p": 4, "write": 2},
            {"phase": "collect", "column": 2, "p": -1, "write": 3},
            {"phase": "collect", "column": 3, "p": 1, "write": 3},
            {"phase": "collect", "column": 4, "p": 3, "write": 4},
        ],
    }
    for method, expected in sparse_expected.items():
        frames = sparse_lesson.get("animation", {}).get(method, [])
        if [frame.get("pointers") for frame in frames] != expected:
            raise ValueError(f"sparse-fast-transpose-20261122.{method}: 指针/桶位置与算法步骤不一致")
        for index, frame in enumerate(frames):
            if frame.get("array") != [1, 3, 0, 4, 1]:
                raise ValueError(f"sparse-fast-transpose-20261122.{method}: 第{index + 1}帧输入列号数组错误")
            if not frame.get("diagram") or not frame.get("text") or not isinstance(frame.get("active"), list):
                raise ValueError(f"sparse-fast-transpose-20261122.{method}: 第{index + 1}帧缺少连线/说明/高亮")

    inputs = {
        "kmp-20261111": "ababcabcac\nabcac\n",
        "lc217-20261027": "4\n1 2 3 1\n",
        "lc997-20261109": "3 2\n1 3\n2 3\n",
        "lc-hash-linear-20261116": "7 5\n5 20016 40027 17 20028 -3 8\n40027 5 99 -3 20028\n",
        "lc994-20261110": "3 3\n2 1 1\n1 1 0\n0 1 1\n",
        "lc503-20261106": "3\n1 2 1\n",
        "quick-sort-20261117": "8\n5 1 8 3 2 7 4 6\n",
        "floyd-20261118": "4 5\n1 2 5\n1 3 10\n2 3 3\n2 4 9\n3 4 1\n",
        "sliding-window-max-20261121": "8 3\n1 3 -1 -3 5 3 6 7\n",
        "sparse-fast-transpose-20261122": "4 5 5\n0 1 12\n0 3 9\n2 0 -3\n2 4 14\n3 1 24\n",
        "lc94-inorder-iterative-20261123": "6 1\n1 2 3\n2 4 5\n3 0 6\n4 0 0\n5 0 0\n6 0 0\n",
        "radix-sort-20261124": "8\n170 45 75 90 802 24 2 66\n",
        "shell-sort-20261125": "10\n49 38 65 97 76 13 27 49 55 4\n",
        "complete-tree-bfs-20261128": "6\n2 3\n4 5\n6 0\n0 0\n0 0\n0 0\n",
        "selection-sort-20261129": "5\n64 25 12 22 11\n",
        "avl-insert-20261130": "6\n30 20 10 25 28 27\n",
        "threaded-binary-tree-20261201": "7 1\n4 2 3\n2 4 5\n6 6 7\n1 0 0\n3 0 0\n5 0 0\n7 0 0\n",        "btree-search-20261202": "4 4 1 50\n2 30 60 2 3 4\n2 10 20 0 0 0\n2 40 50 0 0 0\n2 70 80 0 0 0\n",
        "linear-search-sentinel-20261203": "6\n8 3 5 1 9 2\n9\n",

    }
    variant_inputs = { "kmp-20261111": "aaaaab\naaab\n","lc-hash-linear-20261116": "7 5\n5 20016 40027 17 20028 -3 8\n40027 5 99 -3 20028\n",
                      "lc997-20261109": "3 3\n1 3\n2 3\n3 1\n",
                      "lc994-20261110": "2 2\n2 0\n0 1\n",
                      "lc503-20261106": "5\n3 8 4 1 2\n", "quick-sort-20261117": "6\n3 -1 3 0 -1 2\n", "floyd-20261118": "3 3\n1 2 4\n2 3 -2\n1 3 5\n", "sliding-window-max-20261121": "8 3\n1 3 -1 -3 5 3 6 7\n",
                      "sparse-fast-transpose-20261122": "3 4 4\n0 1 5\n1 0 -2\n1 3 8\n2 1 7\n",
                      "lc94-inorder-iterative-20261123": "6 1 3\n1 2 3\n2 4 5\n3 0 6\n4 0 0\n5 0 0\n6 0 0\n",
                      "complete-tree-bfs-20261128": "5\n2 3\n4 5\n0 0\n0 0\n0 0\n",
                      "selection-sort-20261129": "4\n2 1\n1 2\n2 3\n1 4\n", "avl-insert-20261130": "6 1\n25 2 3\n20 4 0\n28 5 6\n10 0 0\n27 0 0\n30 0 0\n", "threaded-binary-tree-20261201": "7 1 3\n4 2 3\n2 4 5\n6 6 7\n1 0 0\n3 0 0\n5 0 0\n7 0 0\n"                      "btree-search-20261202": "4 4 1 55\n2 30 60 2 3 4\n2 10 20 0 0 0\n2 40 50 0 0 0\n2 70 80 0 0 0\n",
                      "linear-search-sentinel-20261203": "5\n4 2 4 4 7\n4\n"
}
    count = 0
    for x in queue:
        case = CASES.get(x["id"])
        if not case:
            raise ValueError(f"未给题目 {x['id']} 配置预期输出，请先审核")
        if len(case) >= 3:
            expected_brute, expected_optimal, expected_variation = case[:3]
        else:
            # 旧题的朴素解与优化解输出相同，沿用二元组配置。
            expected_brute = expected_optimal = case[0]
            expected_variation = case[1]
        check_one(x["brute"]["code"], expected_brute, x["id"] + ".brute",
                  inputs.get(x["id"], ""))
        count += 1
        check_one(x["optimal"]["code"], expected_optimal, x["id"] + ".optimal",
                  inputs.get(x["id"], ""))
        count += 1
        check_one(x["variation"]["code"], expected_variation, x["id"] + ".variation",
                  variant_inputs.get(x["id"], ""))
        count += 1
        if x["id"] == "complete-tree-bfs-20261128":
            # 空树、单结点和“左侧缺口后仍有右孩子”是完全二叉树判定的关键边界。
            empty = "0\n"
            single = "1\n0 0\n"
            incomplete = "5\n2 3\n0 5\n0 0\n0 0\n0 0\n"
            for method, expected in (("brute", "朴素法：YES"), ("optimal", "优化法：YES")):
                check_one(x[method]["code"], expected, x["id"] + "." + method + ".empty", empty)
                count += 1
                check_one(x[method]["code"], expected, x["id"] + "." + method + ".single", single)
                count += 1
                check_one(x[method]["code"], expected.replace("YES", "NO"),
                          x["id"] + "." + method + ".gap_then_child", incomplete)
                count += 1
            check_one(x["variation"]["code"], "YES", x["id"] + ".variation.empty", empty)
            count += 1
            check_one(x["variation"]["code"], "YES", x["id"] + ".variation.single", single)
            count += 1
            check_one(x["variation"]["code"], "NO", x["id"] + ".variation.one_child", incomplete)
            count += 1

        if x["id"] == "selection-sort-20261129":
            # 检查单元素、重复值、负数，以及稳定版对相同关键字的原始次序。
            extra = [
                ("single", "1\n7\n", "7"),
                ("all_equal", "4\n5 5 5 5\n", "5 5 5 5"),
                ("negative_duplicates", "6\n-3 0 -3 2 0 -1\n", "-3 -3 -1 0 0 2"),
                ("already_sorted", "5\n1 2 3 4 5\n", "1 2 3 4 5"),
            ]
            for method in ("brute", "optimal"):
                for label, data, expected in extra:
                    check_one(x[method]["code"], expected, x["id"] + "." + method + "." + label, data)
                    count += 1
            stable_case = "3\n2 1\n2 2\n1 3\n"
            check_one(x["variation"]["code"], "1:3 2:1 2:2",
                      x["id"] + ".variation.equal_keys", stable_case)
            count += 1

        if x["id"] == "threaded-binary-tree-20261201":
            empty = "0 0\n"
            for method in ("brute", "optimal"):
                check_one(x[method]["code"], "", x["id"] + "." + method + ".empty", empty)
                count += 1
            single = "1 1\n5 0 0\n"
            for method in ("brute", "optimal"):
                check_one(x[method]["code"], "5", x["id"] + "." + method + ".single", single)
                count += 1
            check_one(x["variation"]["code"], "-1", x["id"] + ".variation.empty",
                      "0 0 7\n")
            count += 1
            check_one(x["variation"]["code"], "-1", x["id"] + ".variation.single_last",
                      "1 1 5\n5 0 0\n")
            count += 1
            check_one(x["variation"]["code"], "3", x["id"] + ".variation.real_right_child",
                      "7 1 2\n4 2 3\n2 4 5\n6 6 7\n1 0 0\n3 0 0\n5 0 0\n7 0 0\n")
            count += 1

        if x["id"] == "lc94-inorder-iterative-20261123":
            for method in ("brute", "optimal"):
                check_one(x[method]["code"], "", x["id"] + "." + method + ".empty_tree", "0 0\n")
                count += 1
            check_one(x["variation"]["code"], "-1", x["id"] + ".variation.empty_tree", "0 0 1\n")
            count += 1

            single = "1 1\n-1 0 0\n"
            for method in ("brute", "optimal"):
                check_one(x[method]["code"], "-1", x["id"] + "." + method + ".single_minus_one", single)
                count += 1
            check_one(x["variation"]["code"], "FOUND -1",
                      x["id"] + ".variation.found_negative_one", "1 1 1\n-1 0 0\n")
            count += 1
            check_one(x["variation"]["code"], "-1", x["id"] + ".variation.k_zero",
                      "1 1 0\n-1 0 0\n")
            count += 1
            check_one(x["variation"]["code"], "-1", x["id"] + ".variation.k_too_large",
                      "1 1 2\n-1 0 0\n")
            count += 1

            chain_rows = "\n".join(
                f"{i} 0 {i + 1 if i < 100 else 0}" for i in range(1, 101)
            )
            chain_input = "100 1\n" + chain_rows + "\n"
            chain_output = " ".join(str(i) for i in range(1, 101))
            for method in ("brute", "optimal"):
                check_one(x[method]["code"], chain_output,
                          x["id"] + "." + method + ".right_skew_100", chain_input)
                count += 1
            check_one(x["variation"]["code"], "FOUND 100",
                      x["id"] + ".variation.k_equals_n",
                      "100 1 100\n" + chain_rows + "\n")
            count += 1
            check_one(x["variation"]["code"], "-1",
                      x["id"] + ".variation.k_greater_than_n",
                      "100 1 101\n" + chain_rows + "\n")
            count += 1
        if x["id"] == "tree-reconstruct-pre-in-20261126":
            # 三份静态演示程序都必须通过样例、单结点及26个唯一大写字母的退化树测试。
            replacements = {
                "brute": [
                    ('const char pre[] = "ABDECF";', 'const char pre[] = "A";'),
                    ('const char in[] = "DBEACF";', 'const char in[] = "A";'),
                ],
                "optimal": [
                    ('const char pre[] = "ABDECF";', 'const char pre[] = "A";'),
                    ('const char in[] = "DBEACF";', 'const char in[] = "A";'),
                ],
                "variation": [
                    ('const char in[] = "DBEACF";', 'const char in[] = "A";'),
                    ('const char post[] = "DEBFCA";', 'const char post[] = "A";'),
                ],
            }
            single_expected = {
                "brute": "后序遍历：A",
                "optimal": "后序遍历：A",
                "variation": "先序遍历：A",
            }
            for method, pairs in replacements.items():
                code = x[method]["code"].replace("int n = 6;", "int n = 1;", 1)
                for old, new in pairs:
                    if old not in code:
                        raise ValueError(f"{x['id']}.{method}: 单结点测试替换锚点缺失")
                    code = code.replace(old, new, 1)
                check_one(code, single_expected[method], x["id"] + "." + method + ".single_node")
                count += 1

            alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            reverse_alphabet = alphabet[::-1]
            skew_cases = {
                "left_skew": (alphabet, reverse_alphabet, reverse_alphabet),
                "right_skew": (alphabet, alphabet, reverse_alphabet),
            }
            for case_name, (preorder, inorder, postorder) in skew_cases.items():
                for method in ("brute", "optimal"):
                    code = x[method]["code"].replace('const char pre[] = "ABDECF";',
                                                     f'const char pre[] = "{preorder}";', 1)
                    code = code.replace('const char in[] = "DBEACF";',
                                        f'const char in[] = "{inorder}";', 1)
                    code = code.replace("int n = 6;", "int n = 26;", 1)
                    check_one(code, "后序遍历：" + " ".join(postorder),
                              x["id"] + "." + method + "." + case_name + "_26")
                    count += 1
                code = x["variation"]["code"].replace('const char in[] = "DBEACF";',
                                                      f'const char in[] = "{inorder}";', 1)
                code = code.replace('const char post[] = "DEBFCA";',
                                    f'const char post[] = "{postorder}";', 1)
                code = code.replace("int n = 6;", "int n = 26;", 1)
                check_one(code, "先序遍历：" + " ".join(alphabet),
                          x["id"] + ".variation." + case_name + "_26")
                count += 1
        if x["id"] == "tree-level-order-20261119":
            sample_tree = """Node tree[] = {
        {'A', 1, 2},
        {'B', 3, 4},
        {'C', -1, 5},
        {'D', -1, -1},
        {'E', -1, -1},
        {'F', -1, -1}
    };"""
            single_tree = "Node tree[] = {{'A', -1, -1}};"
            for method in ("brute", "optimal", "variation"):
                code = x[method]["code"]
                if sample_tree not in code:
                    raise ValueError(f"{x['id']}.{method}: 示例树代码与验证模板不一致")
                single_code = code.replace(sample_tree, single_tree, 1)
                single_expected = "1" if method == "variation" else "A"
                check_one(single_code, single_expected, x["id"] + "." + method + ".single_node")
                count += 1
                if "int root = 0;" not in code:
                    raise ValueError(f"{x['id']}.{method}: 找不到root初始化，无法测试空树")
                empty_code = code.replace("int root = 0;", "int root = -1;", 1)
                empty_expected = "0" if method == "variation" else ""
                check_one(empty_code, empty_expected, x["id"] + "." + method + ".empty_tree")
                count += 1
        if x["id"] == "huffman-20261113":
            brute_code = x["brute"]["code"].replace("int n = 6;", "int n = 2;")
            brute_code = brute_code.replace(
                "int input[6] = {5, 9, 12, 13, 16, 45};",
                "int input[6] = {4, 7};"
            )
            optimal_code = x["optimal"]["code"].replace(
                "int input[6] = {5, 9, 12, 13, 16, 45};",
                "int input[6] = {4, 7};"
            ).replace("int n = 6;", "int n = 2;")
            variation_code = x["variation"]["code"].replace(
                "int weight[4] = {2, 3, 7, 9};",
                "int weight[4] = {4, 7};"
            ).replace("i < 4", "i < 2")
            for method, code in (("brute", brute_code), ("optimal", optimal_code),
                                 ("variation", variation_code)):
                check_one(code, "11", x["id"] + "." + method + ".two_leaves")
                count += 1
        if x["id"] == "two-stacks-one-array-20261120":
            harnesses = {
                "brute": """int main(void) {
    FixedStacks s; int x = -1;
    initFixed(&s, 2);
    if (!push1(&s, 1)) return 1;
    if (push1(&s, 2)) return 2;
    if (!push2(&s, 9)) return 3;
    if (!pop1(&s, &x) || x != 1) return 4;
    if (!pop2(&s, &x) || x != 9) return 5;
    if (pop1(&s, &x) || pop2(&s, &x)) return 6;
    puts("PASS"); return 0;
}""",
                "optimal": """int main(void) {
    SharedStacks s; int x = -1;
    initShared(&s, 2);
    if (!push1(&s, 1) || !push2(&s, 9)) return 1;
    if (push1(&s, 2)) return 2;
    if (!pop1(&s, &x) || x != 1) return 3;
    if (!pop2(&s, &x) || x != 9) return 4;
    if (pop1(&s, &x) || pop2(&s, &x)) return 5;
    puts("PASS"); return 0;
}""",
                "variation": """int main(void) {
    SharedStacks s; int x = -1;
    init(&s, 2);
    if (!push1(&s, 1) || !push2(&s, 9)) return 1;
    if (push2(&s, 2)) return 2;
    if (!pop2(&s, &x) || x != 9) return 3;
    if (!pop1(&s, &x) || x != 1) return 4;
    if (pop1(&s, &x) || pop2(&s, &x)) return 5;
    puts("PASS"); return 0;
}"""
            }
            for method, harness in harnesses.items():
                code = x[method]["code"].rsplit("int main(void) {", 1)[0] + harness
                check_one(code, "PASS", x["id"] + "." + method + ".capacity_two")
                count += 1
        if x["id"] == "sliding-window-max-20261121":
            extra = [
                ("k_one", "4 1\n2 -1 2 3\n", "2 -1 2 3"),
                ("k_equals_n", "4 4\n-5 -2 -9 -3\n", "-2"),
                ("all_negative", "5 2\n-5 -2 -7 -1 -3\n", "-2 -2 -1 -1"),
                ("all_equal", "4 3\n5 5 5 5\n", "5 5"),
            ]
            for method in ("brute", "optimal", "variation"):
                for label, data, expected in extra:
                    check_one(x[method]["code"], expected, x["id"] + "." + method + "." + label, data)
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
        if x["id"] == "kmp-20261111":
            extra = [
                ("single", "a\na\n", "0"),
                ("pattern_longer", "a\naa\n", "-1"),
                ("not_found", "abcdef\ngh\n", "-1"),
                ("overlap", "abababa\nababa\n", "0"),
                ("repeated_prefix", "aaaaab\naaab\n", "2"),
            ]
            for variant in ("brute", "optimal", "variation"):
                for label, data, expected in extra:
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1
        if x["id"] == "lc-hash-linear-20261116":
            extra = [
                ("single_zero", "1 2\n0\n0\n1\n", "1\n-1", "1\n1"),
                ("negative_collision", "3 2\n-3 20008 40019\n-3\n40019\n",
                 "1\n3", "1\n3"),
            ]
            for variant in ("brute", "optimal", "variation"):
                for label, data, standard, probe_count in extra:
                    expected = probe_count if variant == "variation" else standard
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1
        if x["id"] == "lc503-20261106":
            extra = [
                ("single", "1\n5\n", "-1"),
                ("equal", "3\n2 2 2\n", "-1 -1 -1"),
                ("increasing", "3\n1 2 3\n", "2 3 -1"),
                ("wrap", "3\n3 1 2\n", "-1 2 3"),
                ("negative", "3\n-1 -2 -3\n", "-1 -1 -1"),
                ("extreme", "3\n1000000000 -1000000000 999999999\n",
                 "-1 999999999 1000000000"),
                ("descending", "5\n5 4 3 2 1\n", "-1 5 5 5 5"),
                ("max_n", "10000\n" + " ".join(map(str, range(1, 10001))) + "\n",
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
        if x["id"] == "quick-sort-20261117":
            extra = [
                ("single", "1\n7\n", "7"),
                ("already_sorted", "5\n1 2 3 4 5\n", "1 2 3 4 5"),
                ("reverse", "5\n5 4 3 2 1\n", "1 2 3 4 5"),
                ("all_equal", "5\n2 2 2 2 2\n", "2 2 2 2 2"),
                ("extreme", "4\n1000000000 -1000000000 0 -1000000000\n",
                 "-1000000000 -1000000000 0 1000000000"),
                ("max_n", "100\n" + " ".join(map(str, range(100, 0, -1))) + "\n",
                 " ".join(map(str, range(1, 101)))),
            ]
            for variant in ("brute", "optimal", "variation"):
                for label, data, expected in extra:
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1


        if x["id"] == "radix-sort-20261124":
            extra = [
                ("single_zero", "1\n0\n", "0"),
                ("all_zero", "4\n0 0 0 0\n", "0 0 0 0"),
                ("repeated_and_zero", "6\n5 50 5 500 0 50\n", "0 5 5 50 50 500"),
                ("six_digit_boundaries", "5\n999999 0 100000 10 1\n", "0 1 10 100000 999999"),
            ]
            for variant in ("brute", "optimal"):
                for label, data, expected in extra:
                    check_one(x[variant]["code"], expected,
                              x["id"] + "." + variant + "." + label, data)
                    count += 1
                check_rejected(x[variant]["code"], x["id"] + "." + variant + ".negative_input",
                               "2\n-1 0\n")
                count += 1


        if x["id"] == "shell-sort-20261125":
            extra_cases = [
                ("single", "1\n7\n", "7", "7"),
                ("negative_duplicates", "6\n-3 0 -3 2 0 -1\n",
                 "-3 -3 -1 0 0 2", "-3 0 -3 2 0 -1\n-3 -3 -1 0 0 2"),
                ("already_sorted", "5\n1 2 3 4 5\n",
                 "1 2 3 4 5", "1 2 3 4 5\n1 2 3 4 5"),
                ("reverse", "5\n5 4 3 2 1\n",
                 "1 2 3 4 5", "1 2 3 4 5\n1 2 3 4 5"),
                ("int_extremes", "5\n2147483647 -2147483648 0 -1 2147483647\n",
                 "-2147483648 -1 0 2147483647 2147483647",
                 "0 -2147483648 2147483647 -1 2147483647\n-2147483648 -1 0 2147483647 2147483647"),
            ]
            for label, data, brute_expected, shell_expected in extra_cases:
                check_one(x["brute"]["code"], brute_expected,
                          x["id"] + ".brute." + label, data)
                count += 1
                check_one(x["optimal"]["code"], shell_expected,
                          x["id"] + ".optimal." + label, data)
                count += 1
            for method in ("brute", "optimal"):
                check_rejected(x[method]["code"], x["id"] + "." + method + ".n_zero", "0\n")
                count += 1
                check_rejected(x[method]["code"], x["id"] + "." + method + ".n_over_limit",
                               "1001\n")
                count += 1
            max_values = list(range(1000))
            max_data = "1000\n" + " ".join(map(str, max_values)) + "\n"
            max_sorted = " ".join(map(str, max_values))
            check_one(x["brute"]["code"], max_sorted, x["id"] + ".brute.max_n", max_data)
            count += 1
            max_shell_expected = "\n".join([max_sorted] * 9)
            check_one(x["optimal"]["code"], max_shell_expected,
                      x["id"] + ".optimal.max_n", max_data)
            count += 1

        if x["id"] == "sparse-fast-transpose-20261122":
            extra_cases = [
                ("empty_nnz", "3 4 0\n", "0 0 0 0\n4 3 0"),
                ("zero_cols", "3 0 0\n", "\n0 3 0"),
                ("one_col", "4 1 3\n0 0 7\n2 0 -5\n3 0 9\n",
                 "0\n1 4 3\n0 0 7\n0 2 -5\n0 3 9"),
                ("last_col", "3 4 3\n0 3 5\n1 3 -2\n2 3 8\n",
                 "0 0 0 0\n4 3 3\n3 0 5\n3 1 -2\n3 2 8"),
                ("single_cell", "1 1 1\n0 0 -1000000000\n",
                 "0\n1 1 1\n0 0 -1000000000"),
                ("full_matrix", "2 2 4\n0 0 1\n0 1 2\n1 0 3\n1 1 4\n",
                 "0 2\n2 2 4\n0 0 1\n0 1 3\n1 0 2\n1 1 4"),
            ]
            for method in ("brute", "optimal", "variation"):
                for label, data, expected in extra_cases:
                    check_one(x[method]["code"], expected, x["id"] + "." + method + "." + label, data)
                    count += 1
            invalid_cases = [
                ("unsorted", "2 2 2\n1 0 3\n0 1 4\n"),
                ("duplicate", "2 2 2\n0 1 3\n0 1 4\n"),
                ("zero_value", "1 1 1\n0 0 0\n"),
                ("out_of_range", "2 2 1\n2 0 5\n"),
            ]
            for method in ("brute", "optimal", "variation"):
                for label, data in invalid_cases:
                    check_rejected(x[method]["code"], x["id"] + "." + method + "." + label, data)
                    count += 1
    # 历史正式题库中不在pending队列的题也要做回归，避免错误变式漏检。
    published = json.loads((ROOT / "lessons.json").read_text(encoding="utf-8"))
    for lesson in published:
        source = lesson.get("source")
        if not isinstance(source, str) or not source.startswith(("http://", "https://")):
            raise ValueError("{}: 已发布课程缺少真实HTTP来源链接".format(lesson.get("id")))
        expected_source = expected_sources.get(lesson["id"])
        if expected_source and source != expected_source:
            raise ValueError("{}: 已发布课程来源链接与已核验资料不一致".format(lesson.get("id")))
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
