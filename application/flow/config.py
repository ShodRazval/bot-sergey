from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.words_repository import WordsRepository
from application.flow.flow_service import FlowService
from application.flow.handlers.joke_check import JokeCheck
from application.flow.handlers.self_check import SelfCheck

__joke_repository: JokesRepository
__words_repository: WordsRepository


def init_flow_context(jokes_repository: JokesRepository, words_repository: WordsRepository):
    global __joke_repository, __words_repository
    __joke_repository = jokes_repository
    __words_repository = words_repository


def create_flow() -> FlowService:
    global __joke_repository, __words_repository

    self_check = SelfCheck()
    joke_check = JokeCheck(jokes_repository=__joke_repository,
                           words_repository=__words_repository)

    flow = {
        self_check.order(): self_check,
        joke_check.order(): joke_check
    }

    return FlowService(flow)
