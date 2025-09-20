EMAIL_CATEGORIZER_TASK = """
Instrucciones:
    1. Revisa detenidamente el contenido del email proporcionado.
    2. Usa las siguientes reglas para asignar la categoría correcta:
      - **consulta_producto**: Cuando el email busca información sobre una característica, beneficio, servicio o precio de un producto.
      - **queja_cliente**: Cuando el email comunica insatisfacción o una queja.
      - **comentario_cliente**: Cuando el email proporciona comentarios o sugerencias sobre un producto o servicio.
      - **no_relacionado**: Cuando el contenido del email no coincide con ninguna de las categorías anteriores.
CONTENIDO DEL EMAIL:
{email}

Notas:
    Basa tu categorización estrictamente en el contenido del email proporcionado; evita hacer suposiciones o generalizar en exceso.
"""
