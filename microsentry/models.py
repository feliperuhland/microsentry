import dataclasses
import datetime
import typing


@dataclasses.dataclass
class Context:
    build: str
    name: str
    version: str


@dataclasses.dataclass
class Frame:
    abs_path: str
    context_line: str
    filename: str
    function: str
    lineno: int
    module: str
    pre_context: typing.List[str]
    post_context: typing.List[str]
    variable_map: typing.Dict[str, str]


@dataclasses.dataclass
class SentryException:
    frame_list: typing.List[Frame]
    handled: bool
    module: str
    type: str
    value: str


@dataclasses.dataclass
class Event:
    id: str
    context: Context
    level: str
    modules: typing.Dict[str, str]
    server_name: str
    timestamp: datetime.datetime
    project_id: int
    exception_list: typing.List[SentryException]
