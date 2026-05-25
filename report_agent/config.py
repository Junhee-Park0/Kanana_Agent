from __future__ import annotations

import os
from dataclasses import dataclass

from utils.config_bootstrap import bootstrap_config

_CTX = bootstrap_config(__file__, dotenv_mode="project")
BaseConfig = _CTX.base_config


@dataclass(frozen=True)
class Settings:
    upstage_api_key: str | None = os.getenv("UPSTAGE_API_KEY") or None
    huggingfacehub_api_token: str | None = os.getenv("HUGGINGFACEHUB_API_TOKEN") or None
    kanana_model_id: str = os.getenv("KANANA_MODEL_ID", BaseConfig.KANANA_MODEL_NAME)
    kanana_model_path: str = BaseConfig.resolve_path(BaseConfig.KANANA_MODEL_PATH)
    app_port: int = int(os.getenv("PORT_NUM", "8000"))
    log_dir: str = BaseConfig.resolve_path(BaseConfig.LOG_DIR)
    runtime_dir: str = BaseConfig.resolve_path(
        os.getenv("RUNTIME_DIR", BaseConfig.resolve_data_path("report_data", "runtime_files"))
    )


settings = Settings()
