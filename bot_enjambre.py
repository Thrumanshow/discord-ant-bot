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
    embed.add_field(name="Firma LBH", value=f"`{feromona['lbh_sig']}`", inline=True)
    embed.add_field(name="Estado", value="🟢 Óptimo", inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="node", description="Muestra la telemetría del borde")
async def node(interaction: discord.Interaction):
    telemetry = generar_feromona("edge_heartbeat", "node_ant_01", "healthy", {"cpu_load": "1.2%", "memory": "256MB/3.8GB"})
    await interaction.response.send_message(f"📡 **[Telemetría Edge]**\n```json\n{telemetry}\n```")

@bot.tree.command(name="verify", description="Valida la integridad de un paquete de datos LBH")
@app_commands.describe(origin="Origen del nodo", sig="Firma LBH hash")
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

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: TOKEN no configurado.")
