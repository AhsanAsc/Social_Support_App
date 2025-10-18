import httpx
import streamlit as st

st.set_page_config(page_title="Social Support AI — Intake", layout="wide")
st.title("Social Support AI — Intake")

api_base = "http://api:8080"

st.header("Create application")
with st.form("create_app"):
    full_name = st.text_input("Applicant full name", placeholder="Jane Doe")
    national_id = st.text_input("National ID (optional)")
    household_size = st.number_input("Household size", min_value=1, step=1, value=1)
    monthly_income = st.number_input("Monthly income (AED)", min_value=0, step=100, value=0)
    submitted = st.form_submit_button("Create")
if submitted and full_name.strip():
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.post(
                f"{api_base}/applications",
                json={
                    "applicant_full_name": full_name,
                    "applicant_national_id": national_id or None,
                    "household_size": int(household_size),
                    "monthly_income": float(monthly_income),
                },
            )
        if r.status_code == 200:
            st.session_state["app_id"] = r.json()["id"]
            st.success(f"Application created: {st.session_state['app_id']}")
        else:
            st.error(f"API error: {r.text}")
    except Exception as e:  # noqa: BLE001
        st.error(f"Request failed: {e}")

st.divider()

# Upload
st.header("Upload documents")
app_id = st.text_input("Application ID", value=st.session_state.get("app_id", ""))
doc_type = st.selectbox(
    "Document type",
    [
        "eid_front",
        "eid_back",
        "bank_statement",
        "salary_certificate",
        "credit_report",
        "utility_bill",
        "resume",
    ],
)
file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg", "docx", "xlsx"])
if st.button("Upload", disabled=not (app_id and file)):
    if not app_id:
        st.warning("Create or paste an Application ID first.")
    else:
        try:
            files = {"file": (file.name, file.getvalue(), file.type or "application/octet-stream")}
            data = {"doc_type": doc_type}
            with httpx.Client(timeout=60.0) as client:
                r = client.post(
                    f"{api_base}/applications/{app_id}/documents", files=files, data=data
                )
            if r.status_code == 200:
                st.success(f"Uploaded! Document ID: {r.json()['document_id']}")
            else:
                st.error(f"Upload failed: {r.text}")
        except Exception as e:  # noqa: BLE001
            st.error(f"Upload error: {e}")

# List docs for this app
if app_id:
    try:
        with httpx.Client(timeout=10.0) as client:
            q = client.get(f"{api_base}/applications/{app_id}/documents")
        if q.status_code == 200:
            docs = q.json().get("documents", [])
            st.subheader("Documents")
            for d in docs:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.code(f"{d['doc_type']}\n{d['filename']}")
                with col2:
                    st.caption(f"{d['content_type']} — {d['size_bytes']} bytes")
                with col3:
                    if st.button("Parse now", key=d["id"]):
                        with httpx.Client(timeout=60.0) as client:
                            pr = client.post(f"{api_base}/documents/{d['id']}/parse")
                        if pr.status_code == 200:
                            st.success(f"Parsed: {pr.json()['chunks']} chunks")
                        else:
                            st.error(f"Parse failed: {pr.text}")
        else:
            st.info("No documents yet.")
    except Exception as e:  # noqa: BLE001
        st.error(f"List docs failed: {e}")


st.divider()
st.header("Application status & evaluation")

app_id = st.text_input("Application ID (status/evaluate)", value=st.session_state.get("app_id", ""))

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Fetch status", disabled=not app_id):
        try:
            with httpx.Client(timeout=10.0) as client:
                r = client.get(f"{api_base}/applications/{app_id}/status")
            if r.status_code == 200:
                s = r.json()
                st.write(s)
                if s.get("missing_required"):
                    st.warning("Missing: " + ", ".join(s["missing_required"]))
                else:
                    st.success("All required docs uploaded.")
            else:
                st.error(r.text)
        except Exception as e:
            st.error(f"Status error: {e}")

