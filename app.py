"""
app.py — IndicAI Multilingual Intent Classifier
Streamlit app: load model → classify text → display results

Run:
    streamlit run app.py

Requirements:
    model/classifier.pkl and model/label_encoder.pkl must exist.
    If they don't exist, run train_model.ipynb first (or use the
    inline training button in this app).
"""

import re
import pickle
import unicodedata
from pathlib import Path

import numpy as np
import streamlit as st
from scipy.stats import entropy as scipy_entropy

# ── Page config (must be FIRST Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="IndicAI — Intent Classifier",
    page_icon="🧠",
    layout="centered",
)

# ── Import futuristic UI system ───────────────────────────────────────────
from ui_design import (
    load_ui,
    render_3d_background,
    render_particles,
    render_header,
    render_sidebar,
    render_footer,
    render_hologram_effect,
    render_glass_container,
    render_result_card,
    render_loading_animation,
    render_divider,
)

# ── Paths ─────────────────────────────────────────────────────────────────
MODEL_DIR    = Path("model")
CLF_PATH     = MODEL_DIR / "classifier.pkl"
LE_PATH      = MODEL_DIR / "label_encoder.pkl"
INTENTS_PATH = Path("intents.json")

EMBEDDING_MODEL      = "paraphrase-multilingual-MiniLM-L12-v2"
CONFIDENCE_THRESHOLD = 0.35   # below → "not recognized confidently"
ENTROPY_THRESHOLD    = 2.60   # above → "not recognized confidently"

# ── Intent display metadata ───────────────────────────────────────────────
INTENT_META = {
    "greeting":         {"icon": "👋", "color": "#a29bfe", "label": "Greeting"},
    "complaint":        {"icon": "📢", "color": "#fd79a8", "label": "Complaint"},
    "support_request":  {"icon": "🛠️",  "color": "#6c5ce7", "label": "Support Request"},
    "payment_issue":    {"icon": "💳", "color": "#ff9f43", "label": "Payment Issue"},
    "refund_request":   {"icon": "💰", "color": "#00b894", "label": "Refund Request"},
    "cancel_request":   {"icon": "❌", "color": "#ff6b6b", "label": "Cancel Request"},
    "recharge_request": {"icon": "⚡", "color": "#ffd93d", "label": "Recharge Request"},
    "unknown_intent":   {"icon": "❓", "color": "#636e72", "label": "Unknown Intent"},
}


# ══════════════════════════════════════════════════════════════════════════
# GARBAGE DETECTION
# ══════════════════════════════════════════════════════════════════════════

_VOWELS = set('aeiouAEIOU')


