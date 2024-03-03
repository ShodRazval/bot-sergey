from aiogram import Bot

from application.datasource.repositories.users_stats_repository import UserStatsRepository

__users_repository: UserStatsRepository
__bot: Bot


def init_stats_service(users_repository: UserStatsRepository,
                       bot: Bot):
    global __users_repository, __bot
    __users_repository = users_repository
    __bot = bot


def get_stats(chat_id: str) -> str:
    __bot.get_chat_member()