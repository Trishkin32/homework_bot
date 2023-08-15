class ApiConnectError(Exception):
    """Исключение возникает при запросе к API."""

    pass


class TelegramError(Exception):
    """Исключение возникает при ошибки Telegrama."""

    pass
