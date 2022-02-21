import logging
from typing import List, Optional

import objectrest

from dim import static
from dim._info import __title__
from dim.decorators import get_json, post_bool, delete_bool, patch_bool
from dim.utils import _is_invalid_choice, build_optional_params, int_list_to_string


class API:
    def __init__(self, base_url: str, username: str, password: str, verbose: bool = False):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self._url = f"{base_url}/api/v1"
        self._session = objectrest.Session()
        self._token = None
        logging.basicConfig(format='%(levelname)s:%(message)s', level=(logging.DEBUG if verbose else logging.ERROR))
        self._logger = logging.getLogger(__title__)
        if not self._authenticate(username=username, password=password):
            raise Exception("Authentication failed")

    def _get(self, command: str, params: dict = None) -> objectrest.Response:
        """
        Get response from API call
        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: Response from the API
        :rtype: objectrest.Response
        """
        if not params:
            params = {}
        headers = {}
        if self._token:
            headers = {'Authorization': f"{self._token}"}
        url = f"{self._url}/{command}"
        return self._session.get(url=url, params=params, headers=headers)

    def _get_json(self, command: str, params: dict = None) -> dict:
        """
        Get JSON data from API call

        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: JSON data from the API response
        :rtype: dict
        """
        response = self._get(command=command, params=params)
        if response:
            return response.json()
        return static.empty_dict

    def _post(self, command: str, params: dict = None, **kwargs) -> objectrest.Response:
        """
        Post response from API call
        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: Response from the API
        :rtype: objectrest.Response
        """
        if not params:
            params = {}
        headers = {}
        if self._token:
            headers = {'Authorization': f"{self._token}"}
        url = f"{self._url}/{command}"
        return self._session.post(url=url, params=params, headers=headers, **kwargs)

    def _post_json(self, command: str, params: dict = None, **kwargs) -> dict:
        """
        Post JSON data from API call

        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: JSON data from the API response
        :rtype: dict
        """
        response = self._post(command=command, params=params, **kwargs)
        if response:
            return response.json()
        return static.empty_dict

    def _patch(self, command: str, params: dict = None, **kwargs) -> objectrest.Response:
        """
        Patch response from API call
        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: Response from the API
        :rtype: objectrest.Response
        """
        if not params:
            params = {}
        headers = {}
        if self._token:
            headers = {'Authorization': f"{self._token}"}
        url = f"{self._url}/{command}"
        return self._session.patch(url=url, params=params, headers=headers, **kwargs)

    def _patch_json(self, command: str, params: dict = None, **kwargs) -> dict:
        """
        Patch JSON data from API call

        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: JSON data from the API response
        :rtype: dict
        """
        response = self._patch(command=command, params=params, **kwargs)
        if response:
            return response.json()
        return static.empty_dict

    def _delete(self, command: str, params: dict = None, **kwargs) -> objectrest.Response:
        """
        Delete response from API call
        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: Response from the API
        :rtype: objectrest.Response
        """
        if not params:
            params = {}
        headers = {}
        if self._token:
            headers = {'Authorization': f"{self._token}"}
        url = f"{self._url}/{command}"
        return self._session.delete(url=url, params=params, headers=headers, **kwargs)

    def _delete_json(self, command: str, params: dict = None, **kwargs) -> dict:
        """
        Delete JSON data from API call

        :param command: Dim endpoint
        :type command: str
        :param params: Dictionary of parameters to add to url
        :type params: dict, optional
        :return: JSON data from the API response
        :rtype: dict
        """
        response = self._delete(command=command, params=params, **kwargs)
        if response:
            return response.json()
        return static.empty_dict

    def _authenticate(self, username: str, password: str) -> bool:
        response = self._post_json(command="auth/login", json={"username": username, "password": password})
        if response:
            self._token = response["token"]
            return True
        return False

    @property
    @get_json
    def libraries(self) -> List[dict]:
        return 'library', None

    @get_json
    def get_library_items(self, library_id: str) -> List[dict]:
        return f'library/{library_id}/media', None

    @get_json
    def get_unmatched_library_items(self, library_id: str) -> List[dict]:
        return f'library/{library_id}/unmatched', None

    @get_json
    def get_media(self, media_id: int) -> dict:
        return f'media/{media_id}', None

    @get_json
    def get_media_files(self, media_id: int) -> dict:
        return f'media/{media_id}/files', None

    @patch_bool
    def update_media(self, media_id: int, **kwargs) -> dict:
        return f'media/{media_id}', {'data': kwargs}

    @delete_bool
    def delete_media(self, media_id: int) -> dict:
        return f'media/{media_id}', None

    @post_bool
    def map_progress(self, media_id: int) -> bool:
        return f'media/{media_id}/progress', None

    @get_json
    def get_media_file_info(self, media_id: int) -> dict:
        return f"mediafile/{media_id}", None

    @patch_bool
    def rematch_media_file(self, media_id: int, tmdb_id: int, media_type: str) -> dict:
        if _is_invalid_choice(media_type, 'media_type', ['movie', 'tv']):
            raise Exception("Invalid media type")
        return f"mediafile/{media_id}/match", {'tmdb_id': tmdb_id, 'media_type': media_type}

    @get_json
    def get_library(self, library_id: int) -> dict:
        return f'library/{library_id}/media', None

    def add_library(self, paths: List[str], name: str, media_type: str) -> bool:
        if _is_invalid_choice(media_type, 'media_type', ['movie', 'tv']):
            raise Exception("Invalid media type")
        response = self._post(command="library", json={"locations": paths, "name": name, "media_type": media_type})
        if response:
            return True
        return False

    @delete_bool
    def delete_library(self, library_id: int) -> bool:
        return f'library/{library_id}', None

    @property
    @get_json
    def settings(self) -> dict:
        return 'user/settings', None

    @property
    @get_json
    def who_am_i(self) -> dict:
        return 'auth/whoami', None

    @property
    @get_json
    def banner(self) -> dict:
        return 'dashboard/banner', None

    @property
    @get_json
    def dashboard(self) -> dict:
        return 'dashboard', None

    @get_json
    def tmdb_search(self, query: str, media_type: str, year: int = None) -> List[dict]:
        if _is_invalid_choice(media_type, 'media_type', ['movie', 'tv']):
            raise Exception("Invalid media type")
        params = build_optional_params(query=query, media_type=media_type, year=year)
        return 'tmdb_search', params

    @get_json
    def search(self, query: str) -> List[dict]:
        return 'search', {"query": query}

    @property
    @get_json
    def file_browser(self, path: str = None) -> dict:
        if path:
            return f'filebrowser/{path}', None
        return 'filebrowser', None

    @get_json
    def get_tv_season(self, tv_id: int, season_number: int) -> dict:
        return f'tv/{tv_id}/season/{season_number}', None

    """
    @patch_bool
    def update_tv_season(self, tv_id: int, season_number: int, **kwargs) -> bool:
        return f'tv/{tv_id}/season/{season_number}', {'data': kwargs}
    """

    @delete_bool
    def delete_tv_season(self, tv_id: int, season_number: int) -> bool:
        return f'tv/{tv_id}/season/{season_number}', None

    @get_json
    def get_tv_episode(self, episode_id: int) -> dict:
        return f'episode/{episode_id}', None

    """
    @patch_bool
    def update_tv_episode(self, episode_id: int, **kwargs) -> bool:
        return f'episode/{episode_id}', {'data': kwargs}
    """

    @delete_bool
    def delete_tv_episode(self, episode_id: int) -> bool:
        return f'episode/{episode_id}', None

    @get_json
    def get_virtual_manifest(self, stream_id: str, manifest_guid: str = None) -> dict:
        params = build_optional_params(manifest_guid=manifest_guid)
        return f'stream/{stream_id}/manifest', params

    def get_manifest(self, stream_id: str, start_num: int, should_kill: bool = False, includes: List[int] = None) -> \
            Optional[str]:
        includes = int_list_to_string(includes)
        params = build_optional_params(start_num=start_num, should_kill=should_kill, includes=includes)
        res = self._get(command=f'stream/{stream_id}/manifest.mpd', params=params)
        if res:
            return res.text
        return None
