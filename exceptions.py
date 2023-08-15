class NotTelegramSending(Exception):
    """Не для отправления в телеграм."""

    pass


class ApiConnectError(NotTelegramSending):
    """Исключение возникает при запросе к API."""

    pass


class MessageSendingError(NotTelegramSending):
    """Ошибка телеграма."""

    pass
