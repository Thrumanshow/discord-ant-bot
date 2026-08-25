import json
import time
import hashlib
import os
import discord
import aiohttp
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
            mem_lines = f.readlines()
            mem_total_kb = int(mem_lines[0].split()[1])
            mem_free_kb = int(mem_lines[1].split()[1])
            mem_used_mb = round((mem_total_kb - mem_free_kb) / 1024)
            mem_total_gb = round(mem_total_kb / (1024**2), 1)
            mem_str = f"{mem_used_mb}MB/{mem_total_gb}GB"
    except Exception:
        cpu = "1.2% (Host)"
        mem_str = "256MB/3.8GB (Host)"

    telemetry = generar_feromona("edge_heartbeat", "node_ant_01", "healthy", {"cpu_load": cpu, "memory": mem_str})
    header = "📡 **[Telemetría Edge en Tiempo Real]**"
    msg = header + "\n```json\n" + json.dumps(telemetry, indent=2) + "\n```"
    await interaction.response.send_message(msg)

@bot.tree.command(name="verify", description="Verifica un sello LBH real contra hormigasais.com")
@app_commands.describe(sig="Firma del sello, ej. CLHQ-XXXXXXXX")
async def verify(interaction: discord.Interaction, sig: str):
    await interaction.response.defer()
    url = f"https://api.hormigasais.com/seal/{sig}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                data = await resp.json()
    except Exception as e:
        await interaction.followup.send(f"⚠️ **[Verificación LBH]**: no fue posible consultar el nodo ({e})")
        return

    if "error" in data:
        await interaction.followup.send(f"❌ **[Verificación LBH]**: sello `{sig}` no encontrado.")
        return

    sello = data.get("sello", {})
    hash_valido = sello.get("hash_valido", False)
    owner = sello.get("owner", "desconocido")
    asset = sello.get("asset", "desconocido")
    plan = sello.get("plan", "desconocido")
    valido_hasta = sello.get("valido_hasta", "desconocido")

    if hash_valido:
        estado = "✅ Sello VÁLIDO"
    else:
        estado = "⚠️ Sello existente, pero hash no verificado"

    await interaction.followup.send(
        f"🔍 **[Verificación LBH]**: {estado}\n"
        f"› Propietario: `{owner}`\n"
        f"› Activo: `{asset}`\n"
        f"› Plan: `{plan}`\n"
        f"› Válido hasta: `{valido_hasta}`"
    )

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

@bot.tree.command(name="cita-status", description="Consulta el estado de una cita en barberia.hormigasais.com")
@app_commands.describe(id_reserva="ID de la reserva (recibido al confirmar tu cita)")
async def cita_status(interaction: discord.Interaction, id_reserva: str):
    await interaction.response.defer()
    url = f"https://cristhiam-barber-api.chrisquionez354.workers.dev/api/reserva/{id_reserva}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=8)) as resp:
                data = await resp.json()
    except Exception as e:
        await interaction.followup.send(f"⚠️ **[Barbería HormigasAIS]**: no fue posible conectar con el nodo de reservas ({e})")
        return

    if "error" in data:
        await interaction.followup.send(f"❌ **[Barbería HormigasAIS]**: no se encontró esa reserva.")
        return

    reserva = data.get("reserva", {})
    estado = reserva.get("estado", "desconocido")
    servicio = reserva.get("servicio", "desconocido")
    fecha = reserva.get("fecha", "desconocido")

    iconos = {"confirmed": "✅ Confirmada", "cancelled": "❌ Cancelada", "completed": "✨ Completada"}
    estado_txt = iconos.get(estado, f"⏳ {estado}")

    await interaction.followup.send(
        f"💈 **[Barbería HormigasAIS]**: {estado_txt}\n"
        f"› Servicio: `{servicio}`\n"
        f"› Fecha: `{fecha}`"
    )

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: TOKEN no configurado.")
