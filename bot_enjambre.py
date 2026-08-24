import discord
import asyncio
import json
import os
from contract import LBHBotContract

# --- Hormiga 2: Procesadora LBH (Lógica interna) ---
class HormigaProcesadora:
    def procesar(self, raw_feromona: str) -> str:
        feromona = LBHBotContract.validar_feromona(raw_feromona)
        cmd = feromona["data"].get("command", "").lower()
        
        if cmd == "ping":
            return "🐜 **[LBH-Edge]** Pong! Trama procesada en 0.02ms desde Termux."
        elif cmd == "estado":
            return "🐜 **[Enjambre]** Nodos activos: Centinela (OK), Procesadora (OK), Estado (OK)."
        elif cmd == "ayuda":
            return "🐜 **[HormigasAIS Bot]** Comandos: `!hormiga ping`, `!hormiga estado`, `!hormiga feromona`"
        elif cmd == "feromona":
            return f"📡 **[Feromona LBH Ultima]** `{feromona['lbh_sig']}` | Origen: `{feromona['origin']}`"
        else:
            return f"⚠️ Comando `{cmd}` no reconocido por la colonia LBH."

# --- Hormiga 3: Estado y Sincronización ---
class HormigaEstado:
    def __init__(self):
        self.log_path = "colonia_events.log"

    def registrar_evento(self, raw_feromona: str):
        with open(self.log_path, "a") as f:
            f.write(raw_feromona + "\n")

# Instancias de las hormigas de soporte
procesadora = HormigaProcesadora()
estado = HormigaEstado()

# --- Hormiga 1: Centinela (Discord Gateway) ---
class HormigaCentinela(discord.Client):
    async def on_ready(self):
        print(f"🐜 [Hormiga Centinela] Conectada a Discord como {self.user}")
        print("🐜 [Enjambre HormigasAIS] Operando en el Borde desde Termux (Baja energía)")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!hormiga"):
            partes = message.content.split(" ", 1)
            comando = partes[1] if len(partes) > 1 else "ayuda"

            # 1. Centinela emite feromona
            feromona_raw = LBHBotContract.emitir_feromona(
                origen=f"discord_usr_{message.author.id}",
                tipo_pulso="command_pulse",
                contenido={"command": comando, "channel": message.channel.id}
            )

            # 2. Hormiga de Estado registra el pulso
            estado.registrar_evento(feromona_raw)

            # 3. Hormiga Procesadora ejecuta respuesta
            respuesta = procesadora.procesar(feromona_raw)

            # 4. Centinela responde en Discord
            await message.channel.send(respuesta)

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True
    client = HormigaCentinela(intents=intents)
    
    # Colocar aquí tu Token de Bot de Discord o leerlo de variable de entorno
    TOKEN = os.getenv("DISCORD_TOKEN", "TU_DISCORD_TOKEN_AQUI")
    
    if TOKEN == "TU_DISCORD_TOKEN_AQUI":
        print("⚠️ Reemplaza 'TU_DISCORD_TOKEN_AQUI' con tu token real de Discord.")
    else:
        client.run(TOKEN)
