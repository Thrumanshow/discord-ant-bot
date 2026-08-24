import time
import json
import hashlib

class LBHBotContract:
    @staticmethod
    def emitir_feromona(origen: str, tipo_pulso: str, contenido: dict) -> str:
        payload = {
            "timestamp": time.time(),
            "origin": origen,
            "type": tipo_pulso,
            "data": contenido,
            "mode": "edge_termux"
        }
        # Trama LBH simplificada con hash de integridad
        raw_json = json.dumps(payload, sort_keys=True)
        sig = hashlib.sha256(raw_json.encode('utf-8')).hexdigest()[:12]
        payload["lbh_sig"] = sig
        return json.dumps(payload)

    @staticmethod
    def validar_feromona(raw_str: str) -> dict:
        data = json.loads(raw_str)
        if "lbh_sig" in data and "origin" in data:
            return data
        raise ValueError("Trama LBH inválida o no firmada")
