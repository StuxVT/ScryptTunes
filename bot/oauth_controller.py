from urllib.parse import urlencode

import requests
from flask import Flask, request
import logging
import threading
import time
from ui.controllers.settings_controller import SettingsController


class OAuthConnector:
    def __init__(self, settings_controller: SettingsController):
        self.settings_controller = settings_controller
        self.config = settings_controller.config_model
        self.auth_url = "https://id.twitch.tv/oauth2/authorize"
        self.token_url = "https://id.twitch.tv/oauth2/token"
        self.validate_url = "https://id.twitch.tv/oauth2/validate"
        self.redirect_uri = "http://localhost:17563"
        self.scopes = ["chat:read", "chat:edit", "channel:read:redemptions", "channel:bot"]
        self.auth_successful = False

    def start_auth_flow(self):
        app = Flask(__name__)

        @app.route('/')  # Change this to root route
        def callback():
            error = request.args.get('error')
            error_description = request.args.get('error_description')

            if error:
                print(f"Authentication error: {error}")
                print(f"Error description: {error_description}")
                return f"Authentication failed: {error_description}"

            code = request.args.get('code')
            if code:
                token_data = self.exchange_code_for_token(code)
                if token_data:
                    self.settings_controller.update_oauth_tokens(
                        token_data['access_token'],
                        token_data['refresh_token']
                    )
                    self.auth_successful = True
                    return "Authentication successful! You can close this window."
            return "Authentication failed."

        def run_flask():
            app.run(port=17563)

        flask_thread = threading.Thread(target=run_flask)
        flask_thread.start()

        auth_params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes)
        }
        auth_url = f"{self.auth_url}?{urlencode(auth_params)}"

        logging.warning(
            "\n\n*** WARNING ***\nPlease open the following URL in your browser to authenticate:\n%s\n****************\n\n",
            auth_url)

        timeout = 300  # 5 minutes timeout
        start_time = time.time()
        while not self.auth_successful and time.time() - start_time < timeout:
            time.sleep(1)

        if not self.auth_successful:
            raise Exception("Authentication timed out or failed.")

    def exchange_code_for_token(self, code):
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            return response.json()
        return None

    def validate_token(self):
        headers = {
            "Authorization": f"OAuth {self.config.token}"
        }
        response = requests.get(self.validate_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return all(scope in data.get("scopes", []) for scope in self.scopes)
        return False

    def refresh_token(self):
        if not self.config.refresh_token:
            print("No refresh token available. Starting new auth flow.")
            self.start_auth_flow()
            return self.validate_token()

        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.config.refresh_token
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            new_token_data = response.json()
            self.settings_controller.update_oauth_tokens(
                new_token_data["access_token"],
                new_token_data["refresh_token"]
            )
            return True
        return False

    def ensure_valid_token(self):
        if not self.validate_token():
            if self.refresh_token():
                if self.validate_token():
                    return True
                else:
                    print("Refreshed token is still invalid. Starting new auth flow.")
                    self.start_auth_flow()
            else:
                print("Failed to refresh token. Starting new auth flow.")
                self.start_auth_flow()
        return True


def initialize_oauth(settings_controller: SettingsController):
    connector = OAuthConnector(settings_controller)
    connector.ensure_valid_token()
    return connector