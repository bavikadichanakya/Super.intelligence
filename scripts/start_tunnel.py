import subprocess
import re
import sys
import os

cloudflared_path = os.path.abspath("bin/cloudflared.exe")
if not os.path.exists(cloudflared_path):
    print("cloudflared.exe not found!")
    sys.exit(1)

cmd = [cloudflared_path, "tunnel", "--url", "http://localhost:5000"]
print(f"Starting tunnel: {' '.join(cmd)}")

proc = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    encoding="utf-8",
    errors="replace"
)

tunnel_url = None
url_regex = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

for line in iter(proc.stdout.readline, ""):
    sys.stdout.write(line)
    sys.stdout.flush()
    match = url_regex.search(line)
    if match and not tunnel_url:
        tunnel_url = match.group(0)
        print(f"\n=======================================================")
        print(f"DISCOVERED PUBLIC HTTPS TUNNEL URL: {tunnel_url}")
        print(f"=======================================================\n")
        
        # Save to file
        os.makedirs("data", exist_ok=True)
        with open("data/tunnel_url.txt", "w") as f:
            f.write(tunnel_url.strip())
            
        # Update .env
        redirect_uri = f"{tunnel_url}/oauth/instagram/callback"
        env_lines = open(".env", "r", encoding="utf-8").readlines()
        new_env = []
        found = False
        for eline in env_lines:
            if eline.startswith("INSTAGRAM_REDIRECT_URI="):
                new_env.append(f"INSTAGRAM_REDIRECT_URI={redirect_uri}\n")
                found = True
            elif eline.startswith("INSTAGRAM_PUBLIC_TUNNEL_URL="):
                new_env.append(f"INSTAGRAM_PUBLIC_TUNNEL_URL={tunnel_url}\n")
            else:
                new_env.append(eline)
        if not found:
            new_env.append(f"INSTAGRAM_REDIRECT_URI={redirect_uri}\n")
        with open(".env", "w", encoding="utf-8") as f:
            f.writelines(new_env)
        print(f"Updated .env with INSTAGRAM_REDIRECT_URI={redirect_uri}")

proc.wait()
