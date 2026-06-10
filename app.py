from html import escape

import streamlit as st

from rss_service import buscar_noticias

st.set_page_config(
    page_title="InfoRadar",
    page_icon=":material/radar:",
    layout="wide",
    initial_sidebar_state="collapsed",
)


REGIONES = ["Global", "Argentina", "Estados Unidos", "China", "Europa"]
CATEGORIAS = ["Todo", "Tecnología", "Deportes", "Economía", "Fútbol", "Básquet"]


def cargar_estilos():
    st.markdown(
        """
        <style>
        :root {
            --fondo: #07110f;
            --panel: rgba(17, 34, 30, 0.86);
            --borde: rgba(154, 255, 207, 0.14);
            --texto: #f1f7f4;
            --suave: #9aada7;
            --acento: #67f0ae;
            --acento-oscuro: #123d2d;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 0%, rgba(38, 139, 95, .22), transparent 30rem),
                radial-gradient(circle at 100% 35%, rgba(31, 104, 110, .16), transparent 34rem),
                var(--fondo);
            color: var(--texto);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stDecoration"] {
            display: none;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1180px;
            padding-top: 4rem;
            padding-bottom: 5rem;
        }

        .marca {
            display: inline-flex;
            align-items: center;
            gap: .65rem;
            color: var(--acento);
            font-size: .82rem;
            font-weight: 800;
            letter-spacing: .18em;
            text-transform: uppercase;
        }

        .pulso {
            width: .65rem;
            height: .65rem;
            border-radius: 50%;
            background: var(--acento);
            box-shadow: 0 0 0 .4rem rgba(103, 240, 174, .12);
        }

        .hero {
            max-width: 820px;
            padding: 1.5rem 0 2rem;
        }

        .hero h1 {
            margin: 0 0 1rem;
            color: var(--texto);
            font-size: clamp(3.2rem, 8vw, 6.8rem);
            line-height: .94;
            letter-spacing: -.07em;
        }

        .hero h1 span {
            color: var(--acento);
        }

        .hero p {
            max-width: 620px;
            margin: 0;
            color: var(--suave);
            font-size: 1.15rem;
            line-height: 1.7;
        }

        [data-testid="stForm"] {
            padding: 0;
            border: none;
            border-radius: 0;
            background: transparent;
            box-shadow: none;
        }

        [data-testid="stTextInput"] label {
            display: none;
        }

        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextInput"] [data-baseweb="base-input"] {
            border-color: var(--borde);
            background-color: transparent;
            align-items: center;
        }

        [data-testid="stTextInput"] input {
            min-height: 4.0rem;
            box-sizing: border-box;
            padding: .9rem 1rem;
            border: 1px solid var(--borde);
            border-radius: .8rem;
            background-color: transparent;
            color: var(--texto);
            font-size: 1rem;
            line-height: 1.4;
        }

        [data-testid="InputInstructions"] {
            display: none;
        }

        [data-testid="stTextInput"] input:-webkit-autofill,
        [data-testid="stTextInput"] input:-webkit-autofill:hover,
        [data-testid="stTextInput"] input:-webkit-autofill:focus {
            -webkit-text-fill-color: var(--texto);
            -webkit-box-shadow: 0 0 0 1000px var(--fondo) inset;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: var(--acento);
            box-shadow: 0 0 0 .2rem rgba(103, 240, 174, .1);
        }

        [data-testid="stSelectbox"] label {
            color: var(--suave);
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        [data-testid="stSelectbox"] > div > div {
            border-color: rgba(255, 255, 255, .08);
            background: rgba(255, 255, 255, .04);
        }

        [data-testid="stTabs"] [role="tablist"] {
            gap: .75rem;
            margin: 1rem 0 2rem;
        }

        [data-testid="stTabs"] [role="tab"] {
            height: auto;
            padding: .75rem 1.2rem;
            border: 1px solid var(--borde);
            border-radius: 99rem;
            color: var(--suave);
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            background: var(--acento-oscuro);
            color: var(--acento);
        }

        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            display: none;
        }

        .stButton button, [data-testid="stFormSubmitButton"] button {
            min-height: 3.4rem;
            border: 1px solid var(--borde);
            border-radius: .8rem;
            background: var(--acento);
            color: #062016;
            font-weight: 800;
        }

        .stButton button:hover, [data-testid="stFormSubmitButton"] button:hover {
            border-color: #a7ffd2;
            background: #a7ffd2;
            color: #062016;
        }

        .temas-label {
            margin: 1.4rem 0 .35rem;
            color: var(--suave);
            font-size: .78rem;
            font-weight: 700;
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .resultados-cabecera {
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 1rem;
            margin: 1.0rem 0 1.5rem;
        }

        .resultados-cabecera h2 {
            margin: 0;
            color: var(--texto);
            font-size: clamp(2rem, 4vw, 3.1rem);
            letter-spacing: -.045em;
        }

        .resultados-cabecera p {
            margin: .5rem 0 0;
            color: var(--suave);
        }

        .contador {
            white-space: nowrap;
            padding: .5rem .8rem;
            border: 1px solid var(--borde);
            border-radius: 99rem;
            color: var(--acento);
            font-size: .78rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .noticia {
            min-height: 295px;
            margin-bottom: 1rem;
            padding: 1.35rem;
            border: 1px solid var(--borde);
            border-radius: 1.15rem;
            background: linear-gradient(145deg, rgba(19, 39, 34, .92), rgba(10, 24, 21, .92));
            transition: transform .2s ease, border-color .2s ease;
        }

        .noticia:hover {
            transform: translateY(-4px);
            border-color: rgba(103, 240, 174, .48);
        }

        .noticia-meta {
            color: var(--acento);
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .noticia h3 {
            margin: 1rem 0 .8rem;
            color: var(--texto);
            font-size: 1.25rem;
            line-height: 1.3;
            letter-spacing: -.02em;
        }

        .noticia p {
            margin: 0 0 1.2rem;
            color: var(--suave);
            font-size: .9rem;
            line-height: 1.6;
        }

        .noticia a {
            color: var(--texto);
            font-size: .85rem;
            font-weight: 800;
            text-decoration: none;
        }

        .noticia a:hover {
            color: var(--acento);
        }

        @media (max-width: 700px) {
            [data-testid="stMainBlockContainer"] {
                padding-top: 2rem;
            }

            .hero h1 {
                font-size: 3.6rem;
            }

            .resultados-cabecera {
                align-items: start;
                flex-direction: column;
            }

            .noticia {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def obtener_noticias(tema, region, enfoque, clave):
    tema = tema.strip()
    if not tema:
        st.warning("Escribí un tema para comenzar la búsqueda.")
        return

    with st.spinner("Explorando las noticias más recientes..."):
        st.session_state[f"{clave}_tema"] = tema
        st.session_state[f"{clave}_region"] = region
        st.session_state[f"{clave}_enfoque"] = enfoque
        st.session_state[f"{clave}_noticias"] = buscar_noticias(tema, region, enfoque)


def mostrar_encabezado():
    st.markdown(
        """
        <div class="marca"><span class="pulso"></span> InfoRadar / Noticias en foco</div>
        <section class="hero">
            <h1>Encontra la señal entre el <span>ruido.</span></h1>
            <p>
                Busca un tema y explora las noticias más recientes en un solo lugar,
                sin distracciones.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def mostrar_filtros(clave):
    region_col, enfoque_col = st.columns(2)
    with region_col:
        region = st.selectbox("Región", REGIONES, key=f"{clave}_selector_region")
    with enfoque_col:
        enfoque = st.selectbox("Categoría", CATEGORIAS, key=f"{clave}_selector_enfoque")
    return region, enfoque


def mostrar_explorar():
    st.markdown(
        '<p class="temas-label">Descubrí qué está pasando</p>',
        unsafe_allow_html=True,
    )
    region, enfoque = mostrar_filtros("explorar")

    filtros_cambiaron = (
        st.session_state.get("explorar_region") != region
        or st.session_state.get("explorar_enfoque") != enfoque
    )
    if not st.session_state.get("explorar_noticias") or filtros_cambiaron:
        obtener_noticias("Actualidad", region, enfoque, "explorar")

    mostrar_resultados("explorar", "Tendencias")


def mostrar_buscar():
    with st.form("busqueda", clear_on_submit=False):
        campo, boton = st.columns([5, 1.2], vertical_alignment="bottom")
        with campo:
            busqueda = st.text_input(
                "Tema",
            )
        with boton:
            buscar = st.form_submit_button("Buscar", use_container_width=True)

        region, enfoque = mostrar_filtros("buscar")

    if buscar:
        obtener_noticias(busqueda, region, enfoque, "buscar")

    if st.session_state.get("buscar_tema"):
        mostrar_resultados("buscar", "Resultados")


def mostrar_resultados(clave, titulo_seccion):
    tema = st.session_state[f"{clave}_tema"]
    noticias = st.session_state[f"{clave}_noticias"]
    region = st.session_state[f"{clave}_region"]
    enfoque = st.session_state[f"{clave}_enfoque"]

    st.markdown(
        f"""
        <div class="resultados-cabecera">
            <div>
                <h2>{escape(titulo_seccion)}: {escape(tema)}</h2>
                <p>{escape(region)} / {escape(enfoque)} / Noticias en español</p>
            </div>
            <span class="contador">{len(noticias)} resultados</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not noticias:
        st.info("No encontré noticias para ese tema. Probá con otra palabra.")
        return

    columnas = st.columns(3)
    for index, noticia in enumerate(noticias):
        titulo = escape(noticia["titulo"])
        descripcion = escape(noticia["descripcion"] or "Lee la cobertura completa en la fuente.")
        fuente = escape(noticia["fuente"])
        fecha = escape(noticia["fecha"])
        url = escape(noticia["url"], quote=True)

        with columnas[index % 3]:
            st.markdown(
                f"""
                <article class="noticia">
                    <div class="noticia-meta">{fuente} / {fecha}</div>
                    <h3>{titulo}</h3>
                    <p>{descripcion}</p>
                    <a href="{url}" target="_blank" rel="noopener noreferrer">
                        Leer noticia &rarr;
                    </a>
                </article>
                """,
                unsafe_allow_html=True,
            )


cargar_estilos()
mostrar_encabezado()
explorar, buscar = st.tabs(["Explorar", "Buscar"])
with explorar:
    mostrar_explorar()
with buscar:
    mostrar_buscar()
