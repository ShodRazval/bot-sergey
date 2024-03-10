import configuration
from application.datasource.repositories.repositories import MongoRepositories
from application.flow.config import init_flow_context, create_flow
from application.telegram_bot.bot_controller import run_bot
from application.telegram_bot.bot_processor import init_processor


def main():
    # Init datasource
    repositories = MongoRepositories.instance()

    init_flow_context(repositories.get_jokes_repository(), repositories.get_words_repository())

    init_processor(
        repositories.get_jokes_repository(),
        repositories.get_users_repository(),
        repositories.get_words_repository(),
        create_flow()
    )

    # Start bot
    run_bot()


if __name__ == "__main__":
    main()
