#!/usr/bin/env bash
set -euo pipefail

API=http://localhost:8080
UI=http://localhost:8501
OLLAMA_HOST=${OLLAMA_HOST:-http://localhost:11435}

echo "== Bring up stack =="
make up
sleep 2

echo "== Health checks =="
curl -fsS $API/healthz | jq

echo "== Ollama model tags (if empty, we’ll pull DEFAULT_MODEL) =="
curl -fsS $OLLAMA_HOST/api/tags | jq || true
make ollama-pull || true

echo "== Create application =="
APP_JSON=$(curl -fsS -X POST $API/applications \
  -H 'content-type: application/json' \
  -d '{"applicant_full_name":"Test User","household_size":3,"monthly_income":1500}')
APP_ID=$(echo "$APP_JSON" | jq -r .id)
echo "APP_ID=$APP_ID"

# --- adjust the three paths below to files you actually have ---
PDF_PATH=${PDF_PATH:-"$(pwd)/Demand_Forecasting_Report.pdf"}
EID_FRONT=${EID_FRONT:-"$(pwd)/Id.jpg"}
EID_BACK=${EID_BACK:-"$(pwd)/Id.jpg"}   # for demo, reuse front; replace with real back if you have it

echo "== Upload docs =="
UPLOAD_URL="$API/applications/$APP_ID/documents"

PDF_JSON=$(curl -fsS -F "doc_type=bank_statement" -F "file=@${PDF_PATH};type=application/pdf" "$UPLOAD_URL")
PDF_ID=$(echo "$PDF_JSON" | jq -r .document_id)
echo "PDF_ID=$PDF_ID"

FR_JSON=$(curl -fsS -F "doc_type=eid_front" -F "file=@${EID_FRONT};type=image/jpeg" "$UPLOAD_URL")
FR_ID=$(echo "$FR_JSON" | jq -r .document_id)
echo "FR_ID=$FR_ID"

BK_JSON=$(curl -fsS -F "doc_type=eid_back" -F "file=@${EID_BACK};type=image/jpeg" "$UPLOAD_URL")
BK_ID=$(echo "$BK_JSON" | jq -r .document_id)
echo "BK_ID=$BK_ID"

echo "== Parse all =="
curl -fsS -X POST "$API/applications/$APP_ID/parse_all" | jq

echo "== Status should show no missing required =="
curl -fsS "$API/applications/$APP_ID/status" | jq

echo "== Index all (RAG embeddings) =="
curl -fsS -X POST "$API/applications/$APP_ID/reindex" | jq

echo "== Semantic search =="
curl -fsS "$API/applications/$APP_ID/search?q=monthly%20income&k=6" | jq

echo "== QA over RAG =="
curl -fsS -X POST "$API/applications/$APP_ID/qa?q=Summarize%20income%20and%20household" | jq

echo "== Deterministic justification (LLM) =="
curl -fsS -X POST "$API/applications/$APP_ID/justify" | jq

echo "== Agent Orchestrator (LangGraph) =="
curl -fsS -X POST "$API/applications/$APP_ID/agent/run" | jq

echo "== Train ML (LogReg) on current apps =="
curl -fsS -X POST "$API/ml/train" | jq

echo "== ML score (with per-feature contributions) =="
curl -fsS "$API/applications/$APP_ID/ml_score" | jq

echo "== UI =="
echo "Open $UI"
