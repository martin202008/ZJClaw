"""
ZJClaw WebUI - Standalone web interface for commercial management AI assistant
"""

import os
import json
import asyncio
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "zjclaw-webui-secret-key-change-in-production")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = Path(__file__).parent / "flask_session"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

Session(app)

CONFIG_FILE = Path(__file__).parent / "config.json"
HISTORY_FILE = Path(__file__).parent / "chat_history.json"

current_provider = None
current_model = None
agent_instance = None

def load_chat_history():
    """Load chat history from file"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chat_history(history):
    """Save chat history to file"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving chat history: {e}")

chat_history = load_chat_history()

def init_agent():
    """Initialize agent from config - called once on startup"""
    global agent_instance, current_provider, current_model
    
    config = load_webui_config()
    
    if not config.get("apiKey"):
        print("[ZJClaw] No API key configured, waiting for user configuration")
        return None
    
    try:
        from zjclaw.agent.loop import AgentLoop
        from zjclaw.bus.queue import MessageBus
        from zjclaw.session.manager import SessionManager
        from zjclaw.cron.service import CronService
        from pathlib import Path
        import shutil
        
        bus = MessageBus()
        workspace = get_workspace_from_config()
        workspace.mkdir(parents=True, exist_ok=True)
        
        sandbox_enabled = bool(config.get("workspace"))
        
        # Copy skills to workspace
        pkg_skills = Path(__file__).parent.parent / "zjclaw" / "skills"
        workspace_skills = workspace / "skills"
        
        project_skills_dir = Path(__file__).parent.parent / "skills"
        system_skills_dir = project_skills_dir / "system-skills"
        user_skills_dir = project_skills_dir / "user-skills"
        
        def merge_skills_to_workspace():
            if workspace_skills.exists():
                shutil.rmtree(workspace_skills)
            workspace_skills.mkdir(parents=True, exist_ok=True)
            
            if pkg_skills.exists():
                for skill_dir in pkg_skills.iterdir():
                    if skill_dir.is_dir():
                        dest = workspace_skills / skill_dir.name
                        shutil.copytree(skill_dir, dest)
            
            if system_skills_dir.exists():
                for skill_dir in system_skills_dir.iterdir():
                    if skill_dir.is_dir():
                        dest = workspace_skills / skill_dir.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(skill_dir, dest)
            
            if user_skills_dir.exists():
                for skill_dir in user_skills_dir.iterdir():
                    if skill_dir.is_dir():
                        dest = workspace_skills / skill_dir.name
                        if dest.exists():
                            shutil.rmtree(dest)
                        shutil.copytree(skill_dir, dest)
        
        skills_empty = workspace_skills.exists() and not any(workspace_skills.iterdir())
        if not workspace_skills.exists() or skills_empty:
            merge_skills_to_workspace()
        
        session_manager = SessionManager(workspace)
        cron_store_path = workspace / "cron_jobs.json"
        cron = CronService(cron_store_path)
        
        # Initialize provider
        provider = get_provider_for_model(
            config.get("provider", "minimax"),
            config["apiKey"],
            config.get("apiBase")
        )
        
        if provider:
            current_provider = provider
            current_model = config.get("model", "MiniMax-Text-01")
            
            agent_instance = AgentLoop(
                bus=bus,
                provider=current_provider,
                workspace=workspace,
                model=current_model,
                max_iterations=40,
                context_window_tokens=65536,
                cron_service=cron,
                restrict_to_workspace=sandbox_enabled,
                session_manager=session_manager,
            )
            
            print(f"[ZJClaw] Agent initialized with model: {current_model}")
        
        return agent_instance
        
    except Exception as e:
        print(f"[ZJClaw] Error initializing agent: {e}")
        return None

def load_webui_config():
    """Load WebUI specific configuration"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_workspace_from_config():
    """Get workspace path from config or return default"""
    config = load_webui_config()
    workspace_path = config.get("workspace", "")
    if workspace_path:
        path = Path(workspace_path).expanduser().resolve()
        if path.exists() and path.is_dir():
            return path
    return Path.home() / ".zjclaw" / "workspace"

def save_webui_config(config):
    """Save WebUI configuration"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# Initialize agent on startup - AFTER all functions are defined
# We'll initialize on first request instead to avoid ordering issues
print("[ZJClaw] WebUI ready, agent will be initialized on first request")

