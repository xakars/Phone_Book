from enum import Enum

class Verb_Request(Enum):
    GET = "ОТДОВАЙ"
    DELETE = "УДОЛИ"
    WRITE = "ЗОПИШИ"

MODE_VERB = {
        1: Verb_Request.GET,
        2: Verb_Request.WRITE,
        3: Verb_Request.DELETE
}

