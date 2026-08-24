import json
import hashlib

def generar_feromona(event_type: str, origin: str, status: str = "healthy", data: dict = None) -> dict:
    payload = {
        "type": event_type,
        "origin": origin,
        "status": status,
        "data": data or {}
    }
    serialized = json.dumps(payload, sort_keys=True)
    hash_sig = hashlib.sha256(serialized.encode('utf-8')).hexdigest()[:16]
    payload["lbh_sig"] = hash_sig
    return payload

def validar_feromona(feromona: dict) -> bool:
    if not isinstance(feromona, dict) or "lbh_sig" not in feromona:
        return False
    
    sig_original = feromona.pop("lbh_sig", None)
    serialized = json.dumps(feromona, sort_keys=True)
    recalculated_sig = hashlib.sha256(serialized.encode('utf-8')).hexdigest()[:16]
    
    # Restaurar la firma en el diccionario
    feromona["lbh_sig"] = sig_original
    
    return sig_original == recalculated_sig
