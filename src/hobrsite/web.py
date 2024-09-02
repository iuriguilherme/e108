"""Web"""

import logging, sys
logger: logging.Logger = logging.getLogger(__name__)

try:
    import aiohttp
    from jinja2 import TemplateNotFound
    # ~ import json
    import os
    from quart import (
        jsonify,
        Quart,
        render_template,
        request,
    )
    # ~ from quart_wtf.csrf import CSRFProtect
    import secrets
    # ~ from werkzeug.utils import secure_filename
    ## TODO: mudar pra .. quando empacotar(emmodular?) web
    from . import (
        __description__ as description,
        __name__ as name,
        __version__ as version,
    )
    from .api.v2 import get_placar
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
    """Battle Ball"""
    try:
        placar: dict = await get_placar("um")
        if placar["status"]:
            return await render_template(
                "battleball/index.html",
                color = "success",
                description = description,
                name = name,
                rankings = placar["message"],
                site = site,
                title = "Ranking Battle Ball",
                version = version,
            )
        else:
            return await render_template(
                "error.html",
                description = description,
                error = placar["message"],
                name = name,
                site = site,
                title = "Não deu certo",
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

@app.route("/comunidade")
async def comunidade() -> str:
    """Links úteis e outros nem tanto"""
    try:
        return await render_template(
            "comunidade.html",
            color = "primary",
            description = description,
            name = name,
            site = site,
            title = "Links úteis",
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

@app.route("/info")
async def info() -> str:
    """Informações sobre este site"""
    try:
        return await render_template(
            "info.html",
            color = "primary",
            description = description,
            name = name,
            site = site,
            title = "F.A.Q.",
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

@app.route("/atualiza")
async def atualiza()-> str:
    """Atualiza rank último dia"""
    try:
        retorno: list[dict] = []
        for buser in busers:
            retorno.append(await atualizar(buser))
        return await render_template(
            "error.html",
            description = description,
            error = jsonify(retorno),
            name = name,
            site = site,
            title = "Dessa vez não é um erro",
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
