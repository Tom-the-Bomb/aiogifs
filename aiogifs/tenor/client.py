from .http import HTTPClient, Route
import asyncio
from aiohttp import ClientSession # just for type hinting
from typing import Optional
from .types import MediaFilter, AspectRatio, ContentFilter
from .models import TenorResponse


class TenorClient:
    def __init__(self, *, api_key: str, session: Optional[ClientSession] = None):
        """Initialises the TenorClient

        :param api_key: Your API Key for the Tenor API
        :type api_key: str
        :param session: Allows for custom session passing. If none is passed, a new session is created, defaults to None
        :type session: Optional[ClientSession], optional
        """
        self._auth = api_key
        self.http = HTTPClient(api_key = self._auth, session = session)

    async def search(self, query: str, *, locale: Optional[str] = None, content_filter: Optional[ContentFilter] = "off", media_filter: Optional[MediaFilter] = None, ar_range: Optional[AspectRatio] = None, limit: Optional[int] = None, pos: Optional[int] = None, anon_id: Optional[str] = None) -> TenorResponse:
        """Searches tenor with the provided query.

        :param query: The query used to search Tenor
        :type query: str
        :param locale: The locale. Usually in the format of xx_YY, defaults to None
        :type locale: Optional[str], optional
        :param content_filter: The strength of the content filter, defaults to "off"
        :type content_filter: Optional[ContentFilter], optional
        :param media_filter: The type of Media Filter used. This filters the types of media returned, defaults to None
        :type media_filter: Optional[MediaFilter], optional
        :param ar_range: Aspect Ratio range. Limits the size of media returned, defaults to None
        :type ar_range: Optional[AspectRatio], optional
        :param limit: Limits how many results you get returned, defaults to None
        :type limit: Optional[int], optional
        :param pos: [description], defaults to None
        :type pos: Sets a starting value to search from, optional
        :param anon_id: Specify the anonymous_id tied to the given user, defaults to None
        :type anon_id: Optional[str], optional
        :return: Returns a TenorResponse object. Holds the media returned to us.
        :rtype: TenorResponse
        """
        params = {
            "q": query,
            "locale": locale,
            "contentfilter": content_filter,
            "mediafilter": media_filter,
            "ar_range": ar_range,
            "limit": limit,
            "pos": pos,
            "anon_id": anon_id

        }
        params = self._filter_params(params)
        route = Route("/search", params = params)
        data = await self.http.request(route)
        return TenorResponse(data = data)

    async def trending(self, *, locale: Optional[str] = None, content_filter: Optional[ContentFilter] = "off", media_filter: Optional[MediaFilter] = None, ar_range: Optional[AspectRatio] = None, limit: Optional[int] = None, pos: Optional[int] = None, anon_id: Optional[str] = None) -> TenorResponse:
        """Fetches currently trending media on Tenor

        :param locale: The locale. Usually in the format of xx_YY, defaults to None
        :type locale: Optional[str], optional
        :param content_filter: The strength of the content filter, defaults to "off"
        :type content_filter: Optional[ContentFilter], optional
        :param media_filter: The type of Media Filter used. This filters the types of media returned, defaults to None
        :type media_filter: Optional[MediaFilter], optional
        :param ar_range: Aspect Ratio range. Limits the size of media returned, defaults to None
        :type ar_range: Optional[AspectRatio], optional
        :param limit: Limits how many results you get returned, defaults to None
        :type limit: Optional[int], optional
        :param pos: [description], defaults to None
        :type pos: Sets a starting value to search from, optional
        :param anon_id: Specify the anonymous_id tied to the given user, defaults to None
        :type anon_id: Optional[str], optional
        :return: Returns a TenorResponse object. Holds the media returned to us.
        :rtype: TenorResponse
        """
        params = {
            "locale": locale,
            "contentfilter": content_filter,
            "mediafilter": media_filter,
            "ar_range": ar_range,
            "limit": limit,
            "pos": pos,
            "anon_id": anon_id

        }
        params = self._filter_params(params)
        route = Route("/trending", params = params)
        data = await self.http.request(route)
        return TenorResponse(data = data)

    async def close(self):
        """Cleans up. Primarily HTTP Session closing.
        """
        return await self.http.cleanup()

    async def connect(self):
        """Opens the aiohttp.ClientSession(), thus allowing connections to the Tenor API
        """
        return await self.http.open_session()

    def  _filter_params(self, map: dict) -> dict:
        new_dict = {k: v for k, v in map.items() if v is not None}
        return new_dict
