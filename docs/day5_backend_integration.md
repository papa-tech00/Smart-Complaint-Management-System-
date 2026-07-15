# Day 5 – Backend Integration Planning
## Complaint Classification System

**Module:** ML API Integration Planning
**Status:** Planning Phase (Model training pending — no code implementation yet)

---

## 1. API Contract

This is the formal agreement between the **Backend Team** and the **ML Team** on how the complaint classification service will be consumed.

| Detail | Value |
|---|---|
| Endpoint | `/predict` |
| Method | `POST` |
| Content-Type | `application/json` |
| Authentication | None (internal service call, to be confirmed with backend team) |
| Base URL (Dev) | `http://localhost:5000` |
| Base URL (Prod) | *To be finalized after deployment* |
| Expected Response Time | < 1 second per request |
| Response Format | `application/json` |

**Field Contract**

| Field | Type | Required | Direction | Description |
|---|---|---|---|---|
| `complaint` | string | Yes | Request | Raw complaint text submitted by the citizen/user |
| `category` | string | Yes | Response | Predicted complaint category |
| `confidence` | float (0–1) | Yes | Response | Model's confidence score for the predicted category |

**Validation Rules**
- `complaint` must not be empty or null
- `complaint` should be a plain string (max length suggested: 500 characters)
- `complaint` must contain at least 3 words for meaningful classification

---

## 2. Request JSON

**Endpoint:** `POST /predict`

```json
{
  "complaint": "Street light is not working near the bus stand"
}
```

---

## 3. Response JSON

**Success Response — `200 OK`**

```json
{
  "category": "Street Light",
  "confidence": 0.98
}
```

---

## 4. Error Responses

| Scenario | Status Code | Response Body |
|---|---|---|
| Missing `complaint` field | `400 Bad Request` | `{ "error": "Missing 'complaint' field in request" }` |
| Empty `complaint` string | `400 Bad Request` | `{ "error": "'complaint' field cannot be empty" }` |
| Invalid JSON body | `400 Bad Request` | `{ "error": "Invalid JSON format" }` |
| Complaint exceeds max length | `400 Bad Request` | `{ "error": "'complaint' exceeds maximum allowed length of 500 characters" }` |
| Model/server failure | `500 Internal Server Error` | `{ "error": "Prediction service failed. Please try again later." }` |
| Service unavailable (model not loaded) | `503 Service Unavailable` | `{ "error": "Model is not ready. Please try again shortly." }` |

---

## 5. Integration Workflow Diagram

```
┌────────────┐        ┌────────────┐        ┌───────────────────┐        ┌────────────┐
│  Frontend   │  ───▶  │  Backend    │  ───▶  │   ML API            │  ───▶  │  ML Model   │
│ (User Form) │        │ (Server)    │        │ (Flask/FastAPI)      │        │ (.pkl file) │
└────────────┘        └────────────┘        └───────────────────┘        └────────────┘
      ▲                      │                        │                          │
      │                      │                        │  preprocess + predict    │
      │                      │                        │ ◀────────────────────────┘
      │                      │   category + confidence │
      │                      │ ◀────────────────────────┘
      │   Display result      │
      │ ◀────────────────────┘
      │                      │
      │                      ▼
      │              ┌───────────────┐
      │              │   Database      │
      │              │ (store result)  │
      │              └───────────────┘
```

**Step-by-step Flow**

1. User submits a complaint through the frontend form.
2. Backend server receives the complaint and validates basic input.
3. Backend sends a `POST /predict` request to the ML API with the complaint text.
4. ML API preprocesses the text (cleaning, tokenizing, vectorizing).
5. Preprocessed text is passed to the trained model for prediction.
6. Model returns a predicted category and confidence score.
7. ML API formats and sends the JSON response back to the backend.
8. Backend stores the result (category, confidence) in the database, linked to the original complaint record.
9. Backend forwards the categorized result to the frontend/admin dashboard for display.

---

## 6. Folder Structure

Planned structure for the ML API service (to be implemented after model training is complete):

```
ai-service/
│
├── app.py                     # Main API entry point (Flask/FastAPI)
├── model/
│   ├── model.pkl               # Trained classification model
│   └── vectorizer.pkl          # Text vectorizer (TF-IDF / embeddings)
│
├── utils/
│   ├── preprocess.py           # Text cleaning & preprocessing functions
│   └── predict.py              # Prediction logic wrapper
│
├── tests/
│   └── test_api.py             # Unit tests for /predict endpoint
│
├── config.py                    # Configuration (host, port, model path)
├── requirements.txt              # Python dependencies
└── README.md                      # API documentation for backend team
```

**Notes**
- `model/` will only be populated once training is complete.
- `app.py` will remain a thin layer — routing only, no business logic.
- `utils/predict.py` will isolate the model-calling logic so the model can be swapped/retrained without touching API code.

---

## 7. Backend Integration Notes

- The ML API will run as an **independent microservice**, separate from the main backend server.
- Communication will happen over **HTTP/REST** using JSON payloads.
- The backend team does **not** need access to the model file or training pipeline — only the API contract above.
- During development, the ML API will run locally (`localhost:5000`); a production URL will be shared once deployed.
- The ML API is **stateless** — every `/predict` call is independent, no session or history is maintained on the ML side.
- Backend is responsible for persisting results (category + confidence) in the database against the relevant complaint ID.
- If the ML service is down or times out, backend should handle it gracefully (e.g., mark complaint as "Pending Classification" and retry later).
- No authentication is planned for the internal call in the current phase; this can be added later (API key) if the service is exposed externally.
- Actual implementation of `/predict` will begin only after model training and evaluation are complete.

---

## 8. Sample Postman Request

**Setup in Postman**

| Field | Value |
|---|---|
| Method | `POST` |
| URL | `http://localhost:5000/predict` |
| Headers | `Content-Type: application/json` |
| Body Type | `raw` → `JSON` |

**Body:**
```json
{
  "complaint": "Street light is not working near the bus stand"
}
```

**Expected Response:**
```json
{
  "category": "Street Light",
  "confidence": 0.98
}
```

---

## 9. Sample cURL Request

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"complaint": "Street light is not working near the bus stand"}'
```

**Expected Output:**
```json
{
  "category": "Street Light",
  "confidence": 0.98
}
```

---

## 10. Communication Document for Backend Developer

**Subject: ML Complaint Classification API — Integration Details**

Hi [Backend Developer's Name],

Here are the integration details for the complaint classification ML service. Please review and let me know if any changes are needed on your end.

**Endpoint**
- `POST http://localhost:5000/predict` (local/dev environment for now)

**Request Format**
```json
{
  "complaint": "Street light is not working near the bus stand"
}
```

**Response Format**
```json
{
  "category": "Street Light",
  "confidence": 0.98
}
```

**Error Handling**
Please handle the following status codes on your end:
- `400` → Bad request (invalid/missing complaint text)
- `500` → Internal server error on the ML service
- `503` → ML service temporarily unavailable (model not loaded)

**Testing**
You can test the endpoint independently using the cURL/Postman samples above once the service is live.

**Timeline**
The model is currently in the training phase. The actual `/predict` endpoint will be implemented and deployed once training and evaluation are complete. I'll share the updated base URL and any changes to this contract at that point.

**Open Questions for You**
1. Do you need any authentication (API key) on this endpoint, or is internal network access sufficient?
2. Should the ML API be called synchronously (backend waits for response) or should we consider a queue-based async approach for scale?
3. What complaint ID or reference field, if any, should be echoed back in the response for tracking?

Thanks,
[Your Name]

---

*End of Day 5 – Backend Integration Planning Document*