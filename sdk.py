"""ctypes bindings to FaceLivenessSDK.dll (Face Liveness, Windows).

Native call flow matches `_dropped/Face-Recognition-LivenessDetection-Windows`
liveness path: FaceSDK_liveness_all(jpeg_bytes, len, out) → JSON string.
"""

from __future__ import annotations

import base64
import ctypes
import io
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "lib" / "cpu"
DLL = LIB / "FaceLivenessSDK.dll"

os.chdir(ROOT)

if not DLL.is_file():
    print(
        f"ERROR: missing {DLL.relative_to(ROOT)}\n"
        "Download the Windows runtime into .\\lib\\cpu\\.",
        file=sys.stderr,
    )
    raise SystemExit(1)

# idliveface/OpenVINO can AV on a cold LoadLibrary; keep OpenMP modest and cache local.
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OV_CACHE_DIR", str(Path(os.environ.get("TEMP", ROOT)) / "faceplugin-ov-cache"))
os.environ["PATH"] = str(LIB) + os.pathsep + os.environ.get("PATH", "")
if hasattr(os, "add_dll_directory"):
    os.add_dll_directory(str(LIB))

_dll = ctypes.WinDLL(str(DLL))

_dll.FaceSDK_initSDK.restype = ctypes.c_int
_dll.FaceSDK_initSDK.argtypes = []
_dll.FaceSDK_activate.restype = ctypes.c_int
_dll.FaceSDK_activate.argtypes = [ctypes.c_char_p]
_dll.FaceSDK_getMachineCode.restype = ctypes.c_int
_dll.FaceSDK_getMachineCode.argtypes = [ctypes.c_char_p]
_dll.FaceSDK_liveness_all.restype = ctypes.c_int
_dll.FaceSDK_liveness_all.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p]


def _opt_sym(name, restype, argtypes):
    fn = getattr(_dll, name, None)
    if fn is None:
        return None
    fn.restype = restype
    fn.argtypes = argtypes
    return fn


_get_license_status = _opt_sym(
    "FaceSDK_getLicenseStatus", ctypes.c_int, [ctypes.c_char_p]
)

_MC_BUF = 768
_STATUS_BUF = 512
_OUT = 2 * 1024 * 1024
_MAX_IMG = 8 * 1024 * 1024


def _b(v) -> bytes:
    if v is None:
        raise ValueError("required")
    if isinstance(v, bytes):
        return v
    return str(v).encode("utf-8")


def _jpeg_bytes(image_b64: str) -> bytes:
    if image_b64 is None or not str(image_b64).strip():
        raise ValueError("Image not suitable")
    try:
        text = str(image_b64).strip()
        if text.startswith("data:") and "base64," in text:
            text = text.split("base64,", 1)[1]
        data = base64.b64decode(text, validate=False)
        if not data:
            raise ValueError("Image not suitable")
        if len(data) <= _MAX_IMG and data[:2] == b"\xff\xd8":
            return data
        from PIL import Image

        img = Image.open(io.BytesIO(data))
        img.load()
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=90)
        out = buf.getvalue()
        while len(out) > _MAX_IMG and img.width > 32:
            img = img.resize((max(1, int(img.width * 0.75)), max(1, int(img.height * 0.75))))
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=80)
            out = buf.getvalue()
        return out
    except ValueError as ex:
        if str(ex).strip() == "Image not suitable":
            raise
        raise ValueError("Image not suitable") from ex
    except Exception as ex:  # noqa: BLE001
        raise ValueError("Image not suitable") from ex


def backend() -> str:
    return "cpu"


def get_machine_code() -> str:
    buf = ctypes.create_string_buffer(_MC_BUF)
    _dll.FaceSDK_getMachineCode(buf)
    return buf.value.decode("utf-8", errors="replace")


def get_license_status() -> dict:
    fallback = {
        "licensed": False,
        "level": -1,
        "levelName": "None",
        "recognition": False,
        "liveness": False,
        "label": "Not licensed",
    }
    if _get_license_status is None:
        return fallback
    buf = ctypes.create_string_buffer(_STATUS_BUF)
    if int(_get_license_status(buf)) != 0:
        return fallback
    try:
        data = json.loads(buf.value.decode("utf-8", errors="replace") or "{}")
        return data if isinstance(data, dict) else fallback
    except Exception:  # noqa: BLE001
        return fallback


def activate(license_path: str) -> int:
    return int(_dll.FaceSDK_activate(_b(license_path)))


def init_sdk() -> int:
    return int(_dll.FaceSDK_initSDK())


def liveness(image: str) -> str:
    jpeg = _jpeg_bytes(image)
    out = ctypes.create_string_buffer(_OUT)
    _dll.FaceSDK_liveness_all(jpeg, len(jpeg), out)
    return out.value.decode("utf-8", errors="replace")
