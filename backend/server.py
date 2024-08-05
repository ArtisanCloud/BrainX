import sys

import alembic
import uvicorn
from app.config.config import settings
from app.logger import logger
import asyncio


def start():
    print("Running in AppEnvironment: " + settings.server.environment)
    # __setup_sentry()
    """Launched with `poetry run start` at root level"""

    if settings.server.server_render:
        # on render.com deployments, run migrations
        logger.debug("Running migrations")
        alembic_args = ["--raiseerr", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        logger.debug("Migrations complete")
    else:
        logger.debug("Skipping migrations")

    # if need fastapi reload
    live_reload = not settings.server.server_render
    # print(live_reload, settings.server.worker_count)
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=live_reload,
        workers=settings.server.worker_count,

    )


def main():
    if len(sys.argv) <= 1:
        print("Please provide a command")
        sys.exit(1)

    if "--database" in sys.argv:
        from app.database.alembic_manager import AlembicManager
        alembic_manager = AlembicManager()

        if "--migrate" in sys.argv:
            try:
                e = alembic_manager.upgrade()
                if e:
                    logger.error(e)
                    raise e
            except (IndexError, ValueError):
                sys.exit(1)

        if "--downgrade" in sys.argv:
            if "--steps" in sys.argv:
                try:
                    steps_index = sys.argv.index("--steps") + 1
                    steps = int(sys.argv[steps_index])
                    e = alembic_manager.downgrade(steps=steps)
                    if e:
                        logger.error(e)
                        raise e
                except (IndexError, ValueError):
                    print("Please provide a valid number of steps after --steps")
                    sys.exit(1)

            elif "--version" in sys.argv:
                try:
                    version_index = sys.argv.index("--version") + 1
                    version = sys.argv[version_index]
                    e = alembic_manager.downgrade_to_version(version)
                    if e:
                        logger.error(e)
                        raise e
                except IndexError:
                    print("Please provide a valid version after --version")
                    sys.exit(1)

            else:
                print("Please provide --steps or --version when use --downgrade")

        elif "--downgrade-all" in sys.argv:
            e = alembic_manager.downgrade_all()
            if e:
                logger.error(e)
                raise e

        if "--upgrade-to-version" in sys.argv:
            try:
                version_index = sys.argv.index("--upgrade-to-version") + 1
                version = sys.argv[version_index]
                e = alembic_manager.upgrade_to_version(version)
                if e:
                    logger.error(e)
                    raise e
            except IndexError:
                print("Please provide a valid version after --upgrade-to-version")
                sys.exit(1)

    if "--seed" in sys.argv:
        from app.database.seed.main import start_seed

        e = asyncio.run(start_seed())
        if e:
            logger.error(e)
            raise e

    if "--start" in sys.argv:
        from app.main import start
        start()


if __name__ == '__main__':
    main()
