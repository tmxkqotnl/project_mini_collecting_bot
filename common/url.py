from typing import Optional, Tuple


class URL:
    __url: Optional[str]
    __params: dict[str, str]

    def __init__(self, url: Optional[str]):
        if url is not None:
            self.__url, self.__params = self.__parse_url(url)
        else:
            self.__url = None
            self.__params = {}

    def get_url(self) -> Optional[str]:
        return self.__url

    def set_url(self, url: str):
        __url, __params = self.__parse_url(url)

    def get_params(self) -> dict[str, str]:
        return self.__params

    def set_params(self, params: dict[str, str]):
        if type(params) is not dict:
            raise TypeError("params must be dict[str,str]")
        if self.__url is None:
            raise ValueError("Cannot set params without url address")

        for k, v in params.items():
            self.__params[k] = v

    def __parse_url(self, full_address: str) -> Tuple[str, dict[str, str]]:
        if full_address.find("?") == -1:
            return full_address, {}

        base_url, params = full_address.split("?")
        params = {i: j for i, j in [i for i in params.split("&")]}

        return base_url, params

    def get_full_url(self) -> str:
        if self.__url is None:
            raise ValueError("url is None")

        params_joined = "&".join(
            ["{}={}".format(k, v) for k, v in self.get_params().items()]
        )
        return "?".join([self.__url, params_joined])
