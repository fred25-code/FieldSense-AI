
from pathlib import Path
import re

import numpy as np
from PIL import Image, ImageOps, ImageEnhance


PARAMETERS = {
    "pH": [r"\bp\s*h\b"],
    "Temperature": [r"\btemperature\b", r"\btemp\.?\b"],
    "Turbidity": [r"\bturbidity\b"],
    "Conductivity": [r"\bconductivity\b", r"\bspecific conductance\b"],
    "Dissolved Oxygen": [r"\bdissolved oxygen\b", r"\bDO\b"],
    "Total Dissolved Solids": [r"\btotal dissolved solids\b", r"\bTDS\b"],
    "Salinity": [r"\bsalinity\b"],
    "Nitrate": [r"\bnitrate\b"],
    "Phosphate": [r"\bphosphate\b"],
}

VALUE_RE = re.compile(
    r"([-+]?\d+(?:[.,]\d+)?)\s*"
    r"(mg/L|µS/cm|μS/cm|uS/cm|mS/cm|NTU|°C|degC|C|ppt|%|ppm)?",
    re.IGNORECASE,
)


class LocalOCREngine:
    """Offline OCR using local PaddleOCR 2.10 models."""

    def __init__(self, model_root=None):
        self.model_root = Path(
            model_root
            or Path(__file__).resolve().parent.parent
            / "models"
            / "paddleocr"
        )
        self.engine = None

    def _load(self):
        if self.engine is not None:
            return self.engine

        det = self.model_root / "det"
        rec = self.model_root / "rec"
        cls = self.model_root / "cls"

        required = [
            det / "inference.pdiparams",
            det / "inference.pdmodel",
            rec / "inference.pdiparams",
            rec / "inference.pdmodel",
            cls / "inference.pdiparams",
            cls / "inference.pdmodel",
        ]

        missing = [str(p) for p in required if not p.is_file()]

        if missing:
            raise RuntimeError(
                "Local OCR model files are missing:\n"
                + "\n".join(missing)
                + "\nNo network download will be attempted."
            )

        from paddleocr import PaddleOCR

        self.engine = PaddleOCR(
            lang="en",
            det_model_dir=str(det),
            rec_model_dir=str(rec),
            cls_model_dir=str(cls),
            use_angle_cls=False,
            show_log=False,
        )

        return self.engine

    @staticmethod
    def preprocess(image):
        image = ImageOps.exif_transpose(image).convert("RGB")
        image = ImageOps.autocontrast(image)
        image = ImageEnhance.Contrast(image).enhance(1.12)
        image = ImageEnhance.Sharpness(image).enhance(1.15)
        return image

    def extract(self, image):
        engine = self._load()

        if isinstance(image, (str, Path)):
            image = Image.open(image)

        arr = np.asarray(self.preprocess(image))
        result = engine.ocr(arr, cls=False)

        rows = []

        for page in result or []:
            for line in page or []:
                try:
                    text = str(line[1][0]).strip()
                    confidence = float(line[1][1])

                    if text:
                        rows.append({
                            "text": text,
                            "confidence": confidence,
                        })

                except (IndexError, TypeError, ValueError):
                    continue

        return rows


def parse_measurements(ocr_rows, review_threshold=0.85):
    """Extract labelled measurements and flag uncertain OCR readings."""

    found = []

    for row in ocr_rows:
        text = str(row.get("text", "")).strip()

        for parameter, patterns in PARAMETERS.items():
            label_match = None

            for pattern in patterns:
                label_match = re.search(pattern, text, re.IGNORECASE)
                if label_match:
                    break

            if not label_match:
                continue

            remaining = text[label_match.end():]
            value_match = VALUE_RE.search(remaining)

            if not value_match:
                break

            try:
                value = float(value_match.group(1).replace(",", "."))
            except ValueError:
                break

            confidence = row.get("confidence")

            if confidence is not None:
                try:
                    confidence = float(confidence)
                except (TypeError, ValueError):
                    confidence = None

            found.append({
                "parameter": parameter,
                "value": value,
                "unit": value_match.group(2) or "",
                "original_text": text,
                "confidence": confidence,
                "requires_review": (
                    confidence is None
                    or confidence < review_threshold
                ),
            })

            break

    return found
