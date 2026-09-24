import httpx


class ApiError(Exception):
    def __init__(self, status_code: int | None, detail: str):
        self.status_code = status_code
        self.detail = detail
        label = status_code if status_code is not None else "connection error"
        super().__init__(f"[{label}] {detail}")


class ApiClient:
    def __init__(self, base_url: str):
        self._client = httpx.Client(base_url=base_url.rstrip("/"), timeout=10.0)

    def close(self):
        self._client.close()

    def _request(self, method: str, path: str, json=None, headers=None):
        try:
            response = self._client.request(method, path, json=json, headers=headers)
        except httpx.RequestError as exc:
            raise ApiError(None, f"Could not reach API ({exc})") from exc

        if response.status_code >= 400:
            detail = response.text
            try:
                body = response.json()
                if isinstance(body, dict) and "detail" in body:
                    detail = body["detail"]
            except ValueError:
                pass
            raise ApiError(response.status_code, detail)

        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    def get(self, path: str, headers=None):
        return self._request("GET", path, headers=headers)

    def post(self, path: str, json, headers=None):
        return self._request("POST", path, json=json, headers=headers)

    def put(self, path: str, json, headers=None):
        return self._request("PUT", path, json=json, headers=headers)

    def delete(self, path: str, headers=None):
        return self._request("DELETE", path, headers=headers)
