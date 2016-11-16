
from pbr import version as pbr_version

VSM_VENDOR = "Intel"
VSM_PRODUCT = "Intel"
VSM_PACKAGE = None

loaded = False
version_info = pbr_version.VersionInfo('vsm')
version_string = version_info.version_string
