import os
from pathlib import Path


class BaseConfig:
    """Agent 전역 설정 (모든 Agent에 공통적으로 사용되는 설정)"""

    PROJECT_ROOT = Path(__file__).resolve().parent

    # --------------------------------------------
    # Agent 설정 파일 (ID와 FastAPI 접속 주소 매핑)
    # --------------------------------------------
    AGENT_PORTS_CONFIG = {
        "legal": "http://localhost:8001",
        "news": "http://localhost:8002",
        "report": "http://localhost:8003",
        "stock": "http://localhost:8004",
        "trend": "http://localhost:8005",
    }

    # --------------------------------------------
    # 모델 설정
    # --------------------------------------------
    KANANA_MODEL_NAME = "kakaocorp/kanana-1.5-2.1b-instruct-2505"
    BGE_M3_MODEL_NAME = "BAAI/bge-m3"
    KANANA_MAX_NEW_TOKENS = int(os.getenv("KANANA_MAX_NEW_TOKENS", "512"))
    ENABLE_LOCAL_LOGGING = os.getenv("ENABLE_LOCAL_LOGGING", "false").lower() == "true"

    # --------------------------------------------
    # 경로 설정
    # --------------------------------------------
    DATA_ROOT = "./data"
    LOG_DIR = "./logs"
    KANANA_MODEL_PATH = "./Kanana_Model"
    BGE_M3_MODEL_PATH = "./models/bge-m3"

    # --------------------------------------------
    # 에이전트별로 필요한 것들
    # --------------------------------------------
    TICKER_MAP = {
        "엔비디아": "NVDA",
        "NVIDIA": "NVDA",
        "NVDA": "NVDA",
        "마이크로소프트": "MSFT",
        "Microsoft": "MSFT",
        "MSFT": "MSFT",
        "테슬라": "TSLA",
        "Tesla": "TSLA",
        "TSLA": "TSLA",
        "일라이 릴리": "LLY",
        "LLY": "LLY",
        "Eli Lilly": "LLY",
        "뱅크 오브 아메리카": "BAC",
        "BAC": "BAC",
        "Bank of America": "BAC",
        "코카-콜라": "KO",
        "Coca-Cola": "KO",
        "KO": "KO",
        "메타": "META",
        "Meta": "META",
        "META": "META",
        "애플": "AAPL",
        "Apple": "AAPL",
        "AAPL": "AAPL",
        "구글": "GOOG",
        "Google": "GOOG",
        "GOOG": "GOOG",
        "아마존": "AMZN",
        "Amazon": "AMZN",
        "AMZN": "AMZN"
    }

    @classmethod
    def get_agent_ports(cls):
        """Agent 포트 목록 반환"""
        return cls.AGENT_PORTS_CONFIG

    @classmethod
    def resolve_path(cls, path_value: str) -> str:
        """프로젝트 루트 기준 절대 경로로 변환"""
        path = Path(path_value)
        if path.is_absolute():
            return str(path)
        return str((cls.PROJECT_ROOT / path).resolve())

    @classmethod
    def resolve_data_path(cls, *parts: str) -> str:
        """공통 data 루트 기준 절대 경로로 변환"""
        path = Path(cls.DATA_ROOT)
        for part in parts:
            path /= part
        return cls.resolve_path(str(path))
