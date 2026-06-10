from urllib.parse import quote_plus

import feedparser

from config import MAX_NOTICIAS_POR_BUSQUEDA
from formatters import acortar_texto, formatear_fecha, limpiar_html


REGIONES = {
    "Global": "",
    "Argentina": "Argentina",
    "Estados Unidos": "Estados Unidos",
    "China": "China",
    "Europa": "Europa",
}

ENFOQUES = {
    "Todo": "",
    "Tecnología": "tecnología",
}


def construir_consulta(tema, region="Global", enfoque="Todo"):
    partes = [
        ENFOQUES.get(enfoque, ""),
        tema.strip(),
        REGIONES.get(region, ""),
    ]
    return " ".join(parte for parte in partes if parte)


def buscar_noticias(tema, region="Global", enfoque="Todo"):
    noticias_encontradas = []
    consulta = construir_consulta(tema, region, enfoque)
    tema_url = quote_plus(consulta)
    url_busqueda = (
        f"https://news.google.com/rss/search?q={tema_url}"
        "&hl=es-419&gl=AR&ceid=AR:es-419"
    )
    feed = feedparser.parse(url_busqueda)

    for entrada in feed.entries:
        titulo = limpiar_html(entrada.get("title", "Sin titulo"))
        descripcion_completa = limpiar_html(
            entrada.get("summary", entrada.get("description", ""))
        )
        contenido_rss = entrada.get("content", [])
        contenido = (
            limpiar_html(contenido_rss[0].get("value", ""))
            if contenido_rss
            else descripcion_completa
        )
        fuente = entrada.get("source", {})
        nombre_fuente = (
            fuente.get("title", "Google News")
            if hasattr(fuente, "get")
            else "Google News"
        )

        noticia = {
            "titulo": titulo,
            "descripcion": acortar_texto(contenido or descripcion_completa),
            "fuente": limpiar_html(nombre_fuente),
            "fecha": formatear_fecha(entrada.get("published")),
            "url": entrada.get("link", "#"),
        }
        noticias_encontradas.append(noticia)

        if len(noticias_encontradas) >= MAX_NOTICIAS_POR_BUSQUEDA:
            return noticias_encontradas

    return noticias_encontradas
