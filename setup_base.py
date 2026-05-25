from pathlib import Path

import requests

from config_base import BaseConfig

PROJECT_ROOT = Path(__file__).resolve().parent


def _resolve_from_project_root(path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def download_kanana(model_name: str, save_dir: Path) -> None:
    """
    Hugging Face에서 Kanana 모델을 다운로드하는 함수 (최초 1회 실행).
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer

    save_dir.mkdir(parents = True, exist_ok = True)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    tokenizer.save_pretrained(str(save_dir))
    model.save_pretrained(str(save_dir))

    print(f"✅ Kanana 모델과 토크나이저가 `{save_dir}`에 저장되었습니다.")


def download_bge_m3(model_name: str, save_dir: Path) -> None:
    """
    Hugging Face에서 BGE-M3 임베딩 모델을 다운로드하는 함수 (최초 1회 실행).
    """
    from sentence_transformers import SentenceTransformer

    save_dir.mkdir(parents = True, exist_ok = True)

    model = SentenceTransformer(model_name, device = "cpu")
    model.save(str(save_dir))

    print(f"✅ BGE-M3 모델이 `{save_dir}`에 저장되었습니다.")


def has_local_kanana(save_dir: Path) -> bool:
    """
    로컬 Kanana 모델 폴더에 필수 파일이 있는지 확인합니다.
    """
    required_files = [
        save_dir / "config.json",
        save_dir / "tokenizer_config.json",
    ]
    return all(path.exists() for path in required_files)


def has_local_bge_m3(save_dir: Path) -> bool:
    """
    로컬 BGE-M3 모델 폴더에 필수 파일이 있는지 확인합니다.
    """
    required_files = [
        save_dir / "config.json",
        save_dir / "modules.json",
        save_dir / "tokenizer.json",
        save_dir / "1_Pooling" / "config.json",
    ]
    normalize_dir = save_dir / "2_Normalize"
    return all(path.exists() for path in required_files) and normalize_dir.is_dir()


def ensure_kanana_model() -> None:
    """
    공통 Kanana 모델 존재 여부를 확인하고 필요 시 다운로드합니다.
    """
    model_name = BaseConfig.KANANA_MODEL_NAME
    save_dir = _resolve_from_project_root(BaseConfig.KANANA_MODEL_PATH)

    print("Kanana 모델 확인 중..")
    if has_local_kanana(save_dir):
        print("✅ Kanana 모델 확인 완료")
        return

    print("로컬 Kanana 모델이 없어 다운로드를 시작합니다..")
    download_kanana(model_name, save_dir)
    print("✅ Kanana 모델 준비 완료")


def ensure_bge_m3_model() -> None:
    """
    공통 BGE-M3 임베딩 모델 존재 여부를 확인하고 필요 시 다운로드합니다.
    """
    model_name = BaseConfig.BGE_M3_MODEL_NAME
    save_dir = _resolve_from_project_root(BaseConfig.BGE_M3_MODEL_PATH)

    print("BGE-M3 임베딩 모델 확인 중..")
    if has_local_bge_m3(save_dir):
        print("✅ BGE-M3 모델 확인 완료")
        return

    print("로컬 BGE-M3 모델이 없어 다운로드를 시작합니다..")
    download_bge_m3(model_name, save_dir)
    print("✅ BGE-M3 모델 준비 완료")

def ensure_dirs() -> None:
    # log 파일
    log_dir = _resolve_from_project_root(BaseConfig.LOG_DIR)
    log_dir.mkdir(parents = True, exist_ok = True)

def check_all_agents() -> None:
    for agent_id, url in BaseConfig.get_agent_ports().items():
        try:
            res = requests.get(f"{url}/health", timeout = 2)
            if res.status_code == 200:
                print(f"✅ {agent_id} Agent Setup 완료: {url}")
            else:
                print(f"❌ {agent_id} Agent 응답 이상: {url} - status {res.status_code}")
        except Exception as e:
            print(f"❌ {agent_id} Agent Setup 실패: {url} - {e}")


def main() -> None:
    print("초기 환경 점검을 시작합니다.")
    ensure_kanana_model()
    ensure_bge_m3_model()
    check_all_agents()
    print("모든 초기 설정이 완료되었습니다.")


if __name__ == "__main__":
    main()