"""DataUpdateCoordinator for Xplora Watch Tracker."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import XploraApiClient, XploraApiError, XploraAuthError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class XploraCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Polls Xplora API for all watch data on a schedule."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: XploraApiClient,
        watches: list[dict[str, str]],
        scan_interval: int = DEFAULT_SCAN_INTERVAL,
    ) -> None:
        self.client  = client
        self.watches = watches  # [{wuid, name}, ...]

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch latest data for every watch. Called by HA on each poll cycle."""
        result: dict[str, Any] = {}

        for watch in self.watches:
            wuid = watch["wuid"]
            try:
                location = await self.client.get_watch_location(wuid)
                result[wuid] = location
                _LOGGER.debug("Updated %s: %s", watch["name"], location)
            except XploraAuthError as err:
                # Token expired — trigger HA reauth flow
                raise ConfigEntryAuthFailed(
                    f"Xplora authentication expired: {err}"
                ) from err
            except XploraApiError as err:
                _LOGGER.warning("Failed to update watch %s: %s", watch["name"], err)
                # Keep last known data if available, don't fail everything
                if self.data and wuid in self.data:
                    result[wuid] = self.data[wuid]

        if not result:
            raise UpdateFailed("No data returned for any watch")

        return result
