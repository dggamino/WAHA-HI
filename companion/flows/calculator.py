# companion/flows/calculator.py
# HEREDITARIA™ OS — Estado de Cuenta: Gasto Invisible del Cuidador

import json
import os
import re
from datetime import datetime
from pathlib import Path

CATEGORY_BREAKDOWN = {
    "Salud": 0.35,
    "Vivienda": 0.30,
    "Manutención": 0.25,
    "Transporte": 0.10
}

DATA_DIR = Path("data/estados_cuenta")


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _get_next_folio():
    _ensure_data_dir()
    today_prefix = datetime.now().strftime("HER-%y%m%d")
    existing = list(DATA_DIR.glob(f"{today_prefix}-*.json"))
    seq = len(existing) + 1
    return f"{today_prefix}-{seq:03d}"


def _save_estado_cuenta(folio, data):
    _ensure_data_dir()
    filepath = DATA_DIR / f"{folio}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath


def _calculate_breakdown(total):
    return {
        cat: round(total * pct, 2)
        for cat, pct in CATEGORY_BREAKDOWN.items()
    }


def _format_currency(amount):
    return f"${amount:,.2f}"


class CalculatorFlow:
    def __init__(self):
        self.sessions = {}

    def _get_session(self, session_id):
        if session_id not in self.sessions:
            self.sessions[session_id] = {"step": "ask_meses"}
        return self.sessions[session_id]

    def _extract_number(self, text):
        if not text:
            return None
        clean = text.replace("$", "").replace(",", "").replace(" ", "")
        match = re.search(r"\d+", clean)
        return int(match.group()) if match else None

    def process(self, text, session_id=None, user_id=None):
        sid = session_id or "default"
        sess = self._get_session(sid)

        if sess["step"] == "ask_meses":
            meses = self._extract_number(text)
            if meses and meses > 0:
                sess["meses"] = meses
                sess["step"] = "ask_gasto"
                return {
                    "type": "text",
                    "content": (
                        f"✅ {meses} meses registrados.\n\n"
                        f"¿Cuál es tu gasto promedio *bimestral*?\n"
                        f"(Ejemplo: $16,090 — incluye medicamentos, despensa, luz, agua, etc.)"
                    )
                }
            else:
                return {
                    "type": "text",
                    "content": (
                        "📋 *ESTADO DE CUENTA HEREDITARIA™*\n\n"
                        "Voy a calcular tu *gasto invisible* como cuidador.\n\n"
                        "¿Cuántos meses llevas cuidando a tu familiar?"
                    )
                }

        elif sess["step"] == "ask_gasto":
            gasto = self._extract_number(text)
            if gasto and gasto > 0:
                sess["gasto_bimestral"] = gasto
                return self._generate_result(sid, sess)
            else:
                return {
                    "type": "text",
                    "content": (
                        "Por favor dime un monto numérico.\n"
                        "Ejemplo: *16090* o *$16,090*"
                    )
                }

        else:
            sess["step"] = "ask_meses"
            if "meses" in sess:
                del sess["meses"]
            if "gasto_bimestral" in sess:
                del sess["gasto_bimestral"]
            return self.process(text, sid, user_id)

    def _generate_result(self, sid, sess):
        meses = sess["meses"]
        gasto_bimestral = sess["gasto_bimestral"]
        gasto_mensual = gasto_bimestral / 2
        total_regalado = meses * gasto_mensual

        folio = _get_next_folio()
        hoy = datetime.now()
        desglose = _calculate_breakdown(total_regalado)

        estado_data = {
            "folio": folio,
            "fecha_emision": hoy.isoformat(),
            "session_id": sid,
            "meses_cuidando": meses,
            "gasto_bimestral": gasto_bimestral,
            "gasto_mensual_estimado": round(gasto_mensual, 2),
            "total_regalado": round(total_regalado, 2),
            "desglose_por_categoria": desglose,
            "porcentajes_categoria": CATEGORY_BREAKDOWN,
            "nota": "Documento de registro sistemático con fines documentales."
        }
        _save_estado_cuenta(folio, estado_data)

        del self.sessions[sid]

        cats = list(desglose.items())
        lineas = []
        for i, (cat, monto) in enumerate(cats):
            prefix = "└─" if i == len(cats) - 1 else "├─"
            lineas.append(f"{prefix} {cat}: {_format_currency(monto)}")

        return {
            "type": "text",
            "content": (
                f"📋 *ESTADO DE CUENTA HEREDITARIA™*\n"
                f"Folio: `{folio}`\n"
                f"Período: {meses} meses de cuidado\n"
                f"Fecha de emisión: {hoy.strftime('%d de %B de %Y')}\n\n"
                f"💰 *GASTO INVISIBLE CALCULADO*\n"
                f"• Meses cuidando: {meses}\n"
                f"• Gasto bimestral promedio: {_format_currency(gasto_bimestral)}\n"
                f"• Gasto mensual estimado: {_format_currency(gasto_mensual)}\n"
                f"• *TOTAL REGALADO: {_format_currency(total_regalado)}*\n\n"
                f"📊 *Desglose estimado por categoría:*\n"
                f"{chr(10).join(lineas)}\n\n"
                f"⚠️ Este documento es un registro sistemático con fines documentales.\n"
                f"Para formalizar, escribe *ASESORÍA* y te conectamos con un especialista.\n\n"
                f"🔗 *Guarda este folio:* `{folio}`"
            )
        }


_calculator_flow = None

def get_calculator_flow():
    global _calculator_flow
    if _calculator_flow is None:
        _calculator_flow = CalculatorFlow()
    return _calculator_flow


def handle(context):
    text = context.memory.get("raw_text", "") if hasattr(context, "memory") else ""
    session_id = context.session_id if hasattr(context, "session_id") else None
    user_id = context.user_id if hasattr(context, "user_id") else None
    calc = get_calculator_flow()
    return calc.process(text, session_id, user_id)
