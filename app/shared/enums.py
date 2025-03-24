from enum import Enum


class Statuses(Enum):
    ONLIME = "online"
    OFFLINE = "offline"
    BANNED = "banned"


class Roles(Enum):
    OWNER = "owner"
    WORKER = "worker"
