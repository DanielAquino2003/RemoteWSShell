# RemoteWSShell

Terminal web experimental construida con FastAPI, WebSocket, PTY y xterm.js. Permite
usar una shell interactiva desde el navegador, incluyendo aplicaciones TUI como
Codex, `top` o editores de terminal.

> [!CAUTION]
> Esta aplicación entrega una shell real con los permisos del usuario que ejecuta
> el servidor. No incluye autenticación propia y **no debe publicarse directamente
> en Internet ni exponerse mediante port forwarding**. Úsala únicamente en una red
> privada de confianza, preferiblemente mediante Tailscale Serve.

## Requisitos

- Linux
- Python 3.10 o posterior
- Bash
- Una red privada como Tailscale para acceso remoto

## Instalación

```bash
git clone git@github.com:DanielAquino2003/RemoteWSShell.git
cd RemoteWSShell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uso local

El servidor debe escuchar solamente en la interfaz local:

```bash
uvicorn server:app --host 127.0.0.1 --port 8000
```

Abre <http://127.0.0.1:8000> en el navegador. Dentro de la terminal puedes
comprobar la configuración con:

```bash
echo "$TERM"
stty size
```

`TERM` debería ser `xterm-256color`, y `stty size` debería mostrar dimensiones
distintas de `0 0`.

## Acceso privado desde el móvil

Instala Tailscale tanto en el ordenador como en el móvil. Con el servidor
escuchando en `127.0.0.1:8000`, publícalo únicamente dentro de tu tailnet:

```bash
tailscale serve --bg http://127.0.0.1:8000
```

Abre desde el móvil la URL privada HTTPS que muestra Tailscale. No uses
`tailscale funnel`: Funnel haría accesible el servicio desde Internet.

Para conservar el trabajo aunque se cierre el navegador, inicia Codex dentro de
`tmux`:

```bash
tmux new -A -s codex
codex
```

## Seguridad

- No ejecutes el servidor como `root`.
- No abras el puerto 8000 en el router.
- No uses `--host 0.0.0.0` salvo dentro de un entorno aislado y protegido.
- Restringe en Tailscale qué usuarios y dispositivos pueden acceder al equipo.
- Ejecuta la shell con un usuario sin `sudo` y sin acceso a secretos innecesarios.
- Considera este proyecto experimental; antes de cualquier exposición pública
  necesita autenticación, validación de origen, límites de sesión, rate limiting,
  timeouts y limpieza segura de los procesos PTY.

## Estructura

- `server.py`: servidor HTTP y puente WebSocket.
- `pty_manager.py`: creación, lectura, escritura y redimensionado del PTY.
- `index.html`: interfaz xterm.js adaptable al tamaño del navegador.
