import os

from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

CHROMA_DB_PATH = "chroma_db"

KNOWLEDGE_PATH = "knowledge"

EXTERNAL_REPOS_PATH = "external_repos"

PDF_REPORT_NAME = "compliance_report.pdf"

SPDX_REPORT_NAME = "spdx_report.json"

LOG_FILE = "license_scanner.log"