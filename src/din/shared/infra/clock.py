from datetime import datetime
from zoneinfo import ZoneInfo
from din.shared.core.clock import Clock


class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(ZoneInfo("America/Recife"))
