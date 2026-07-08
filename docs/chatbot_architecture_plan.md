# AetherAI: Comprehensive Multi-Modal Chatbot Architecture

## 1. Executive Summary

This document outlines the complete architectural overhaul of AetherAI. The system is transitioning from a static, form-based triage tool into an **Event-Driven, Multi-Modal Conversational Diagnostic Agent**.

The patient interacts directly with the AI in natural language (Bangla or English). The AI dynamically controls the flow of the conversation, using "Tool Calling" to pop up Interactive UI Cards that prompt the user for real-world sensor data (Audio for Coughs, Video for Heart/Respiratory Rate). Once the AI has collected enough conversational and sensor data, it synthesizes a final medical diagnosis and generates a formal PDF prescription.

---

## 2. Technology Stack

### Frontend (The Patient Client)

* **Framework:** React 18 (via Vite), TypeScript, TailwindCSS.
* **Browser APIs:**
  * `SpeechRecognition` (Web Speech API) for Voice-to-Text (Bangla & English).
  * `SpeechSynthesis` for Text-to-Voice output.
  * `MediaDevices.getUserMedia()` for microphone and webcam access.

### Backend (The AI Orchestrator)

* **Framework:** FastAPI (Python 3.10+), Uvicorn.
* **Database:** SQLite + SQLAlchemy (Async).
* **AI Engine:** Google Gemini 1.5 Flash (via `google-genai` SDK).
* **Vitals Processing:** `yarPPG` (Python library for remote photoplethysmography via video).
* **Acoustic Processing:** Gemini 1.5 Native Audio Analysis (bypassing Hugging Face).
* **Reporting:** `reportlab` for PDF generation.

---

## 3. Database Schema Updates

To support persistent, stateful conversations, the database schema will be updated:

* **`Patients` Table:** Updated to store basic onboarding demographic data (Age, Gender, Fever status, Smoker status) and language preference.
* **`ChatHistory` Table (NEW):**
  * `message_id` (UUID)
  * `patient_id` (Foreign Key)
  * `role` (Enum: `user`, `model`, `system`)
  * `content` (String/Text)
  * `timestamp` (DateTime)
* **`TestResults` Table (NEW):**
  * Stores the raw outputs of the sensor tests (e.g., `{"test_type": "vitals", "heart_rate": 85, "respiratory_rate": 18}`).

---

## 4. Gemini Function Calling (The "Tools")

The core of the dynamic architecture relies on configuring Gemini 1.5 with explicitly defined Tools. The backend will initialize the `genai.Client` with the following function declarations:

1. **`trigger_cough_test()`**:
    * *Description to LLM:* "Call this tool if the patient reports coughing, wheezing, or chest congestion. It will ask the patient to record a 5-second audio clip of their cough."
2. **`trigger_vitals_test()`**:
    * *Description to LLM:* "Call this tool to measure the patient's Heart Rate (BPM) and Respiratory Rate. It will ask the patient to look into their camera for 10 seconds."
3. **`finalize_diagnosis()`**:
    * *Description to LLM:* "Call this tool when you have collected enough conversational and sensor data to confidently diagnose the patient. Pass the final diagnosis and recommended medicines as arguments."

---

## 5. System Data Flow & API Architecture

### A. Conversational Loop (`POST /api/v1/chat`)

1. **Request:** Frontend sends `{ "patient_id": "123", "message": "My chest hurts." }`.
2. **Backend:** Appends the message to the DB, pulls the last 10 messages (context window), and sends them to Gemini.
3. **Gemini Decision:**
    * *Path 1 (Text):* Gemini replies with text. Backend returns `{ "type": "message", "content": "How long has it been hurting?" }`.
    * *Path 2 (Tool Call):* Gemini decides a test is needed and calls `trigger_vitals_test()`. Backend intercepts this and returns `{ "type": "tool_trigger", "action": "show_vitals_card" }`.

### B. Sensor Data Loop (`POST /api/v1/test/upload`)

When the frontend receives a `tool_trigger`, a Modal Card pops up.

1. **Request:** User records a 10-second webcam video. Frontend sends the `.webm` file to `/test/upload`.
2. **Backend Processing (`yarPPG`):** The backend saves the video temporarily and runs the `yarPPG` engine on it to extract Heart Rate and Respiratory Rate.
3. **Injection:** The backend saves these results to the DB, injects them into the chat history as a `system` message (e.g., *"System Note: Vitals scan complete. HR: 88 BPM, RR: 16 breaths/min"*), and re-prompts Gemini.
4. **Response:** Gemini acknowledges the new data in its next chat reply.

---

## 6. Frontend Component Breakdown

* **`ChatWindow` Component:** The main UI container. Maps over the message history array.
* **`VoiceInput` Component:** A microphone button. When held, uses `SpeechRecognition` to transcribe audio to text in real-time.
* **Interactive Modal Cards:**
  * **`CoughCard`:** Renders a 5-second countdown timer, requests microphone access, captures a `.wav` Blob, and POSTs it.
  * **`VitalsCard`:** Renders a 10-second countdown timer, requests webcam access, draws a bounding box over the user's face, captures a `.webm` Blob, and POSTs it.

---

## 7. Granular Execution Roadmap

### Phase 1: Database & API Foundation (Backend)

1. Scrap `predict.py` and old SQLite schema.
2. Implement the new `ChatHistory` and `TestResults` SQLAlchemy models.
3. Build the `/api/v1/chat` endpoint and wire up Gemini 1.5 Flash with the basic chat history loop (no tools yet).

### Phase 2: Conversational UI (Frontend)

1. Build the React Chat Interface.
2. Implement Web Speech API for Bangla/English STT (Speech-to-Text).
3. Ensure messages flow seamlessly back and forth between the UI and the Database.

### Phase 3: Sensor APIs & Gemini Tools (Backend)

1. Implement the Gemini Function Calling schema in the backend.
2. Build the `/api/v1/test/upload` endpoint.
3. Integrate the `yarPPG` library into the backend for video processing.
4. Integrate the native Gemini File API for `.wav` processing.

### Phase 4: UI Sensor Cards (Frontend)

1. Build the `CoughCard` and `VitalsCard` React components.
2. Implement the `MediaRecorder` API to capture and transmit the Blobs.
3. Wire the frontend to listen for `tool_trigger` events from the backend to display these cards.

### Phase 5: PDF Generation & Polish (Full Stack)

1. Refactor `reporting/service.py` to accept the entire Chat History and Sensor Data arrays.
2. Add the "Generate Prescription" trigger.
3. **(Stretch Goal):** Implement a Python OpenCV script for Anemia/Jaundice detection as a third Tool Call.
