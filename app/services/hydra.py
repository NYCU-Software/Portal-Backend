import requests


class HydraService:
    def __init__(self, public_url, admin_url, timeout=5):
        self.public_url = public_url
        self.admin_url = admin_url
        self.timeout = timeout

    def get_login_request(self, login_challenge):
        r = requests.get(
            f"{self.admin_url}/oauth2/auth/requests/login",
            params={"login_challenge": login_challenge},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def accept_login_request(self, login_challenge, user_info):
        body = {
            "subject": str(user_info["subject"]),
            "remember": True,
            "remember_for": 3600,
        }
        r = requests.put(
            f"{self.admin_url}/oauth2/auth/requests/login/accept",
            params={"login_challenge": login_challenge},
            json=body,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()["redirect_to"]

    def reject_login_request(self, login_challenge, reason):
        data = {"error": "access_denied", "error_description": reason}
        r = requests.put(
            f"{self.admin_url}/oauth2/auth/requests/login/reject",
            params={"login_challenge": login_challenge},
            json=data,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()["redirect_to"]

    def get_consent_request(self, consent_challenge):
        r = requests.get(
            f"{self.admin_url}/oauth2/auth/requests/consent",
            params={"consent_challenge": consent_challenge},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def accept_consent_request(self, consent_challenge, user_info):
        r = requests.put(
            f"{self.admin_url}/oauth2/auth/requests/consent/accept",
            params={"consent_challenge": consent_challenge},
            json=user_info,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()["redirect_to"]

    def reject_consent_request(self, consent_challenge, reason):
        data = {"error": "access_denied", "error_description": reason}
        r = requests.put(
            f"{self.admin_url}/oauth2/auth/requests/consent/reject",
            params={"consent_challenge": consent_challenge},
            json=data,
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()["redirect_to"]

    def exchange_code_for_token(self, code, redirect_uri, client_id, client_secret):
        r = requests.post(
            f"{self.public_url}/oauth2/token",
            auth=(client_id, client_secret),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            },
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def get_userinfo(self, access_token):
        r = requests.get(
            f"{self.public_url}/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=self.timeout,
        )
        r.raise_for_status()
        return r.json()

    def create_client(self, data):
        url = f"{self.admin_url}/admin/clients"
        headers = {"Content-Type": "application/json"}
        r = requests.post(url, json=data, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def update_client(self, client_id, data):
        url = f"{self.admin_url}/admin/clients/{client_id}"
        headers = {"Content-Type": "application/json"}
        r = requests.put(url, json=data, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_client(self, client_id):
        url = f"{self.admin_url}/admin/clients/{client_id}"
        headers = {"Content-Type": "application/json"}
        r = requests.get(url, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def delete_client(self, client_id):
        url = f"{self.admin_url}/admin/clients/{client_id}"
        headers = {"Content-Type": "application/json"}
        r = requests.delete(url, headers=headers, timeout=self.timeout)
        r.raise_for_status()

    def get_clients(self):
        url = f"{self.admin_url}/admin/clients"
        headers = {"Content-Type": "application/json"}
        r = requests.get(url, headers=headers, timeout=self.timeout)
        r.raise_for_status()
        return r.json()
