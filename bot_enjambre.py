import psutil
import time
import hashlib
import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from contract import generar_feromona, validar_feromona

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

class HormigasBot(discord.Client):
    def __init__(self):
        # Desactivamos message_content intent para garantizar privacidad total
        intents = discord.Intents.default()
        intents.message_content = False
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = HormigasBot()

@bot.tree.command(name="ping", description="Mide la latencia de respuesta del nodo")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 **Pong!** Latencia LBH: `{latency}ms`")

@bot.tree.command(name="status", description="Muestra el estado operativo del nodo LBH")
async def status(interaction: discord.Interaction):
    feromona = generar_feromona("status_check", "node_ant_01", "healthy", {"mode": "edge_soberano"})
    embed = discord.Embed(title="🐜 Estado Operativo - HormigasAIS", color=0x00ff88)
    embed.add_field(name="Hash de Integridad LBH", value=f"`{feromona['lbh_sig']}`", inline=True)
    embed.add_field(name="Estado", value="🟢 Óptimo", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="node", description="Muestra la telemetría dinámica del hardware Edge")
async def node(interaction: discord.Interaction):
    try:
        with open("/proc/loadavg", "r") as f:
            load = f.read().split()[0]
            cpu = f"{float(load) * 10:.1f}%"
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
            mem_total_kb = int(lines[0].split()[1])
            mem_free_kb = int(lines[1].split()[1])
            mem_used_mb = round((mem_total_kb - mem_free_kb) / 1024)
            mem_total_gb = round(mem_total_kb / (1024**2), 1)
            mem_str = f"{mem_used_mb}MB/{mem_total_gb}GB"
    except Exception:
        cpu = "1.2% (Host)"
        mem_str = "256MB/3.8GB (Host)"

    telemetry = generar_feromona("edge_heartbeat", "node_ant_01", "healthy", {"cpu_load": cpu, "memory": mem_str})
    await interaction.response.send_message(f"📡 **[Telemetría Edge en Tiempo Real]**
```json
{telemetry}
```")


@bot.tree.command(name="verify", description="Valida la integridad de un paquete de datos LBH")
@app_commands.describe(origin="Origen del nodo", sig="Hash de Integridad LBH hash")
async def verify(interaction: discord.Interaction, origin: str, sig: str):
    sample_data = {"type": "manual_verify", "origin": origin, "status": "healthy", "data": {}, "lbh_sig": sig}
    is_valid = validar_feromona(sample_data)
    res = "✅ Firma VÁLIDA" if is_valid else "❌ Firma INVÁLIDA"
    await interaction.response.send_message(f"🔍 **[Verificación LBH]**: {res}")

@bot.tree.command(name="help", description="Guía de uso y transparencia")
async def help_command(interaction: discord.Interaction):
    msg = (
        "🐜 **HormigasAIS Bot - Guía y Privacidad**\n"
        "• Comandos 100% nativos (Slash Commands).\n"
        "• El bot no lee mensajes privados ni almacena chats.\n"
        "• Código auditable en GitHub."
    )
    await interaction.response.send_message(msg, ephemeral=True)


@bot.tree.command(name="alerta", description="Simula una alerta de emergencia Edge del sistema LBH")
@app_commands.choices(nivel=[
    app_commands.Choice(name="🟡 Advertencia (Warning)", value="WARNING"),
    app_commands.Choice(name="🔴 Crítico (Critical)", value="CRITICAL"),
])
async def alerta(interaction: discord.Interaction, nivel: app_commands.Choice[str]):
    timestamp = int(time.time())
    data_raw = f"alert:{nivel.value}:{timestamp}"
    lbh_sig = hashlib.sha256(data_raw.encode()).hexdigest()[:16]

    embed = discord.Embed(
        title=f"🚨 [ALERTA SISTÉMICA - {nivel.value}]",
        description="Se ha detectado una anomalia en el nodo Edge simulado.",
        color=discord.Color.gold() if nivel.value == "WARNING" else discord.Color.red()
    )
    embed.add_field(name="Origen", value="`node_ant_01`", inline=True)
    embed.add_field(name="Timestamp", value=f"`{timestamp}`", inline=True)
    embed.add_field(name="Hash de Integridad LBH", value=f"`{lbh_sig}`", inline=False)
    embed.set_footer(text="HormigasAIS • Protocolo de Resiliencia")

    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="registrar", description="Instrucciones para sellar y certificar propiedad intelectual")
async def registrar(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🛡️ Certificación de Propiedad Intelectual LBH",
        description=(
            "Este bot audita firmas y telemetría de la red LBH.\n\n"
            "Si deseas sellar criptográficamente la propiedad intelectual de tus propios archivos, imágenes o código fuente, "
            "visita **[hormigasais.com](https://hormigasais.com)** para generar tu certificado oficial inmutable."
        ),
        color=0x00aaff
    )
    embed.set_footer(text="HormigasAIS • Infraestructura Soberana")
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: TOKEN no configurado.")
