import requests
from ory_kratos_client import Configuration, ApiClient, FrontendApi
from ory_kratos_client.exceptions import ApiException
from ory_kratos_client.models.update_login_flow_body import UpdateLoginFlowBody
from ory_kratos_client.models.perform_native_logout_body import PerformNativeLogoutBody


class KratosService:
    def __init__(self, public_url):
        configuration = Configuration(host=public_url)
        api_client = ApiClient(configuration)
        self.api = FrontendApi(api_client)

    def verify(self, session_token):
        try:
            resp = self.api.to_session(cookie=f"ory_kratos_session={session_token}")
            print(resp.identity)
            return resp.identity
        except ApiException as e:
            if getattr(e, "status", None) == 401:
                return None
            raise
