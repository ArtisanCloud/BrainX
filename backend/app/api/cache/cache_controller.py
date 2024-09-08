from fastapi import APIRouter

from app.cache.factory import CacheFactory

router = APIRouter()


@router.get("/remember")
async def api_remember():
    def return_version():
        print("returned no cached version")
        return "1.0.0"

    cache = CacheFactory.get_cache()

    version = await cache.remember("brain_x_version", 3600, func=return_version)

    return {
        "version": version
    }
