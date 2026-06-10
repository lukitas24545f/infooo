from email.utils import parsedate_to_datetime

from bs4 import BeautifulSoup


def limpiar_html(texto):
    """Quita las etiquetas HTML y devuelve texto legible."""
    if not texto:
        return ""

    return BeautifulSoup(texto, "html.parser").get_text(" ", strip=True)


def acortar_texto(texto, limite=250):
    """Acorta un texto largo para mostrarlo en una tarjeta."""
    if len(texto) <= limite:
        return texto

    return texto[:limite].rsplit(" ", 1)[0] + "..."


def formatear_fecha(fecha):
    """Convierte una fecha RSS a un formato fácil de leer."""
    if not fecha:
        return "Fecha desconocida"

    try:
        fecha_convertida = parsedate_to_datetime(fecha)
        return fecha_convertida.strftime("%d/%m/%Y %H:%M")
    except (TypeError, ValueError, OverflowError):
        return fecha
