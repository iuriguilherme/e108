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
        rankings: dict = dict()
        requalificados: str = ["Tranquilo", "Trax", "Cyrex", "Shadow"]
        desqualificados: str = ["Greg", "LendaryChacal", "lysao", "DON.GOLD"]
        dragon_id_map: dict[str] = {
            "default": "Desconhecido",
            "Hugo": "Desconhecido",
            "Charizard": "Desconhecido",
            "Rimuru": "95200",
            "Rei": "95201",
            "Shirato": "Desconhecido",
            "Tanuke": "Desconhecido",
            "Paris": "Desconhecido",
            "Nicdragon": "95205",
            "DrMax": "95206",
            "Bravura": "95207",
            "jcesarneto": "95208",
            "Onigiri": "Desconhecido",
            "Mentalizado": "95210",
            "Bezinazzi": "95211",
            "Amo": "Desconhecido",
            "Astronis": "95213",
            "Cotonete": "95214",
            ".Red": "95215",
            "Jaguar": "95216",
            "Cigas": "95217",
            "CarlosAndre": "95218",
            "Bad": "95219",
            "Raskolnikov": "95220",
            "Luks": "95221",
            "Senho": "95222",
            "MatheusCaldas": "95223",
            "Vascaina": "95224",
            "Clint": "95225",
            "Pesadelos": "95226",
            "Viktor": "Desconhecido",
            "Socorro": "95228",
            "DDD": "95229",
            "iggy1": "95230",
            "Ryco": "95231",
            "Externet": "Desconhecido",
            "4Cheese": "95233",
            "Tranquilo": "95234",
            "Trax": "Desconhecido",
            "Cyrex": "Desconhecido",
            "Shadow": "95237",
        }
        placar: dict = await get_placar("um")
        if placar["status"]:
            for i, (nome, pontos) in enumerate(placar["message"]):
                premio: str = "Porra Nenhuma"
                table_color: str = "light"
                prize_img: str = "red_cross.gif"
                situacao: str = "Normal"
                if 0 <= i <= 4:
                    premio = f"""Dragão Dourado (\
{dragon_id_map.get(nome, dragon_id_map.get("default"))})"""
                    table_color = "warning"
                    situacao = "Qualificado"
                    prize_img = "dragon_gold.gif"
                elif 5 <= i <= 14:
                    premio = f"""Dragão Prateado (\
{dragon_id_map.get(nome, dragon_id_map.get("default"))})"""
                    table_color = "secondary"
                    situacao = "Qualificado"
                    prize_img = "dragon_silver.gif"
                elif 15 <= i <= 43:
                    premio = f"""Dragão de Bronze (\
{dragon_id_map.get(nome, dragon_id_map.get("default"))})"""
                    table_color = "danger"
                    situacao = "Qualificado"
                    prize_img = "dragon_bronze.gif"
                if nome in desqualificados:
                    premio = "Porra Nenhuma"
                    situacao = "Desqualificado"
                    table_color = "info"
                    prize_img = "red_cross.gif"
                elif nome in requalificados:
                    premio = f"""Dragão de Bronze (\
{dragon_id_map.get(nome, dragon_id_map.get("default"))})"""
                    situacao = "Qualificado"
                    table_color = "danger"
                    prize_img = "dragon_bronze.gif"
                rankings[nome] = {
                    "pontos": pontos,
                    "premio": premio,
                    "situacao": situacao,
                    "table_color": table_color,
                    "prize_img": prize_img,
                    "dragon_id": dragon_id_map.get(nome,
                        dragon_id_map.get("default")),
                }
            rankings["LILO"] = {
                "pontos": 690420,
                "premio": "Troféu de Pato de Bronze do iggy1",
                "situacao": "Banido",
                "table_color": "primary",
                "prize_img": "favicon.ico",
                "dragon_id": dragon_id_map.get("LILO",
                    dragon_id_map.get("default")),
            }
            rankings["Butter"] = {
                "pontos": 171157,
                "premio": "Troféu de Pato de Prata do iggy1",
                "situacao": "Banido",
                "table_color": "primary",
                "prize_img": "favicon.ico",
                "dragon_id": dragon_id_map.get("Butter",
                    dragon_id_map.get("default")),
            }
            if "DON.GOLD" in rankings:
                rankings["DON.GOLD"]["premio"] = """Troféu de Pato de Ouro \
do iggy1"""
                rankings["DON.GOLD"]["table_color"] = "success"
                rankings["DON.GOLD"]["prize_img"] = "favicon.ico"
            if "Greg" in rankings:
                rankings["Greg"]["premio"] = f"""Dragão de Bronze do Astronis \
({dragon_id_map.get("Astronis", dragon_id_map.get("default"))})"""
                rankings["Greg"]["table_color"] = "success"
                rankings["Greg"]["prize_img"] = "favicon.ico"
            return await render_template(
                "battleball/index.html",
                color = "success",
                description = description,
                name = name,
                rankings = {k: v for k, v in sorted(rankings.items(),
                    key = lambda r: r[1]["pontos"], reverse = True)},
                site = site,
                title = "Ranking Battle Ball",
                version = version,
                premio = premio,
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
