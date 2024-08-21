"""api"""

import logging, sys

log_level: int = logging.INFO
logging.basicConfig(level = log_level)
logger: logging.Logger = logging.getLogger(__name__)

sites: dict[str] = {
    'br': "https://origins.habbo.com.br/api/public/",
    'es': "https://origins.habbo.es/api/public/",
    'en': "https://origins.habbo.com/api/public/",
}

try:
    # ~ ## FIXME aiodns no windows não me deixa testar
    # ~ import aiohttp
    # ~ import asyncio
    import datetime
    import requests
    from fastapi import FastAPI
except Exception as e:
    logger.exception(e)
    sys.exit("Erro fatal, stacktrace acima")

app: FastAPI = FastAPI()

# ~ async def get_aurl(url: str = "") -> str:
    # ~ """Get url with AIOHTTP"""
    # ~ ## FIXME aiodns no windows não me deixa testar
    # ~ async with aiohttp.ClientSession() as session:
        # ~ async with session.get(url) as response:
            # ~ if response.status == "200":
                # ~ data: str = await response.json()
                # ~ if data:
                    # ~ return data
    # ~ return {"status": True}

async def get_status(url: str) -> int:
    """Get HTTP status code with requests"""
    try:
        response: requests.Request = requests.get(url)
        return response.status_code
    except Exception as e:
        logger.exception(e)
    ## https://github.com/joho/7XX-rfc
    return 776

async def get_text(url: str) -> dict:
    """Get text data with requests"""
    try:
        response: requests.Request = requests.get(url)
        if response.status_code == 200:
            data: str = response.text
            if data:
                return {
                    "status": True,
                    "message": data,
                }
    except Exception as e:
        logger.exception(e)
    return {
        "status": False,
        "message": "Servidor do Origins não retornou porra nenhuma",
    }

async def get_json(url: str) -> dict:
    """Get json data with requests"""
    try:
        response: requests.Request = requests.get(url)
        if response.status_code == 200:
            data: str = response.json()
            if data:
                return {
                    "status": True,
                    "message": data,
                }
    except Exception as e:
        logger.exception(e)
    return {
        "status": False,
        "message": "Servidor do Origins não retornou porra nenhuma",
    }

@app.get("/")
async def index() -> dict:
    """GET /"""
    return {
        "status": True,
        "message": """Lista de endpoints:\
https://origins.habbo.com/api/public/api-docs/"""
    }

@app.get("/teste")
async def teste() -> dict:
    """GET /teste"""
    return {
        "status": True,
        "message": await get_request("https://httpbin.org/headers"),
    }

@app.get("/status")
async def status(lang: str = 'br') -> dict:
    """GET /ping"""
    return {
        "status": True,
        "response": await get_status("/".join([sites[lang], "ping"])),
    }

@app.get("/users")
async def users(lang: str = "br") -> dict:
    """GET /users"""
    try:
        return {
            "status": True,
            "message": await get_json("/".join([sites[lang],
                "origins", "users"])),
        }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/user/name/{name}")
async def user_name(name: str = "", lang: str = "br") -> dict:
    """GET /users?name"""
    try:
        if name not in ["", " ", None, False]:
            return {
                "status": True,
                "message": await get_json("/".join([sites[lang],
                    f"users?name={name}"])),
            }
        else:
            return {
                "status": False,
                "message": "Qual é o name, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/user/id/{uid}")
async def user_id(uid: str = "", lang: str = "br") -> dict:
    """GET /users/uid"""
    try:
        if uid not in ["", " ", None, False]:
            return {
                "status": True,
                "message": await get_json("/".join([sites[lang],
                    "users", f"{uid}"])),
            }
        else:
            return {
                "status": False,
                "message": "qual é o uid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/player/{pid}")
async def player(pid: str = "", lang: str = "br") -> dict:
    """Get user by pid"""
    try:
        if pid not in ["", " ", None, False]:
            uid: dict = await get_json("/".join([sites[lang],
                "users", "by-playerId", f"{pid}"]))
            if uid["status"]:
                return await get_json("/".join([sites[lang],
                    "users", f'{uid["message"]["uniqueId"]}']))
            else:
                return uid
        else:
            return {
                "status": False,
                "message": "qual é o pid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/matches/{pid}")
async def matches(
    pid: str = "",
    offset: int = 0,
    limit: int = 10,
    start_time: str =  (datetime.datetime.now(datetime.UTC) - 
        datetime.timedelta(days = 1)).timestamp(),
    end_time: str = datetime.datetime.now(datetime.UTC).timestamp(),
    lang: str = "br",
) -> dict:
    """GET /matches/v1/uniquePlayerId/ids"""
    try:
        if pid not in ["", " ", None, False]:
            return await get_json("/".join([sites[lang],
                "matches", "v1", f"{pid}",
                "&".join([f"ids?offset={offset}", f"limit={limit}", 
                f"""start_time=\
{datetime.datetime.fromtimestamp(
start_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}""",
                f"""end_time=\
{datetime.datetime.fromtimestamp(
end_time).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}"""
            ])]))
        else:
            return {
                "status": False,
                "message": "qual é o pid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/match/{mid}")
async def match(
    mid: str = "",
    lang: str = "br",
) -> dict:
    """GET /matches/v1/uniqueMatchId"""
    try:
        if mid not in ["", " ", None, False]:
            return await get_json("/".join([sites[lang],
                "api", "public", "matches", "v1", f"{mid}"]))
        else:
            return {
                "status": False,
                "message": "qual é o pid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/pid2uid")
async def pid2uid(pid: str, lang: str = "br") -> dict:
    """Get uniqueHabboId from uniquePlayerId"""
    try:
        return {
            "status": True,
            "message": await get_json("/".join([sites[lang],
                "users", "by-playerId", f"{pid}"])),
        }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/uid2pid")
async def uid2pid(uid: str, lang: str = "br") -> dict:
    """Get uniquePlayerId from uniqueHabboId"""
    try:
        if uid not in ["", " ", None, False]:
            user: dict = await get_json("/".join([sites[lang],
                "users", f"{uid}"]))
            if user["status"]:
                return {
                    "status": True,
                    "message": user["message"]["bouncerPlayerId"],
                }
            else:
                return user
        else:
            return {
                "status": False,
                "message": "qual é o uid, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/name2pid")
async def name2pid(name: str, lang: str = "br") -> dict:
    """Get uniquePlayerId from name"""
    try:
        if name not in ["", " ", None, False]:
            user: dict = await get_json("/".join([sites[lang],
                f"users?name={name}"]))
            if user["status"]:
                return {
                    "status": True,
                    "message": user["message"]["bouncerPlayerId"],
                }
            else:
                return user
        else:
            return {
                "status": False,
                "message": "qual é o name, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }

@app.get("/name2uid")
async def name2uid(pid: str, lang: str = "br") -> dict:
    """Get uniqueHabboId from name"""
    try:
        if name not in ["", " ", None, False]:
            user: dict = await get_json("/".join([sites[lang],
                f"users?name={name}"]))
            if user["status"]:
                return {
                    "status": True,
                    "message": user["message"]["uniqueId"],
                }
            else:
                return user
        else:
            return {
                "status": False,
                "message": "qual é o name, porra?",
            }
    except Exception as e:
        return {
            "status": False,
            "message": repr(e),
        }