def get_provider_for_model(provider_name, api_key, api_base=None):
    """Get the appropriate provider instance for the model"""
    global current_provider, current_model
    
    try:
        from zjclaw.providers.litellm_provider import LiteLLMProvider
        from zjclaw.providers.base import GenerationSettings
        
        model = provider_name
        base_url = api_base
        
        if provider_name == "minimax":
            base_url = base_url or "https://api.minimaxi.com/v1"
            model = "MiniMax-Text-01"
        elif provider_name == "deepseek":
            base_url = base_url or "https://api.deepseek.com/v1"
            model = "deepseek-chat"
        elif provider_name == "zhipu":
            base_url = base_url or "https://open.bigmodel.cn/api/paas/v4"
            model = "glm-4"
        elif provider_name == "dashscope":
            base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            model = "qwen-plus"
        elif provider_name == "openai":
            base_url = base_url or "https://api.openai.com/v1"
            model = "gpt-4o"
        elif provider_name == "anthropic":
            base_url = base_url or "https://api.anthropic.com/v1"
            model = "claude-opus-4-5"
        elif provider_name == "openrouter":
            base_url = base_url or "https://openrouter.ai/api/v1"
            model = "anthropic/claude-opus-4-5"
        elif provider_name == "ollama":
            base_url = base_url or "http://localhost:11434/v1"
            model = "llama3"
        
        provider = LiteLLMProvider(
            api_key=api_key,
            api_base=base_url,
            default_model=model,
            provider_name=provider_name,
        )
        
        provider.generation = GenerationSettings(
            temperature=0.7,
            max_tokens=4096,
        )
        
        current_provider = provider
        current_model = model
        return provider
    except Exception as e:
        raise Exception(f"Failed to create provider: {str(e)}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    global agent_instance, current_provider
    
    data = request.json
    message = data.get("message", "")
    session_id = session.get("session_id", "webui:default")
    
    if not message:
        return jsonify({"error": "消息不能为空"}), 400
    
    config = load_webui_config()
    
    if not config.get("apiKey"):
        return jsonify({
            "error": "请先在设置中配置 API Key"
        }), 400
    
    try:
        # Re-initialize agent if not exists or if config changed
        if not agent_instance:
            init_agent()
        
        if not agent_instance:
            return jsonify({
                "error": "请先在设置中配置 API Key"
            }), 400
        
        async def get_response():
            response = await agent_instance.process_direct(message, session_id)
            await agent_instance.close_mcp()
            return response
        
        response = asyncio.run(get_response())
        
        # Save to chat history
        if session_id not in chat_history:
            chat_history[session_id] = []
        chat_history[session_id].append({"role": "user", "content": message})
        chat_history[session_id].append({"role": "assistant", "content": response})
        
        # Save to file
        save_chat_history(chat_history)
        
        return jsonify({"response": response, "session_id": session_id})
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        if "api_key" in error_msg.lower() or "auth" in error_msg.lower() or "unauthorized" in error_msg.lower():
            error_msg = "API Key 无效或已过期，请检查设置"
        return jsonify({
            "error": f"处理消息时出错: {error_msg}",
            "trace": traceback.format_exc() if app.debug else None
        }), 500

@app.route("/api/config", methods=["GET"])
def get_config():
    """Get current configuration (without exposing API key)"""
    config = load_webui_config()
    default_workspace = str(Path.home() / ".zjclaw" / "workspace")
    current_workspace = config.get("workspace", "")
    
    return jsonify({
        "config": {
            "provider": config.get("provider", ""),
            "model": config.get("model", ""),
            "apiKey": "********" if config.get("apiKey") else "",
            "apiBase": config.get("apiBase", ""),
            "workspace": current_workspace if current_workspace else default_workspace,
            "sandbox_enabled": bool(current_workspace),
        }
    })

@app.route("/api/config", methods=["POST"])
def update_config():
    """Update configuration"""
    global current_provider, current_model, agent_instance
    
    data = request.json
    provider = data.get("provider", "")
    model = data.get("model", "")
    api_key = data.get("apiKey", "")
    api_base = data.get("apiBase", "")
    
    if not provider:
        return jsonify({"success": False, "error": "请选择提供商"}), 400
    if not model:
        return jsonify({"success": False, "error": "请选择模型"}), 400
    if not api_key:
        return jsonify({"success": False, "error": "请输入 API Key"}), 400
    
    try:
        config = {
            "provider": provider,
            "model": model,
            "apiKey": api_key,
            "apiBase": api_base,
        }
        save_webui_config(config)
        
        # Re-initialize agent with new config
        current_provider = None
        current_model = None
        agent_instance = None
        init_agent()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/history", methods=["GET"])
def get_history():
    session_id = session.get("session_id", "webui:default")
    history = chat_history.get(session_id, [])
    return jsonify({"history": history})

@app.route("/api/clear", methods=["POST"])
def clear_history():
    session_id = session.get("session_id", "webui:default")
    chat_history[session_id] = []
    save_chat_history(chat_history)
    return jsonify({"status": "cleared"})

@app.route("/api/status", methods=["GET"])
def status():
    config = load_webui_config()
    
    if not config.get("apiKey"):
        return jsonify({
            "status": "not_configured",
            "message": "请先配置 API Key"
        })
    
    if config.get("provider") and config.get("model"):
        return jsonify({
            "status": "ready",
            "model": config.get("model", ""),
            "provider": config.get("provider", "")
        })
    
    return jsonify({
        "status": "not_configured",
        "message": "请完成配置"
    })

@app.route("/api/workspace", methods=["GET"])
def get_workspace():
    """Get current workspace configuration"""
    config = load_webui_config()
    workspace_path = config.get("workspace", "")
    default_workspace = str(Path.home() / ".zjclaw" / "workspace")
    
    return jsonify({
        "workspace": workspace_path if workspace_path else default_workspace,
        "is_default": not bool(workspace_path),
        "sandbox_enabled": bool(workspace_path)
    })

@app.route("/api/workspace", methods=["POST"])
def set_workspace():
    """Set workspace path"""
    global current_provider, current_model, agent_instance
    
    data = request.json
    workspace_path = data.get("workspace", "")
    
    if workspace_path:
        path = Path(workspace_path).expanduser().resolve()
        if not path.exists():
            return jsonify({"success": False, "error": "路径不存在"}), 400
        if not path.is_dir():
            return jsonify({"success": False, "error": "路径不是目录"}), 400
    
    try:
        config = load_webui_config()
        if workspace_path:
            config["workspace"] = workspace_path
        elif "workspace" in config:
            del config["workspace"]
        save_webui_config(config)
        
        # Re-initialize agent with new workspace
        agent_instance = None
        init_agent()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/workspace/validate", methods=["POST"])
def validate_workspace():
    """Validate a workspace path"""
    data = request.json
    workspace_path = data.get("workspace", "")
    
    if not workspace_path:
        return jsonify({"valid": False, "error": "路径不能为空"})
    
    path = Path(workspace_path).expanduser().resolve()
    
    if not path.exists():
        return jsonify({"valid": False, "error": "路径不存在"})
    
    if not path.is_dir():
        return jsonify({"valid": False, "error": "路径不是有效目录"})
    
    try:
        test_file = path / ".zjclaw_write_test"
        test_file.write_text("test")
        test_file.unlink()
        return jsonify({"valid": True, "path": str(path)})
    except Exception as e:
        return jsonify({"valid": False, "error": f"无写入权限: {str(e)}"})

@app.route("/api/skills", methods=["GET"])
def get_skills():
    """Get list of all installed skills"""
    skills = []
    
    # Get skills from all sources
    pkg_skills = Path(__file__).parent.parent / "zjclaw" / "skills"
    project_skills_dir = Path(__file__).parent.parent / "skills"
    system_skills_dir = project_skills_dir / "system-skills"
    user_skills_dir = project_skills_dir / "user-skills"
    
    def read_skill_meta(skill_path):
        meta = {"name": skill_path.name, "path": str(skill_path)}
        meta_file = skill_path / "_meta.json"
        if meta_file.exists():
            try:
                meta.update(json.loads(meta_file.read_text(encoding="utf-8")))
            except:
                pass
        skill_md = skill_path / "SKILL.md"
        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---")
                    if len(parts) >= 2:
                        frontmatter = parts[1]
                        for line in frontmatter.split("\n"):
                            if line.startswith("description:"):
                                meta["description"] = line.split("description:", 1)[1].strip()
                                break
            except:
                pass
        return meta
    
    # Built-in skills (zjclaw/skills)
    if pkg_skills.exists():
        for skill_dir in pkg_skills.iterdir():
            if skill_dir.is_dir():
                skill = read_skill_meta(skill_dir)
                skill["source"] = "builtin"
                skills.append(skill)
    
    # System skills
    if system_skills_dir.exists():
        for skill_dir in system_skills_dir.iterdir():
            if skill_dir.is_dir():
                skill = read_skill_meta(skill_dir)
                skill["source"] = "system"
                skills.append(skill)
    
    # User skills
    if user_skills_dir.exists():
        for skill_dir in user_skills_dir.iterdir():
            if skill_dir.is_dir():
                skill = read_skill_meta(skill_dir)
                skill["source"] = "user"
                skills.append(skill)
    
    return jsonify({"skills": skills})

@app.route("/api/update/check", methods=["GET"])
def check_update():
    """Check for available updates from GitHub"""
    try:
        from zjclaw.utils.update import get_update_checker
        checker = get_update_checker()
        result = checker.check_for_update()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "has_update": False,
            "error": str(e)
        }), 500

@app.route("/api/update/perform", methods=["POST"])
def perform_update():
    """Download and install the latest update"""
    try:
        from zjclaw.utils.update import get_update_checker
        checker = get_update_checker()
        
        # First check for update to get download URL
        update_info = checker.check_for_update()
        if not update_info.get("has_update"):
            return jsonify({
                "success": False,
                "message": "No update available"
            }), 400
        
        download_url = update_info.get("download_url")
        if not download_url:
            return jsonify({
                "success": False,
                "message": "No download URL available"
            }), 400
        
        result = checker.download_and_install_update(download_url)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Update failed: {str(e)}"
        }), 500

def create_app():
    Path(app.config["SESSION_FILE_DIR"]).mkdir(parents=True, exist_ok=True)
    return app

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"[ZJClaw] WebUI starting... http://localhost:{port}")
    print("   Press Ctrl+C to stop server")
    app.run(host="0.0.0.0", port=port, debug=debug)
