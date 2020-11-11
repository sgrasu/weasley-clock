import platform

debugging = "macOS" in platform.platform()
interval = 60 if debugging else 240