def is_garbage(text: str) -> bool:
    """
    Returns True for: empty, symbol-only, emoji-only, digit-only,
    repeated-char spam, keyboard-smash (low vowel ratio), repeating n-gram spam.
    Safe for Telugu / Tamil / Hindi / Devanagari / mixed scripts.
    """
    t = text.strip()
    if not t or not t.replace(" ", ""):
        return True

    if not re.search(r'[a-zA-Z\u0900-\u097F\u0C00-\u0C7F\u0B80-\u0BFF\u0A80-\u0AFF]', t):
        return True

    if re.match(r'^\d+$', t):
        return True

    if re.match(r'^(.)\1{4,}$', t, re.UNICODE):
        return True

    letters = re.sub(
        r'[^a-zA-Z\u0900-\u097F\u0C00-\u0C7F\u0B80-\u0BFF\u0A80-\u0AFF]',
        '', t
    )
    if len(letters) < 2:
        return True

    latin = re.sub(r'[^a-zA-Z]', '', t)
    if len(latin) >= 5:
        vowel_ratio = sum(1 for c in latin if c in _VOWELS) / len(latin)
        if vowel_ratio < 0.20:
            return True

    if len(t) >= 6:
        for n in (2, 3):
            if len(t) >= n * 3:
                chunk = t[:n]
                if t == chunk * (len(t) // n) and len(set(chunk)) <= 3:
                    return True

    return False


def preprocess(text: str) -> str:
    """Normalize whitespace. Preserve all multilingual scripts."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text.lower()


# ══════════════════════════════════════════════════════════════════════════
# MODEL LOADING  (cached — loaded once per session)
# ══════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner="Loading sentence encoder…")
def load_encoder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBEDDING_MODEL)


@st.cache_resource(show_spinner="Loading classifier…")
def load_classifier():
    if not CLF_PATH.exists() or not LE_PATH.exists():
        return None, None
    with open(CLF_PATH, "rb") as f:
        clf = pickle.load(f)
    with open(LE_PATH, "rb") as f:
        le = pickle.load(f)
    return clf, le


# ══════════════════════════════════════════════════════════════════════════
# PREDICTION
# ══════════════════════════════════════════════════════════════════════════

def predict(text: str, encoder, clf, le) -> dict:
    """
    Full pipeline:
      1. Garbage check → return "Unknown / Invalid Input"
      2. Embed with SentenceTransformer
      3. Logistic Regression predict_proba
      4. Confidence / entropy thresholding
      5. Return structured result dict
    """
    if is_garbage(text):
        return {
            "status":     "invalid",
            "message":    "Unknown / Invalid Input",
            "intent":     None,
            "confidence": 0.0,
            "all_probs":  {},
        }

    clean = preprocess(text)
    emb   = encoder.encode([clean], normalize_embeddings=True, show_progress_bar=False)

    probs    = clf.predict_proba(emb)[0]
    max_prob = float(probs.max())
    ent      = float(scipy_entropy(probs))

    if max_prob < CONFIDENCE_THRESHOLD or ent > ENTROPY_THRESHOLD:
        return {
            "status":     "low_confidence",
            "message":    "Intent not recognized confidently",
            "intent":     None,
            "confidence": round(max_prob, 4),
            "entropy":    round(ent, 4),
            "all_probs":  {c: round(float(p), 4) for c, p in zip(le.classes_, probs)},
        }

    pred_idx  = int(probs.argmax())
    intent    = le.classes_[pred_idx]
    all_probs = {c: round(float(p), 4) for c, p in zip(le.classes_, probs)}

    return {
        "status":     "ok",
        "message":    "",
        "intent":     intent,
        "confidence": round(max_prob, 4),
        "entropy":    round(ent, 4),
        "all_probs":  all_probs,
    }


# ══════════════════════════════════════════════════════════════════════════
# INLINE TRAINING  (fallback if model files are missing)
# ══════════════════════════════════════════════════════════════════════════

def train_and_save(encoder):
    """Train from intents.json and save model/ files. Called only when needed."""
    import json
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder

    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts, labels = [], []
    for intent, examples in data["training_data"].items():
        for ex in examples:
            ex = ex.strip()
            if ex and not is_garbage(ex):
                texts.append(ex.lower())
                labels.append(intent)

    status_box = st.empty()
    status_box.info(f"Generating embeddings for {len(texts)} samples…")

    batch_size = 64
    all_embs   = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i: i + batch_size]
        embs  = encoder.encode(batch, normalize_embeddings=True, show_progress_bar=False)
        all_embs.append(embs)
    X = np.vstack(all_embs)

    le = LabelEncoder()
    y  = le.fit_transform(labels)

    status_box.info("Training classifier…")
    clf = LogisticRegression(
        max_iter=2000, C=5.0,
        class_weight="balanced",
        multi_class="multinomial",
        solver="lbfgs",
        random_state=42,
    )
    clf.fit(X, y)

    MODEL_DIR.mkdir(exist_ok=True)
    with open(CLF_PATH, "wb") as f:
        pickle.dump(clf, f)
    with open(LE_PATH, "wb") as f:
        pickle.dump(le, f)

    status_box.success("✅ Model trained and saved to model/")
    return clf, le


# ══════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════

def main():

    # ── 1. Inject UI system (CSS + JS + background layers) ───────────────
    load_ui()
    render_3d_background()
    render_particles()

    # ── 2. Cinematic header ───────────────────────────────────────────────
    render_header()

    # ── 3. Load encoder (always needed) ──────────────────────────────────
    encoder = load_encoder()

    # ── 4. Load / train classifier ────────────────────────────────────────
    clf, le = load_classifier()

    if clf is None:
        render_glass_container("""
            <div style="font-family:'Orbitron',monospace;font-size:0.8rem;
                        color:#ffd93d;letter-spacing:0.12em;margin-bottom:8px;">
              ⚠ MODEL FILES NOT FOUND
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.92rem;color:#94a3b8;">
              <code style="color:#00f5ff;background:rgba(0,245,255,0.07);
                           padding:2px 6px;border-radius:4px;font-size:0.82rem;">
                model/classifier.pkl
              </code>
              and
              <code style="color:#00f5ff;background:rgba(0,245,255,0.07);
                           padding:2px 6px;border-radius:4px;font-size:0.82rem;">
                model/label_encoder.pkl
              </code>
              not found.<br><br>
              Run <strong>train_model.ipynb</strong> — or click below to train now.
            </div>
        """)
        if st.button("🚀  INITIALIZE NEURAL ENGINE", type="primary"):
            with st.spinner("Training… this may take 1–2 minutes."):
                clf, le = train_and_save(encoder)
            st.cache_resource.clear()
            st.rerun()
        render_footer()
        return

    # ── 5. Sidebar ────────────────────────────────────────────────────────
    with st.sidebar:
        render_sidebar()

        st.markdown("### 📌 Supported Intents")
        for key, meta in INTENT_META.items():
            if key != "unknown_intent":
                st.markdown(
                    f"<div style='padding:5px 0;font-family:Rajdhani,sans-serif;"
                    f"font-size:0.95rem;'>{meta['icon']} <strong>{meta['label']}</strong></div>",
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("### ⚙️ Model Info")
        st.code(
            f"Encoder : {EMBEDDING_MODEL}\n"
            f"Conf thr: {CONFIDENCE_THRESHOLD:.0%}\n"
            f"Entr thr: {ENTROPY_THRESHOLD}",
            language="text",
        )

        st.markdown("---")
        st.markdown("### 🧪 Rejected Inputs")
        st.caption(
            "These return **Unknown / Invalid Input**:\n"
            "- `@@@@@` · `123456` · `aaaaaaa`\n"
            "- `🙂🙂🙂` · `qwerty` · `asdasd`\n"
            "- pure symbols or empty text"
        )

        st.markdown("---")
        st.caption("IndicAI v1.0 · College Project")

    # ── 6. Input section ──────────────────────────────────────────────────
    render_hologram_effect("▸ NEURAL INPUT INTERFACE")

    examples = [
        "",
        "hi, how are you?",
        "payment fail ho gaya",
        "cancel my order please",
        "refund kavali",
        "app kaam nahi kar raha",
        "recharge cheyyali",
        "service romba mosam",
        "123456",
        "@@@@@",
    ]

    selected = st.selectbox(
        "Try an example (or type your own below):",
        options=examples,
        format_func=lambda x: "— select an example —" if x == "" else x,
    )

    user_input = st.text_area(
        label="Your message:",
        value=selected,
        height=90,
        placeholder="Type anything in English, Hindi, Telugu, Tamil, or Hinglish…",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        classify_btn = st.button(
            "CLASSIFY →",
            type="primary",
            use_container_width=True,
        )

    # ── 7. Run prediction ─────────────────────────────────────────────────
    if classify_btn:
        if not user_input or not user_input.strip():
            st.error("⚠️  Please enter some text first.")
        else:
            placeholder = render_loading_animation()
            result      = predict(user_input.strip(), encoder, clf, le)
            placeholder.empty()

            render_divider()
            render_hologram_effect("▸ CLASSIFICATION RESULT")
            render_result_card(result, INTENT_META)

    # ── 8. Footer ─────────────────────────────────────────────────────────
    render_divider()
    render_footer()


if __name__ == "__main__":
    main()
