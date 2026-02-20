import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen

from .templates import get_templates


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True)


def cmd_doctor() -> int:
    tools = ["python3", "mcporter"]
    uv_path = shutil.which("uv") or shutil.which("uvx")

    print("[doctor] checking tools...")
    ok = True
    for t in tools:
        p = shutil.which(t)
        print(f"- {t}: {'OK (' + p + ')' if p else 'MISSING'}")
        ok = ok and bool(p)

    print(f"- uv/uvx: {'OK (' + uv_path + ')' if uv_path else 'MISSING'}")
    ok = ok and bool(uv_path)

    return 0 if ok else 1


def cmd_templates(project_dir: str) -> int:
    tpls = get_templates(project_dir)
    print("Available templates:")
    for k in tpls:
        print(f"- {k}")
    return 0


def cmd_env_template(template: str, project_dir: str, output: str) -> int:
    tpls = get_templates(project_dir)
    if template not in tpls:
        print(f"Unknown template: {template}")
        return 1

    out = Path(output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tpls[template].env_template)
    print(f"Written: {out}")
    return 0


def _expand_env(value: str) -> str:
    out = value
    for k, v in os.environ.items():
        out = out.replace(f"${{{k}}}", v)
    return out


def cmd_add(template: str, project_dir: str, name: str, scope: str = "project") -> int:
    tpls = get_templates(project_dir)
    if template not in tpls:
        print(f"Unknown template: {template}")
        return 1

    tpl = tpls[template]
    cmd = ["mcporter", "config", "add", name, "--command", _expand_env(tpl.command)]
    for a in tpl.args:
        cmd += ["--arg", _expand_env(a)]
    cmd += ["--scope", scope, "--output", "json"]

    p = run(cmd)
    if p.returncode != 0:
        print(p.stderr.strip() or p.stdout.strip())
        return p.returncode

    print(p.stdout.strip())
    return 0


def cmd_verify(name: str) -> int:
    p = run(["mcporter", "list", name, "--schema", "--output", "json"])
    if p.returncode != 0:
        print(p.stderr.strip() or p.stdout.strip())
        return p.returncode

    try:
        j = json.loads(p.stdout)
        print(f"OK: tools={len(j.get('tools', []))}")
    except Exception:
        print("OK")
    return 0


def cmd_nocodb_link(url: str, workspace_id: str, project_id: str) -> int:
    print(f"{url.rstrip('/')}/#/{workspace_id}/{project_id}")
    return 0


def cmd_nocodb_create_token(url: str, project_id: str, xc_token: str, name: str) -> int:
    endpoint = f"{url.rstrip('/')}/api/v1/db/meta/projects/{project_id}/api-tokens"
    payload = json.dumps({"description": name}).encode("utf-8")
    req = Request(endpoint, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("xc-token", xc_token)
    try:
        with urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8")
            print(body)
            return 0
    except Exception as e:
        print(f"Token creation failed: {e}")
        print("Tip: ensure xc-token has meta/project admin rights.")
        return 1


def main() -> None:
    parser = argparse.ArgumentParser(prog="mcp-onboarder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("doctor")

    p_tpl = sub.add_parser("templates")
    p_tpl.add_argument("--project-dir", default=".")

    p_env = sub.add_parser("env-template")
    p_env.add_argument("template")
    p_env.add_argument("--project-dir", default=".")
    p_env.add_argument("--output", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("template")
    p_add.add_argument("--project-dir", required=True)
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--scope", default="project", choices=["project", "user"])

    p_ver = sub.add_parser("verify")
    p_ver.add_argument("name")

    p_link = sub.add_parser("nocodb-link")
    p_link.add_argument("--url", required=True)
    p_link.add_argument("--workspace-id", required=True)
    p_link.add_argument("--project-id", required=True)

    p_tok = sub.add_parser("nocodb-create-token")
    p_tok.add_argument("--url", required=True)
    p_tok.add_argument("--project-id", required=True)
    p_tok.add_argument("--xc-token", required=True)
    p_tok.add_argument("--name", default="mcp-onboarder")

    args = parser.parse_args()

    if args.cmd == "doctor":
        raise SystemExit(cmd_doctor())
    if args.cmd == "templates":
        raise SystemExit(cmd_templates(args.project_dir))
    if args.cmd == "env-template":
        raise SystemExit(cmd_env_template(args.template, args.project_dir, args.output))
    if args.cmd == "add":
        raise SystemExit(cmd_add(args.template, args.project_dir, args.name, args.scope))
    if args.cmd == "verify":
        raise SystemExit(cmd_verify(args.name))
    if args.cmd == "nocodb-link":
        raise SystemExit(cmd_nocodb_link(args.url, args.workspace_id, args.project_id))
    if args.cmd == "nocodb-create-token":
        raise SystemExit(cmd_nocodb_create_token(args.url, args.project_id, args.xc_token, args.name))


if __name__ == "__main__":
    main()
