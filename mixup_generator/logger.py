from loguru import logger

logger.add(
    "../logs/MixupGenerator.log",
    colorize=True,
    format="<level>{time:YYYY-MM-DD at HH:mm:ss} {message}</level>",
    rotation="1 day",
)

logger.level("CRITICAL", color="<red>", icon="💀")
