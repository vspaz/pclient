from __future__ import annotations

from typing import Union, Dict, Tuple

import requests
import ujson
from urllib3.util.retry import Retry

requests.models.complexjson = ujson


class PyClient:
    def __init__(self, config: Dict[str, dict]) -> None:
        self._validate_config(config=config)
        self._session: requests.Session = requests.Session()
        http_config: dict = config['http']
        port: Union[str, int] = str(http_config.get('port', ''))

        self._session.mount(
            prefix=f"{http_config['host']}" + f":{port}/" if port else '/',
            adapter=self._retry_on(config=http_config.get('retries', {})),
        )
        tls_certificates: dict = config.get('tls', {})
        if tls_certificates:
            self._session.verify = tls_certificates['ca_path']
            self._session.cert = (
                tls_certificates['client_certificate_path'],
                tls_certificates['client_key_path'],
            )
        timeouts: Dict[str, int] = http_config.get('timeouts', {})
        self._timeouts: tuple = (
            timeouts.get('connect', 5),
            timeouts.get('read', 10),
        )

    @staticmethod
    def _retry_on(config: dict) -> requests.adapters.HTTPAdapter:
        return requests.adapters.HTTPAdapter(
            max_retries=Retry(
                total=config.get('retries', 3),
                backoff_factor=config.get('backoff', 0.5),
                status_forcelist=config.get('on_errors', []),
            ),
        )

    def _request(self, url: str, method: str, **kwargs: dict) -> requests.Response:
        return self._session.request(
            method=method,
            url=url,
            timeout=kwargs.get('timeouts', self._timeouts),
            **kwargs,
        )

    @staticmethod
    def _validate_config(config: Dict[str, dict]) -> dict:
        # TODO: add config validation.
        pass

    @staticmethod
    def get_http_client(config: Dict[str, dict]) -> PyClient:
        return PyClient(config=config)