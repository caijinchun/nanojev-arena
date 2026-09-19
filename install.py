# -*- coding: utf-8 -*-
"""NanoJev Arena 一键安装:上游仓库 + 依赖 + checkpoint + 游戏页面。"""
import os, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(__file__).parent
UP = ROOT / "NanoJev"
MIRROR = os.environ.get("HF_ENDPOINT", "https://hf-mirror.com")
CHECKPOINTS = {
    "games_gold_seed17": "贪吃蛇大乱斗",
}

def run(cmd, cwd=None, env=None):
    print(">", " ".join(str(c) for c in cmd))
    subprocess.run([str(c) for c in cmd], check=True, cwd=cwd, env=env)

def main():
    if not UP.exists():
        run(["git", "clone", "--depth", "1",
             "https://github.com/TianyuCodings/NanoJev.git", UP])
    else:
        print("[skip] NanoJev/ 已存在")

    venv = UP / ".venv"
    if not venv.exists():
        run([sys.executable, "-m", "venv", venv])
    py = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    run([py, "-m", "pip", "install", "-q", "--upgrade", "pip"])
    # requirements-toy 默认装 CPU 版 torch;CUDA 版见 README 说明
    run([py, "-m", "pip", "install", "-q", "-r", UP / "requirements-toy.txt"])

    env = dict(os.environ, HF_ENDPOINT=MIRROR, HF_HUB_DISABLE_XET="1")
    run([py, "-c",
         "from huggingface_hub import snapshot_download\n"
         "snapshot_download(repo_id='C-Tianyu/NanoJev', local_dir='checkpoints/games',\n"
         "                  allow_patterns=['variants/games_gold_seed17/*'])\n"
         "print('checkpoint ok')"],
        cwd=UP, env=env)

    for page in ("snake.html",):
        shutil.copy(ROOT / "web" / page, UP / "web" / page)
        print("[copy] web/" + page)

    print("\n完成!启动贪吃蛇大乱斗:")
    if os.name == "nt":
        print(f"  cd {UP}")
        print("  .venv\\Scripts\\python scripts/serve_decisions.py "
              "--checkpoint-dir checkpoints/games/variants/games_gold_seed17 "
              "--web-root web --port 8766 --precision fp32")
    else:
        print(f"  cd {UP} && .venv/bin/python scripts/serve_decisions.py "
              "--checkpoint-dir checkpoints/games/variants/games_gold_seed17 "
              "--web-root web --port 8766 --precision fp32")
    print("  打开 http://127.0.0.1:8766/snake.html")

if __name__ == "__main__":
    main()
