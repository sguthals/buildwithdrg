import yaml
import os

FILENAME = "config/config.yaml"
umask = os.umask(0)
try:
    fd = os.open(FILENAME, os.O_RDONLY, 0o400)
finally:
    os.umask(umask)

with os.fdopen(fd, "r") as ymlfile:
    config = yaml.full_load(ymlfile)