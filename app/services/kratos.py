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

    def login(self, identifier, password):
        try:
            flow = self.api.create_native_login_flow()
        except ApiException as e:
            print("create_browser_login_flow error:", e.body)
            return None

        if not flow or not flow.id:
            print("Flow is None or missing ID")
            return None

        body = {
            "method": "password",
            "identifier": identifier,
            "password": password,
        }

        try:
            res = self.api.update_login_flow(
                flow.id, update_login_flow_body=UpdateLoginFlowBody(body)
            )
            return getattr(res, "session_token", None)
        except ApiException as e:
            print("update_login_flow error:", e.body)
            return None

    def get_session_from_token(self, token):
        try:
            return self.api.to_session(x_session_token=token)
        except ApiException as e:
            print(e.body)
            return None

    def logout(self, token):
        perform_native_logout_body_instance = PerformNativeLogoutBody(
            session_token=token
        )
        self.api.perform_native_logout(perform_native_logout_body_instance)
