import json

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Module:
    name: str
    contact: str
    description: str
    properties: Dict[str, str]
    template: Optional[str] = "default"
    app_template: Optional[str] = "default"


@dataclass
class Pipeline:
    type: str
    namespace: str
    properties: Dict[str, str]


@dataclass
class Application:
    modules: List[Module]
    pipelines: List[Pipeline]


