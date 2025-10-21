# TDS Project 1 - Final Working Version
# Author: madhavraman07

# Setup and library imports
# !pip install fastapi uvicorn pyngrok gitpython nest_asyncio requests > /dev/null

import os
import nest_asyncio
import uvicorn
from fastapi import FastAPI, Request
from pyngrok import ngrok, conf
from git import Repo
from threading import Thread
import requests

# Configuration parameters
GITHUB_USERNAME = "madhavraman07"
GITHUB_TOKEN = "<YOUR_GITHUB_TOKEN>"        # REDACT BEFORE PUBLIC SHARE
NGROK_AUTH = "<YOUR_NGROK_AUTH_TOKEN>"      # REDACT BEFORE PUBLIC SHARE
SECRET = "mysecret123"
REPO_NAME = "TDSFINALPROJECT"

nest_asyncio.apply()

# Kill existing ngrok processes and disconnect tunnels
os.system("pkill ngrok > /dev/null 2>&1")
try:
    tunnels = requests.get("http://localhost:4040/api/tunnels").json()["tunnels"]
    for tunnel in tunnels:
        requests.delete(tunnel["uri"])
except requests.exceptions.ConnectionError:
    pass

# Create or update GitHub repo
os.system(f'curl -u {GITHUB_USERNAME}:{GITHUB_TOKEN} https://api.github.com/user/repos '
          f'-d "{{\\"name\\":\\"{REPO_NAME}\\",\\"private\\":false}}" > /dev/null 2>&1')

os.makedirs(REPO_NAME, exist_ok=True)
with open(f"{REPO_NAME}/README.md", "w") as f:
    f.write(f"# {REPO_NAME}\nAuto-generated for IITM TDS Project submission.\n")

repo = Repo.init(REPO_NAME)
repo.git.add(A=True)
repo.index.commit("Initial commit")
if "origin" not in [r.name for r in repo.remotes]:
    repo.create_remote('origin', f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
origin = repo.remote("origin")
origin.push(refspec="HEAD:main", force=True)

repo_url = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}"

# Define FastAPI app
app = FastAPI()
