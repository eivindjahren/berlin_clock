from pkg_resources import DistributionNotFound, get_distribution

__author__ = """Eivind Jahren"""
__email__ = "eivind.jahren@webstep.no"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = "0.0.0"
