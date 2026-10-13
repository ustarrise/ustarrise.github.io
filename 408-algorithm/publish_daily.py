#!/usr/bin/env python3
"""从审核后的备用题库发布一题到 GitHub Pages；不调用任何收费 API。"""
import argparse
import copy
import json
import os
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent
PUBLISHED = BASE / "lessons.json"
QUEUE = BASE / "pending-lessons.json"

FIELDS = ("id", "date", "year", "number", "category", "title",
          "difficulty", "time", "source", "question", "constraint",
          "sample", "brute", "optimal", "tips", "variation", "animation")


def read_json(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"{path.name} must be a JSON list")
    return data


def validate(lesson):
    missing = [k for k in FIELDS if k not in lesson]
    if missing:
        raise ValueError(f"{lesson.get('id', '?')} missing: {missing}")
    for approach in ("brute", "optimal"):
        val = lesson[approach]
        for k in ("title", "tag", "idea", "complexity", "risk", "code", "explain"):
            if k not in val:
                raise ValueError(f"{lesson['id']}.{approach}.{k} missing")
        if "int main(" not in val["code"] and "int main(void)" not in val["code"]:
            raise ValueError(f"{lesson['id']}.{approach} lacks main()")
    if not lesson["animation"].get("brute") or not lesson["animation"].get("optimal"):
        raise ValueError(f"{lesson['id']} lacks animation")
    if not lesson["variation"].get("code"):
        raise ValueError(f"{lesson['id']} lacks variation solution code")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="只检查备用题库，不写文件")
    args = parser.parse_args()

    published = read_json(PUBLISHED)
    queue = read_json(QUEUE)
    for obj in queue:
        validate(obj)

    # 预测训练：仅发布人工审核、已编译测试的备用题，不生成未审查的新代码。
    # 45/35/20 是长期选题目标，不改变已有课程的预定日期。
    from collections import Counter
    def topic_group(obj):
        label = str(obj.get("category", "")) + " " + str(obj.get("title", ""))
        if any(k in label for k in ("图", "二叉树", "树", "DFS", "BFS")):
            return "综合变式"
        if any(k in label for k in ("矩阵", "稀疏", "栈", "队列")):
            return "预测补盲"
        return "经典方法"

    ids = [x["id"] for x in queue]
    dates = [x["date"] for x in queue]
    if len(ids) != len(set(ids)) or len(dates) != len(set(dates)):
        raise ValueError("备用题存在重复ID或发布日期")
    print("备用题覆盖（目标45%经典/35%综合/20%补盲）：",
          dict(Counter(topic_group(x) for x in queue)))
    for obj in queue:
        if "预测" in str(obj.get("year", "")) and "真题" in str(obj.get("source", "")):
            raise ValueError("预测练习不能冒充真题: " + obj["id"])

    existing_ids = {x["id"] for x in published}
    existing_dates = {x["date"] for x in published}
    if len(existing_ids) != len(published):
        raise ValueError("Published lessons contain duplicate IDs")

    today = datetime.now(ZoneInfo("Asia/Shanghai")).date()
    choices = sorted(
        (x for x in queue
         if x["id"] not in existing_ids and date.fromisoformat(x["date"]) <= today),
        key=lambda x: (x["date"], x["id"])
    )
    future = [x for x in queue if x["id"] not in existing_ids
              and date.fromisoformat(x["date"]) > today]
    print(f"北京时间今天：{today} | 已发布：{len(published)} | 待发布：{len(choices)} | 后备：{len(future)}")
    if args.dry_run:
        print("备用题目校验通过。")
        return

    if today.isoformat() in existing_dates:
        print("今天已经有题目，无需重复发布。")
        return
    if not choices:
        raise RuntimeError("备用题库已耗尽或尚未到发布日期。请补充 pending-lessons.json。")

    picked = copy.deepcopy(choices[0])
    picked["date"] = today.isoformat()  # 任务延迟时，日期以真实发布时间为准
    validate(picked)
    published.append(picked)
    # 与既有网站兼容；保留历史所有题目
    PUBLISHED.write_text(
        json.dumps(published, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    print(f"今日已更新题库：{picked['id']} · {picked['title']}")


if __name__ == "__main__":
    main()
