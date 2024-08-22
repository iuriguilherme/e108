"""Web"""

import logging, sys
logger: logging.Logger = logging.getLogger(__name__)

try:
    import aiohttp
    from jinja2 import TemplateNotFound
    # ~ import json
    import os
    from quart import (
        Quart,
        render_template,
        request,
    )
    # ~ from quart_sqlalchemy.framework import QuartSQLAlchemy
    # ~ from quart_wtf.csrf import CSRFProtect
    import secrets
    # ~ from werkzeug.utils import secure_filename
    ## TODO: mudar pra .. quando empacotar(emmodular?) web
    from . import (
        __description__ as description,
        __name__ as name,
        __version__ as version,
    )
    from .api import placar
    # ~ from .forms import (
      # ~ TestForm,
    # ~ )
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

site: str = "habborigins.com.br"
busers: list = [
    'iggy1',
]

app: object = Quart(__name__)
app.secret_key: str = os.getenv(
    'QUART_SECRET',
    default = secrets.token_urlsafe(32),
)
# ~ csrf: object = CSRFProtect(app)

@app.route("/", defaults = {"pagina": "index"})
@app.route("/<pagina>")
async def carregar(
    pagina: str,
    title: str = f"{name} v{version}: {description}",
    color: str = "primary",
) -> str:
    """Attempt to load template for `pagina`"""
    if pagina == 'favicon.ico':
        return ""
    else:
        try:
            return await render_template(
                f"{pagina}.html",
                color = color,
                description = description,
                name = name,
                site = site,
                title = title,
                version = version,
            )
        except Exception as e:
            logger.exception(e)
            try:
                return await render_template(
                    "error.html",
                    error = repr(e),
                    site = site,
                    title = "Erro",
                )
            except Exception as e1:
                logger.exception(e1)
                return f"""O erro foi tão foda que nem a página de erro \
carregou: {jsonify(repr(e1))}"""

@app.route("/battleball")
async def battleball() -> str:
    """Ranking Battle Ball"""
    try:
        return await render_template(
            "battleball.html",
            color = "success",
            description = description,
            name = name,
            rankings = await placar(),
            site = site,
            title = "Ranking Battle Ball",
            version = version,
        )
    except Exception as e:
        logger.exception(e)
        try:
            return await render_template(
                "error.html",
                description = description,
                error = repr(e),
                name = name,
                site = site,
                title = "Erro",
                version = version,
            )
        except Exception as e1:
            logger.exception(e1)
            return f"""O erro foi tão foda que nem a página de erro \
carregou: {jsonify(repr(e1))}"""

@app.errorhandler(400)
@app.route("/error_400")
async def error_400(*exceptions: Exception) -> str:
    """Erro 4xx"""
    for exception in exceptions:
        logger.exception(exception)
    logger.warning("Erro não tratado, stacktrace acima")
    try:
        return await render_template(
            "error.html",
            description = description,
            error = """Tivemos um problema com esta solicitação e os \
responsáveis já foram notificados. Tente novamente mais tarde ou entre \
em contato com o suporte.""",
            name = name,
            site = site,
            title = "Erro bem errado",
            version = version,
        ), 400
    except Exception as e:
        logger.exception(e)
        return f"""O erro foi tão foda que nem a página de erro carregou: \
{jsonify(repr(e))}"""

@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
@app.route("/não_existe")
async def error_404(*exceptions: Exception) -> str:
    """Não encontrado"""
    for exception in exceptions:
        logger.exception(exception)
    logger.warning("""Tentaram acessar uma página que não existe, \
stacktrace acima""")
    try:
        return await render_template(
            "error.html",
            description = description,
            error = """Alguém te deu o link errado, ou esta página foi \
removida.""",
            name = name,
            site = site,
            title = "Não encontrado",
            version = version,
        ), 404
    except Exception as e:
        logger.exception(e)
        return f"""O erro foi tão foda que nem a página de erro carregou: \
{jsonify(repr(e))}"""

@app.errorhandler(500)
@app.route("/error_500")
async def error_500(*exceptions: Exception) -> str:
    """Erro 5xx"""
    for exception in exceptions:
        logger.exception(exception)
    logger.warning("Erro não tratado, stacktrace acima")
    try:
        return await render_template(
            "error.html",
            description = description,
            error = """Tivemos um problema com esta solicitação e os \
responsáveis já foram notificados. Tente novamente mais tarde ou entre \
em contato com o suporte.""",
            name = name,
            site = site,
            title = "Erro errado",
            version = version,
        ), 500
    except Exception as e:
        logger.exception(e)
        return f"""O erro foi tão foda que nem a página de erro carregou: \
{jsonify(repr(e))}"""

@app.route("/teste")
async def teste(nome: str = "iggy1")-> str:
    """Teste"""
    try:
        for buser in busers:
            await atualiza_rank(buser)
        return "OK"
    except Exception as e:
        logger.exception(e)
        try:
            return await render_template(
                "error.html",
                description = description,
                error = repr(e),
                name = name,
                site = site,
                title = "Erro",
                version = version,
            )
        except Exception as e1:
            logger.exception(e1)
            return f"""O erro foi tão foda que nem a página de erro \
carregou: {jsonify(repr(e1))}"""
