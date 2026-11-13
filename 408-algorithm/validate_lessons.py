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
        "dijkstra-20261114": {"brute": 5, "optimal": 6},
        "aoe-critical-20261115": {"brute": 5, "optimal": 9},
        "quick-sort-20261117": {"brute": 6, "optimal": 10},
        "two-stacks-one-array-20261120": {"brute": 4, "optimal": 5, "variation": 9},
        "sliding-window-max-20261121": {"brute": 18, "optimal": 8, "variation": 8},
    }
    diagram_minimum = {
        "lc997-20261109": {"brute": 6, "optimal": 6},
        "lc-hash-linear-20261116": {"brute": 10, "optimal": 10, "variation": 5},
        "prim-20261112": {"brute": 4, "optimal": 5},
        "huffman-20261113": {"brute": 5, "optimal": 5},
        "dijkstra-20261114": {"brute": 5, "optimal": 6},
        "aoe-critical-20261115": {"brute": 5, "optimal": 9},
        "two-stacks-one-array-20261120": {"brute": 4, "optimal": 5},
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
        "aoe-critical-20261115": ("brute", "optimal"),
        "quick-sort-20261117": ("brute", "optimal"),
        "tree-level-order-20261119": ("brute", "optimal", "variation"),
        "lc-hash-linear-20261116": ("brute", "optimal", "variation"),
        "two-stacks-one-array-20261120": ("brute", "optimal", "variation"),
        "sliding-window-max-20261121": ("brute", "optimal", "variation"),
    }
    reviewed_variations = {
        "lc997-20261109", "lc994-20261110", "kmp-20261111",
        "prim-20261112", "huffman-20261113", "dijkstra-20261114",
        "tree-level-order-20261119",
        "aoe-critical-20261115", "lc-hash-linear-20261116",
        "two-stacks-one-array-20261120", "sliding-window-max-20261121",
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
    for method, expected in (("brute", expected_quick_brute), ("optimal", expected_quick_optimal)):
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
    }
    variant_inputs = { "kmp-20261111": "aaaaab\naaab\n","lc-hash-linear-20261116": "7 5\n5 20016 40027 17 20028 -3 8\n40027 5 99 -3 20028\n",
                      "lc997-20261109": "3 3\n1 3\n2 3\n3 1\n",
                      "lc994-20261110": "2 2\n2 0\n0 1\n",
                      "lc503-20261106": "5\n3 8 4 1 2\n", "quick-sort-20261117": "6\n3 -1 3 0 -1 2\n", "floyd-20261118": "3 3\n1 2 4\n2 3 -2\n1 3 5\n", "sliding-window-max-20261121": "8 3\n1 3 -1 -3 5 3 6 7\n"}
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
                ("k_one", "4 1\\n2 -1 2 3\\n", "2 -1 2 3"),
                ("k_equals_n", "4 4\\n-5 -2 -9 -3\\n", "-2"),
                ("all_negative", "5 2\\n-5 -2 -7 -1 -3\\n", "-2 -2 -1 -1"),
                ("all_equal", "4 3\\n5 5 5 5\\n", "5 5"),
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
