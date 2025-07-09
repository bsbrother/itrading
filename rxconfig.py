import reflex as rx

config = rx.Config(
    app_name="itrading",
    frontend_port=3000,
    backend_port=8000,
    api_url="http://127.0.0.1:8000",
    deploy_url=None,
    backend_host="127.0.0.1",
    frontend_host="127.0.0.1",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    redis_url=None,
    telemetry_enabled=False,
)
