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

class ResponseStatus(Enum):
    """Response statuses specified in RKSOK specs for responses"""
    OK = "НОРМАЛДЫКС"
    NOTFOUND = "НИНАШОЛ"
    NOT_APPROVED = "НИЛЬЗЯ"
    INCORRECT_REQUEST = "НИПОНЯЛ"

