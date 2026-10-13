#!/usr/bin/env python3
"""北京时间06:00检查今日已发布课程并通过SMTP发出简短提醒。"""
import json
import os
import smtplib
import ssl
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: send_daily_email.py lessons.json")
    today = datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat()
    lessons = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    matched = [x for x in lessons if x.get("date") == today]
    if len(matched) != 1:
        raise SystemExit(f"今日 {today} 已发布课程数量为 {len(matched)}，不发送邮件")
    lesson_id = matched[0]["id"]
    if not isinstance(lesson_id, str) or not lesson_id or any(c in lesson_id for c in "\r\n# "):
        raise SystemExit("非法课程ID")
    required = ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_TO")
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise SystemExit("未配置 GitHub Actions Secrets: " + ", ".join(missing))
    sender = os.environ["SMTP_USER"]
    receiver = os.environ["MAIL_TO"]
    host = os.environ["SMTP_HOST"]
    port = int(os.environ.get("SMTP_PORT") or "465")
    msg = EmailMessage()
    msg["Subject"] = "今日408算法题"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("今日408算法题：https://ustarrise.github.io/408-algorithm/#" + lesson_id + "\n")
    if port == 465:
        with smtplib.SMTP_SSL(host, port, timeout=30, context=ssl.create_default_context()) as smtp:
            smtp.login(sender, os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.starttls(context=ssl.create_default_context())
            smtp.login(sender, os.environ["SMTP_PASSWORD"])
            smtp.send_message(msg)
    print("今日邮件已通过 SMTP 提交，课程ID:", lesson_id)

if __name__ == "__main__":
    main()
