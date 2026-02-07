# Requisitos de connection client (connection_client.py)

## Contrato
Exponer un único método `request()` para todas las llamadas remotas.

## Comportamiento obligatorio
- timeouts por request: connect + read.
- retries acotados solo para:
  - HTTP 429,
  - HTTP 5xx,
  - timeout/network.
- backoff exponencial con jitter.
- máximo `MAX_RETRIES`.

## Validación de respuesta
- verificar status esperado por step,
- parsear JSON cuando aplique,
- validar campos mínimos (ej. `id` en create),
- si status es “ok” pero falta contrato mínimo => `invalid_response_schema`.

## Seguridad
- nunca loggear token/header sensible,
- logs técnicos solo con metadatos necesarios.
