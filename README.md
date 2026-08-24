# La Hormiga — Discord Ant Bot

> Bot ligero para Discord orientado al diagnóstico, la telemetría del host y la validación de integridad de datos mediante el formato LBH dentro del ecosistema HormigasAIS.

[![Landing Page](https://img.shields.io/badge/Landing%20Page-GitHub%20Pages-blue)](https://thrumanshow.github.io/discord-ant-bot/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Discord Permissions](https://img.shields.io/badge/Permissions-19456%20%7C%20Minimal-green)](https://docs.discord.com/developers/topics/permissions)

## Descripción

**La Hormiga** es un bot de Discord desarrollado en Python con `discord.py`. Utiliza comandos slash para mostrar latencia, estado operativo, telemetría del host donde se ejecuta, validación de hashes de integridad LBH y simulaciones de eventos.

El proyecto se encuentra en estado **MVP/experimental**. Las métricas mostradas por `/node` corresponden al host que ejecuta el proceso y no representan necesariamente el estado de toda una red distribuida.

Para servicios de certificación de activos digitales, sellado C2PA o custodia de archivos, consulta la plataforma principal en [hormigasais.com](https://hormigasais.com).

## Privacidad y permisos

El bot utiliza `message_content=False`, por lo que no necesita leer el contenido general de los mensajes de los canales. Su interacción principal se realiza mediante comandos slash. Discord puede enviar al bot los metadatos necesarios para procesar una interacción, como el servidor, el canal y el usuario que ejecuta el comando; el proyecto no implementa almacenamiento de conversaciones.

El enlace de instalación utiliza los scopes `bot` y `applications.commands` y el bitfield de permisos `19456`, que corresponde a:

| Permiso | Función |
|---|---|
| `VIEW_CHANNEL` | Ver los canales en los que el rol del bot tenga acceso. |
| `SEND_MESSAGES` | Responder a los comandos ejecutados. |
| `EMBED_LINKS` | Enviar respuestas enriquecidas mediante embeds. |

El bot no solicita `ADMINISTRATOR`, lectura del historial, gestión de canales, gestión de roles, moderación, expulsiones, baneos ni webhooks.

## Comandos slash

| Comando | Categoría | Descripción |
|---|---|---|
| `/ping` | Diagnóstico | Muestra la latencia aproximada del cliente conectado a Discord. |
| `/status` | Estado | Muestra el estado operativo y el hash de integridad de una trama LBH generada por el bot. |
| `/node` | Telemetría | Muestra métricas del host donde se ejecuta el bot, utilizando `/proc` cuando está disponible. |
| `/verify` | Validación | Comprueba el hash de integridad de una estructura LBH predefinida a partir del origen y el hash recibidos. |
| `/help` | Guía | Muestra instrucciones básicas y notas de privacidad. |
| `/alerta` | Simulación | Emite una alerta simulada para pruebas de respuesta en el servidor. |
| `/registrar` | Ecosistema | Muestra información y un enlace hacia la plataforma HormigasAIS. |

> El hash LBH es una huella de integridad basada en SHA-256 truncada a 16 caracteres. No debe interpretarse como una firma digital autenticada ni como un certificado de propiedad.

## Requisitos

Se requiere Python 3.10 o superior, una aplicación creada en [Discord Developer Portal](https://discord.com/developers/applications) y un entorno compatible con el acceso a `/proc` si se desea obtener telemetría dinámica del sistema. En otros entornos, el bot utiliza valores de reserva cuando las métricas no están disponibles.

## Instalación local

```bash
git clone [https://github.com/Thrumanshow/discord-ant-bot.git](https://github.com/Thrumanshow/discord-ant-bot.git)
cd discord-ant-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` y establece el token de tu aplicación:

```env
DISCORD_TOKEN=pega_aqui_el_token_real
```

Inicia el bot con:

```bash
python bot_enjambre.py
```

No publiques el archivo `.env`, el token del bot ni ningún secreto en el repositorio. El archivo `.gitignore` del proyecto excluye `.env`, entornos virtuales, cachés de Python y archivos de log.

## Añadir el bot a un servidor

Utiliza la [Landing Page oficial](https://thrumanshow.github.io/discord-ant-bot/) y revisa cuidadosamente los permisos mostrados por Discord antes de confirmar. La persona que realiza la instalación debe tener permisos suficientes para añadir aplicaciones al servidor.

Después de iniciar el proceso, espera a que Discord sincronice los comandos slash. Si no aparecen inmediatamente, comprueba que el bot esté conectado y vuelve a abrir Discord o espera unos instantes antes de probar `/help`.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `bot_enjambre.py` | Cliente de Discord y definición de los comandos slash. |
| `contract.py` | Generación y validación de hashes de integridad LBH. |
| `index.html` | Landing Page principal. |
| `docs/index.html` | Copia utilizada para publicar la Landing Page mediante GitHub Pages. |
| `logo.png` | Recurso visual del proyecto. |
| `.env.example` | Plantilla segura para la variable de entorno del token. |
| `LICENSE` | Licencia MIT. |

## Limitaciones conocidas

El comando `/node` mide el host donde corre el proceso; no consulta automáticamente una infraestructura remota. El comando `/alerta` es una simulación y no representa un incidente real. El comando `/verify` valida una estructura LBH concreta y no sustituye una firma digital basada en claves criptográficas.

Antes de utilizar el proyecto en producción se recomienda añadir pruebas automatizadas, fijar versiones de dependencias, publicar una política de privacidad completa, definir un sistema de versionado y verificar cada comando en un servidor de pruebas.

## Licencia

Este proyecto se distribuye bajo la [licencia MIT](LICENSE).

## Enlaces

- [Landing Page](https://thrumanshow.github.io/discord-ant-bot/)
- [Repositorio en GitHub](https://github.com/Thrumanshow/discord-ant-bot)
- [HormigasAIS](https://hormigasais.com)
- [Documentación de permisos de Discord](https://docs.discord.com/developers/topics/permissions)
