from dataclasses import dataclass, field

from typing import List

from tonguetwister.xformat.cast import Cast
from tonguetwister.xformat.info import Info
from tonguetwister.xformat.score import Score


@dataclass()
class MovieFormat:
    info: Info = Info()
    casts: List[Cast] = field(default_factory=list)
    score: Score = Score()

