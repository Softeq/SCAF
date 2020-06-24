from common.rest_qa_api.base_endpoint import BaseRequestModel, BaseResponseModel, endpoint_factory
from common.rest_qa_api.rest_utils import SKIP, scaf_dataclass
from common.scaf import raw_config


# TODO - find solution to set dataclass fields properly after initialization
def query_builder(city, token):
    return f'q={city}&appid={token}'


@scaf_dataclass
class DailyWeatherEndpointBuilder:
    @scaf_dataclass
    class _DailyWeatherRequestModel(BaseRequestModel):
        resource: str = 'weather'
        headers = {"Accept": "application/json"}
        post_data = None
        put_data = None
        patch_data = None
        delete_data = None
        params = None
        allowed_methods = ("get",)

    @scaf_dataclass
    class _DailyWeatherResponseModel(BaseResponseModel):
        status_code = 200
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        get_data = {"coord": {"lon": SKIP, "lat": SKIP},
                    "weather": [{"id": SKIP, "main": SKIP, "description": SKIP, "icon": SKIP}],
                    "base": "stations",
                    "main": {"temp": SKIP, "feels_like": SKIP, "temp_min": SKIP, "temp_max": SKIP, "pressure": SKIP,
                             "humidity": SKIP}, "visibility": SKIP, "wind": {"speed": SKIP},
                    "clouds": {"all": SKIP}, "dt": SKIP,
                    "sys": {"type": SKIP, "id": SKIP, "country": SKIP, "sunrise": SKIP, "sunset": SKIP},
                    "timezone": SKIP, "id": SKIP, "name": SKIP, "cod": SKIP}
        post_data = None
        put_data = None
        delete_data = None
        patch_data = None
        error_data = None
        custom_checkers = []

    endpoint = endpoint_factory(raw_config.api_settings.api_url, "DailyWeatherEndpoint",
                                _DailyWeatherRequestModel, _DailyWeatherResponseModel)

    def get_weather_details(self, city, token):
        self.endpoint.request_model.params = query_builder(city, token)
        result = self.endpoint.get()
        return result.get_data
