from ct_core_api.api.app import config

SECRET_KEY = 'We Love Our TODO List'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# TODO: Consider disabling `ct-core-api` auth module by default as it introduces oauth2 libs
# Exclude the `ct-core-api` auth module
ENABLED_MODULES = filter(lambda x: x not in {'auth'}, config.ProductionConfig.AVAILABLE_MODULES)
