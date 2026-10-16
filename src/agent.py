from src.llm_client import consultar_llm


def agente_analista(contexto_datos, pregunta_usuario):
    """Agente inteligente que razona respuestas usando el contexto del dataset."""
    prompt_estructurado = f"""
    Eres un Agente Experto en Ciencia de Datos de nivel universitario.
    A continuación tienes un resumen del dataset que estamos analizando:
    ---
    {contexto_datos}
    ---
    El usuario te hace la siguiente consulta sobre estos datos: "{pregunta_usuario}"
    
    Por favor responde de forma clara, técnica, breve y en español.
    """
    return consultar_llm(prompt_estructurado)