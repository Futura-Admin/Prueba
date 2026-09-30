# CLAUDE.md

## Título de la sesión

En tu primera respuesta de cada sesión, ponte el título `[COD] Asunto @NUBE`.

- **COD** es el código del cliente del que se hable (ACU Acuabit, ALT Altai, BAS Básculas, BSC Bodega Santa Cecilia, EQU Equanum…) o **FUT** si es trabajo interno.
- **@NUBE** indica que esta sesión corre en la nube y no tiene acceso a Drive ni a los ficheros de Futura Admin.

Ponerte el título significa **renombrar la sesión**, no solo escribirlo en el texto de la respuesta:

1. Carga las herramientas con `ToolSearch` (`select:mcp__Claude_Code_Remote__get_session,mcp__Claude_Code_Remote__set_session_title`).
2. Llama a `get_session` sin `session_id` para obtener el id de esta sesión.
3. Llama a `set_session_title` con ese id y el título `[COD] Asunto @NUBE`.

Hazlo antes de responder. Si el asunto cambia de cliente más adelante, vuelve a renombrarla.
