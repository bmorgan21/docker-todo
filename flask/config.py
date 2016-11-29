from ct_core_api.api.app import config

SECRET_KEY = 'We Love Our TODO List'
SECRET_COOKIE_NAME = 'ts12d'
SECRET_COOKIE_MAX_AGE = 15 * 60
SECRET_COOKIE_SECURE = False

LIMIT_TO_ONE_SESSION = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

SWAGGER_UI_JSONEDITOR = False

# TODO: Consider disabling `ct-core-api` auth module by default as it introduces oauth2 libs
# Exclude the `ct-core-api` auth module
ENABLED_MODULES = filter(lambda x: x not in {'auth'}, config.ProductionConfig.AVAILABLE_MODULES)
ENABLED_EXTENSIONS = filter(lambda x: x not in {'login_manager_ext', 'oauth2_ext'}, config.ProductionConfig.AVAILABLE_EXTENSIONS)
