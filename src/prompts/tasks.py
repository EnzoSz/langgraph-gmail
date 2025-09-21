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

EMAIL_WRITER_TASK = """
Instrucciones:
    1. Analiza el contenido del correo electrónico original y su categoría
    2. Si la categoría es product_enquiry o customer_complaint, usa la herramienta de recuperación para consultar 
    la base de datos vectorial en busca de información que pueda ser relevante y agrégala a tu contexto para 
    escribir el mejor correo electrónico posible. Si la categoría es diferente NO uses la herramienta de recuperación.
    3. Crea un asunto claro y profesional que refleje el contenido de la respuesta
    4. Escribe un cuerpo de correo electrónico integral que:
       - Reconozca la consulta del cliente
       - Proporcione información específica y precisa
       - Aborde cualquier preocupación o pregunta planteada
       - Ofrezca próximos pasos o soporte adicional si es necesario
       - Mantenga un tono útil y profesional
    5. Usa la siguiente estructura para crear el correo electrónico:
        - id: El ID del correo electrónico
        - subject: Asunto del correo electrónico, comienza con Re:
        - sender: Dirección de correo electrónico del remitente (en este caso, enzosoliz95@gmail.com, asegúrate de usar 
        Cellfone SA <enzosoliz95@gmail.com>)
        - date: Fecha cuando se envió el correo electrónico
        - body: Contenido del cuerpo del correo electrónico

Pautas:
    - No uses tu propio conocimiento si no estás seguro sobre información del producto,
    en su lugar, confía en la herramienta de recuperación para consultar la base de datos, por ejemplo, si la pregunta
    es sobre un iPhone, usa la herramienta y consulta la base de datos para buscar información confiable.
    - Si hay contexto adicional recuperado de la base de conocimientos, úsalo para escribir el mejor
    correo electrónico posible.
    - Sé conciso pero completo
    - Usa lenguaje claro y profesional
    - Evita jerga técnica a menos que sea necesario
    - Muestra empatía y comprensión
    - Proporciona información accionable
    - Si no tienes información específica, reconoce la limitación y ofrece conectarlos
    con el equipo correcto
    - Finalmente, no uses ningún nombre personal ni número de teléfono al final del correo electrónico, para el nombre de
    la empresa usa "Cellfone SA".
    - Asegúrate de escribir el correo electrónico en español, no en inglés.

Categoría del Correo Original: {email_category}
Contenido del Correo Original: {email_content}
Contexto adicional: {context}
"""