with col_b:
    if st.button("Evaluate now", disabled=not app_id):
        try:
            with httpx.Client(timeout=20.0) as client:
                r = client.post(f"{api_base}/applications/{app_id}/evaluate")
            if r.status_code == 200:
                res = r.json()
                st.metric("Eligibility score", res.get("score", 0.0))
                st.caption(f"Status: {res.get('status')}")
                good = [x for x in res.get("rules", []) if x["passed"]]
                bad = [x for x in res.get("rules", []) if not x["passed"]]
                with st.expander("Passed checks", expanded=True):
                    for g in good:
                        st.write(f"✅ **{g['id']}** — {g['reason']} (w={g['weight']})")
                with st.expander("Needs attention", expanded=True):
                    for b in bad:
                        st.write(f"⚠️ **{b['id']}** — {b['reason']} (w={b['weight']})")
            else:
                st.error(r.text)
        except Exception as e:
            st.error(f"Eval error: {e}")

st.subheader("Bulk actions")
if st.button("Parse all required docs", disabled=not app_id):
    try:
        with httpx.Client(timeout=60.0) as client:
            r = client.post(f"{api_base}/applications/{app_id}/parse_all")
        if r.status_code == 200:
            st.success(f"Parsed {r.json().get('parsed_ok',0)}/{r.json().get('total',0)} documents")
        else:
            st.error(r.text)
    except Exception as e:
        st.error(f"Parse-all error: {e}")


st.subheader("Reviewer explanation")
if st.button("Generate explanation", disabled=not app_id):
    try:
        with httpx.Client(timeout=60.0) as client:
            r = client.post(f"{api_base}/applications/{app_id}/justify")
        if r.status_code == 200:
            ex = r.json()
            st.write(ex.get("explanation", ""))
        else:
            st.error(r.text)
    except Exception as e:
        st.error(f"Explain error: {e}")


st.divider()
st.header("Document search & Q&A")

app_id_rag = st.text_input("Application ID (RAG)", value=st.session_state.get("app_id", ""))
col1, col2 = st.columns([3, 1])
with col1:
    q = st.text_input(
        "Ask a question about this application",
        placeholder="e.g., What is the applicant's monthly income?",
    )
with col2:
    k = st.number_input("Top-K", min_value=1, max_value=12, value=6, step=1)

# Reindex
if st.button("Reindex documents", disabled=not app_id_rag):
    try:
        with httpx.Client(timeout=120.0) as client:
            r = client.post(f"{api_base}/applications/{app_id_rag}/reindex")
        if r.status_code == 200:
            st.success(f"Embedded chunks: {r.json().get('embedded',0)}")
        else:
            st.error(r.text)
    except Exception as e:
        st.error(f"Reindex error: {e}")

# Search
if st.button("Search", disabled=not (app_id_rag and q.strip())):
    try:
        with httpx.Client(timeout=20.0) as client:
            r = client.get(
                f"{api_base}/applications/{app_id_rag}/search", params={"q": q, "k": int(k)}
            )
        if r.status_code == 200:
            res = r.json()
            for i, h in enumerate(res.get("results", []), 1):
                st.write(f"[{i}] **{h['doc_type']}** p{h.get('page')}: {h['text']}")
        else:
            st.error(r.text)
    except Exception as e:
        st.error(f"Search error: {e}")

# Q&A
if st.button("Answer with LLM", disabled=not (app_id_rag and q.strip())):
    try:
        with httpx.Client(timeout=60.0) as client:
            r = client.post(f"{api_base}/applications/{app_id_rag}/qa", params={"q": q})
        if r.status_code == 200:
            res = r.json()
            st.write(res.get("answer", ""))
            with st.expander("Citations / Hits"):
                for i, h in enumerate(res.get("hits", []), 1):
                    st.write(f"[{i}] **{h['doc_type']}** p{h.get('page')}: {h['text']}")
        else:
            st.error(r.text)
    except Exception as e:
        st.error(f"Q&A error: {e}")
