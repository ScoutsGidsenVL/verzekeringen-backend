from django.conf import settings


known_admin_scouts_groups = ["X0001G", "X0002G", "X0015G", "X1027G"]


class SettingsHelper:
    """Convenience class with static methods to easily distinguish what settings are required for dependent packages."""

    @staticmethod
    def get_auth_user_model(default_value=None):
        return getattr(settings, "AUTH_USER_MODEL", default_value)

    @staticmethod
    def get_authorization_roles_config_package(default_value=None):
        return getattr(settings, "AUTHORIZATION_ROLES_CONFIG_PACKAGE", default_value)

    @staticmethod
    def get_authorization_roles_config_yaml(default_value=None):
        return getattr(settings, "AUTHORIZATION_ROLES_CONFIG_YAML", default_value)

    @staticmethod
    def get_oidc_op_token_endpoint(default_value=None):
        return getattr(settings, "OIDC_OP_TOKEN_ENDPOINT", default_value)

    @staticmethod
    def get_oidc_op_user_endpoint(default_value=None):
        return getattr(settings, "OIDC_OP_USER_ENDPOINT", default_value)

    @staticmethod
    def get_oidc_rp_client_id(default_value=None):
        return getattr(settings, "OIDC_RP_CLIENT_ID", default_value)

    @staticmethod
    def get_oidc_rp_client_secret(default_value=None):
        return getattr(settings, "OIDC_RP_CLIENT_SECRET", default_value)

    @staticmethod
    def get_oidc_verify_ssl(default_value=None):
        return getattr(settings, "OIDC_VERIFY_SSL", default_value)

    @staticmethod
    def get_oidc_timeout(default_value=None):
        return getattr(settings, "OIDC_TIMEOUT", default_value)

    @staticmethod
    def get_oidc_proxy(default_value=None):
        return getattr(settings, "OIDC_PROXY", default_value)

    @staticmethod
    def get_group_admin_base_url(default_value=None):
        return getattr(settings, "GROUP_ADMIN_BASE_URL", default_value)

    @staticmethod
    def get_group_admin_allowed_calls_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_ALLOWED_CALLS_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_profile_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_PROFILE_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_search_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_detail_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_group_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_GROUP_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_functions_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_FUNCTIONS_ENDPOINT", default_value)

    @staticmethod
    def get_group_admin_member_list_endpoint(default_value=None):
        return getattr(settings, "GROUP_ADMIN_MEMBER_LIST_ENDPOINT", default_value)

    @staticmethod
    def get_known_admin_groups(default_value=None) -> list:
        try:
            return settings.KNOWN_ADMIN_GROUPS
        except Exception:
            pass

        return ["X0001G", "X0002G", "X0015G", "X1027G"]
