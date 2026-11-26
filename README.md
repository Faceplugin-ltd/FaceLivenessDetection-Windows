<div align="center">
<img alt="FacePlugin" src="https://raw.githubusercontent.com/Faceplugin-ltd/faceplugin-assets/main/brand/logo.png" width="400"/>
</div>

#### 🌐 Company Site - [Here](https://faceplugin.com)
#### 🤗 Hugging Face - [Here](https://huggingface.co/FacePlugin-Ltd)
#### 🛟 Help Center - [Here](https://doc.faceplugin.com)
#### 🐳 Docker Hub - [Here](https://hub.docker.com/r/faceplugin/face-liveness)

# FacePlugin Face Liveness Detection — Windows (Fully On-Premise)

Jump: [Quick start](#quick-start) · [Get the runtime](#get-the-runtime) · [Start the API](#start-the-api) · [SDK License](#sdk-license) · [Try it](#try-it) · [Setup on your own app](#setup-on-your-own-app) · [About SDK](#about-sdk)

## Quick start

- [ ] Clone [FaceLivenessDetection-Windows](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Windows)
- [ ] Download `runtime.zip` from [Releases](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Windows/releases/tag/latest) and extract it into `lib\cpu\` — [Get the runtime](#get-the-runtime)
- [ ] `pip install -r requirements.txt` then `run.bat` — API on **8093**
- [ ] Copy the machine code (`FPMC1.…`) from the terminal, or `GET /api/machinecode`
- [ ] [Contact us](#contact) for a license key → paste it at the prompt, or `POST /api/activate`
- [ ] Try it with Postman, curl, or the Gradio demo on **9093** (`run_demo.bat`)

No Docker on Windows. For Docker, use [FaceLivenessDetection-Docker](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Docker).

## Introduction

FacePlugin **Face Liveness Detection for Windows** is a fully on-premise anti-spoofing engine for KYC and remote identity verification. It answers one question about one photo — *is this a real face in front of the camera, or a presentation attack?* — and returns Real / Spoof with a score. **Passive**: nothing is asked of the person, and a single RGB frame is enough. No depth camera, no infrared, no extra hardware.

It detects printed photos, screen replays (photo and video), 3D masks, and deepfakes handled as one more kind of spoof.

This repository is **standalone**: clone it, drop the runtime into `lib\cpu\`, and run. No other FacePlugin repository is required.

All processing stays on your machine. **No** biometric data is sent to FacePlugin — built for banking, eKYC, and on-premise compliance workflows.

**Windows** product: native x64 runtime, a local HTTP API, and a Gradio demo. **CPU-only**.

### Main Functionalities

| Feature | API |
| ------- | --- |
| **Passive face liveness** — score one RGB image for presentation attacks | `POST /api/liveness` · `sdk.liveness` |
| Printed photo, screen replay, 3D mask and deepfake detection | same call |
| Score, Real/Spoof verdict, pass flag | `data.score` · `data.result` · `data.pass` |
| Health / machine code / activate / license | `GET /api/health` · `GET /api/machinecode` · `POST /api/activate` · `GET /api/licenseStatus` |
| Which runtime is loaded | `GET /api/backend` |

Score **≥ 0.5** → `result: "Real"`, `pass: true`. Score **< 0.5** → `result: "Spoof"`, `pass: false`.

`POST /api/check_liveness` is an alias of `/api/liveness`. Routes are `/api/*`; there is no version segment.

### Benchmarks

Passive mode, at the default threshold of **0.5**:

| Metric | This product (server) |
| ------ | --------------------- |
| **BPCER** — real faces wrongly rejected | **0%** (none observed) |
| **APCER** — attacks wrongly accepted | **0.5 – 1.5%** |

Measured by FacePlugin QA following the **ISO/IEC 30107-3** methodology, against four presentation attack instrument species: printed photo, screen replay (photo), screen replay (video), and a painted 3D resin mask.

> This is an **internal evaluation, not an independent laboratory result**, and no iBeta certification is claimed. A 0% BPCER means no rejection was *observed* — for 600 presentations the one-sided 95% upper bound is about 0.5%. Ask us for the full PAD evaluation report.

Figures: [doc.faceplugin.com](https://doc.faceplugin.com/products/face-recognition-sdk/liveness-detection-sdk).

### Product List

| Product | Repository |
| ------- | ---------- |
| **Face Liveness Detection — Windows** | **[FaceLivenessDetection-Windows](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Windows)** **(this repo)** |
| Face Liveness Detection — Docker | [Docker Hub](https://hub.docker.com/r/faceplugin/face-liveness) · [FaceLivenessDetection-Docker](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Docker) |
| Face Recognition — Windows | [FaceRecognition-Windows](https://github.com/Faceplugin-ltd/FaceRecognition-Windows) |
| Face Recognition — Docker | [Docker Hub](https://hub.docker.com/r/faceplugin/face-recognition) · [FaceRecognition-Docker](https://github.com/Faceplugin-ltd/FaceRecognition-Docker) |

### Related products

On-device liveness apps for mobile:

- **Android** — [FaceLivenessDetection-Android](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Android)
- **iOS** — [FaceLivenessDetection-iOS](https://github.com/Faceplugin-ltd/FaceLivenessDetection-iOS)

On-device face recognition + liveness apps for mobile:

- **Android** — [FaceRecognition-LivenessDetection-Android](https://github.com/Faceplugin-ltd/FaceRecognition-LivenessDetection-Android)
- **iOS** — [FaceRecognition-LivenessDetection-iOS](https://github.com/Faceplugin-ltd/FaceRecognition-LivenessDetection-iOS)

## Before you start

| Step | What you need |
| ---- | ------------- |
| 1 | Windows 10/11 **x64**, Python 3.10+ |
| 2 | The runtime in `.\lib\cpu\` — see [Get the runtime](#get-the-runtime) |
| 3 | Start **without** a license, copy the machine code, send it to FacePlugin ([contact](#contact)), then activate with your license key |

You do **not** need a license to start the API. Product endpoints unlock after you activate.

### System requirements

| Item | Minimum | Recommended |
| ---- | ------- | ----------- |
| CPU | 4 cores | 4 cores |
| RAM | 4 GB | 8 GB |
| Disk | 4 GB | 8 GB |
| OS | Windows 10 x64 | Windows 11 x64 |
| Python | 3.10+ | 3.12 |

## Get the runtime

`.\lib\cpu\` is empty on GitHub because the native binaries and model files are too large. This product is **CPU-only** — there is no `gpu\` package.

**[Download the runtime from Releases](https://github.com/Faceplugin-ltd/FaceLivenessDetection-Windows/releases/tag/latest)**

The release holds one archive, **`runtime.zip`** — there is a single runtime for this product.

1. Clone the repo (if you have not already):

```bat
git clone https://github.com/Faceplugin-ltd/FaceLivenessDetection-Windows.git
cd FaceLivenessDetection-Windows
```

2. Open the release page above and download **`runtime.zip`**.
3. Extract it and put every file **directly** into `.\lib\cpu\` — not inside a nested subfolder.

```text
FaceLivenessDetection-Windows/
└── lib/
    └── cpu/
        ├── FaceLivenessSDK.dll
        ├── facerec.dll
        ├── fal.fpk
        ├── onnxruntime.dll
        └── ... (OpenCV and VC++ runtime DLLs from the archive)
```

Wrong layout: `lib\cpu\SomeFolder\FaceLivenessSDK.dll` (a nested folder breaks local runs).

```bat
dir lib\cpu\FaceLivenessSDK.dll
dir lib\cpu\facerec.dll
dir lib\cpu\fal.fpk
```

The VC++ runtime DLLs ship **inside** `lib\cpu\`, so you do not need to install `vcredist`. `run.bat` puts `lib\cpu` on `PATH`.

## Start the API

You can start **without** a license — the server prints your machine code on startup.

```bat
pip install -r requirements.txt
run.bat
```

API: **http://127.0.0.1:8093**

The API starts even if activation fails. Copy the **machine code** (`FPMC1.…`) from the log and send it to FacePlugin. When prompted, paste your license key, or skip and activate later.

<p align="center">
 <img src="https://raw.githubusercontent.com/Faceplugin-ltd/faceplugin-assets/main/screenshots/face-liveness/windows/api-start.png" alt="run.bat: copy machine code (FPMC1), paste license key, SDK ready on port 8093" width="900"/>
</p>

## SDK License

Licenses are **offline** and bound to your machine. Offline cryptography is pre-packaged within the SDK — no third-party licensing libraries or external OpenSSL installations are required.

### How to get a license

1. **Start the server** ([above](#start-the-api)). A license is not required for the first start.
2. **Copy the machine code** from the terminal — it looks like **`FPMC1.…`** — or fetch it with `GET /api/machinecode`.
3. **Send that machine code** to FacePlugin ([contact](#contact)). We will issue a license key for that code.
4. **Activate** with the license key:

```bat
:: After run.bat, paste the license key at the terminal prompt. You can try 3 times.

:: Or paste the license key into .\license.txt (overwrite the file), then:

curl -s -X POST http://127.0.0.1:8093/api/activate -H "Content-Type: text/plain" --data-binary @license.txt

:: Or stop the process (Ctrl+C), save license.txt, and run run.bat again
```

Use the machine code from the PC where you will deploy. **Windows machine codes are unique to each PC.**

### License capabilities

This product exposes **liveness** APIs only. A key labelled **Liveness only** or **Recognition + Liveness** unlocks `/api/liveness`; a **Recognition only** key leaves it unavailable here.

```bat
curl -s http://127.0.0.1:8093/api/licenseStatus
```

The Gradio demo shows the same summary as **License:** at the top of the page.

## Try it

### Health

```bat
curl -s http://127.0.0.1:8093/api/health
```

### Liveness

```bat
curl -s -X POST http://127.0.0.1:8093/api/liveness -H "Content-Type: application/json" -d "{\"image\":\"<base64-jpeg>\"}"
```

Success `data`:

```json
{ "score": 0.72, "result": "Real", "pass": true }
```

Common failures (`success: false`, `data: null`):

| `message` | Meaning |
| --------- | ------- |
| `NO_FACE` | No usable face in the image |
| `Image not suitable` | Missing or undecodable image |

Full protocol: [https://doc.faceplugin.com](https://doc.faceplugin.com).

### Security

This API has **no authentication**. By default it listens on **0.0.0.0** — every interface, reachable from your network — and answers browser requests from any origin.

| Variable | Purpose |
| -------- | ------- |
| `FACESDK_BIND_HOST` | Listen address. Default `0.0.0.0`. Set it to `127.0.0.1` for this machine only. |
| `PORT` / `FACESDK_PORT` | API port. Default `8093`. |
| `LICENSE` | A license key (`FP1.…`) or a path to a license file. Default `.\license.txt`. |
| `FP_NO_LICENSE_PROMPT` | Set to `1` to skip the interactive paste prompt — for services and CI. |

Put it behind your own gateway, or bind it to localhost, before exposing it anywhere untrusted.

### Postman

Import [`postman/FaceLiveness-API.postman_collection.json`](postman/FaceLiveness-API.postman_collection.json). See [`postman/README.md`](postman/README.md) for the flow and failure messages.

Default base URL: `http://127.0.0.1:8093`. Routes are `/api/*` (`/api/check_liveness` aliases `/api/liveness`).

### Demo UI (Gradio) — local only

A local FacePlugin Face Liveness demo in the browser. The API must already be running on port 8093.

```bat
pip install -r requirements-demo.txt
run_demo.bat
```

Open **http://127.0.0.1:9093**. Sample spoof images are in `assets/examples/samples/`.

To change the ports, set them yourself instead of using `run_demo.bat` — CMD:

```bat
set DEMO_PORT=9093
set API_BASE=http://127.0.0.1:8093
python demo.py
```

PowerShell:

```powershell
$env:DEMO_PORT = "9093"
$env:API_BASE = "http://127.0.0.1:8093"
python demo.py
```

Each run shows **Score**, **Result** (`Real` or `Spoof`) and **Pass**, with the raw JSON beside it.

<p align="center">
 <img src="https://raw.githubusercontent.com/Faceplugin-ltd/faceplugin-assets/main/screenshots/face-liveness/desktop/demo-ui.png" alt="FacePlugin Face Liveness Windows demo — Real/Spoof result with score and Pass" width="900"/>
</p>

## Setup on your own app

Two ways to call the same engine. Full protocol: [https://doc.faceplugin.com](https://doc.faceplugin.com).

| Path | When to use |
| ---- | ----------- |
| **HTTP API** (`run.bat`) | Any language. Keep the API running and `POST` a base64 JPEG to it. |
| **`sdk.py`** | Python on the **same** Windows machine as `lib\cpu\`. No HTTP hop. |

**HTTP (any language)**

1. Start the API with `run.bat` and activate it once.
2. `POST /api/liveness` with `{"image":"<base64-jpeg>"}`.
3. Read `data.pass` for the verdict, and check `success` / `code` on every response.

**Python in-process**

1. Copy [`sdk.py`](sdk.py) and `lib\cpu\` into your project.
2. Put `lib\cpu` on `PATH` (that is all `run.bat` does).
3. Call `get_machine_code` → `activate` → `init_sdk`, then `liveness`.

The Gradio demo (`demo.py` / `run_demo.bat`) is a local test UI. You do not need it in production.

## About SDK

[`sdk.py`](sdk.py) is the Python binding. Every call returns `0` on success, or an error code.

**1. Get the machine code and request a license**

```python
import sdk

print(sdk.get_machine_code())   # FPMC1.…
```

**2. Activate, then initialize**

```python
ret = sdk.activate("license.txt")   # 0 on success
if ret == 0:
    ret = sdk.init_sdk()            # 0 on success

status = sdk.get_license_status()   # what the key unlocks
```

**3. Score a face**

```python
result = sdk.liveness(base64_image)   # JSON string
```

`data` is `{ "score": <float>, "result": "Real" | "Spoof", "pass": <bool> }`. Every RGB engine in the runtime is run and the scores are combined into that one verdict. Images arrive as base64 JPEG (a `data:` prefix is accepted); anything else is converted and re-encoded, and over 8 MB is downscaled.

HTTP endpoints: `/api/health`, `/api/machinecode`, `/api/licenseStatus`, `/api/backend`, `/api/activate`, `/api/liveness`, `/api/check_liveness`.

## Contact

<div align="left">
<a target="_blank" href="mailto:info@faceplugin.com"><img src="https://img.shields.io/badge/email-info@faceplugin.com-blue.svg?logo=gmail" alt="faceplugin.com"></a>&emsp;
<a target="_blank" href="https://t.me/FacePluginSupport"><img src="https://img.shields.io/badge/telegram-@FacePluginSupport-blue.svg?logo=telegram" alt="Telegram @FacePluginSupport"></a>&emsp;
<a target="_blank" href="https://wa.me/+14692784822"><img src="https://img.shields.io/badge/whatsapp-faceplugin-blue.svg?logo=whatsapp" alt="faceplugin.com"></a>
</div>
