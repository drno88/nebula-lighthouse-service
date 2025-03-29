import subprocess
from typing import Iterator, Tuple

import yaml
import os
from pathlib import Path

SNAP = Path(os.environ['SNAP'])
CONFIG_PATH = Path(os.environ['SNAP_COMMON']) / 'config'


def create_config(ca: str, cert: str, key: str, port: int) -> str:
    cfg = dict(
        lighthouse=dict(am_lighthouse=True),
        tun=dict(disabled=True),
        punchy=dict(
            punch=True,
            respond=True,
        ),
        relay=dict(
            am_relay=True
        ),
        listen=dict(port=int(port)),
        pki=dict(
            ca=ca,
            cert=cert,
            key=key,
        ),
    )

    return yaml.safe_dump(cfg)


def test_config(yaml_config: str):
    subprocess.run(f'{SNAP}/bin/nebula -test -config /dev/stdin'.split(),
                   check=True,
                   input=yaml_config.encode())


def read_config(path: Path) -> Tuple[str, str, str, int]:
    contents = path.read_text()
    cfg = yaml.safe_load(contents)

    pki = cfg.get('pki', {})
    ca_crt = pki['ca']
    host_crt = pki['cert']
    host_key = pki['key']
    port = cfg.get('listen', {})['port']

    return ca_crt, host_crt, host_key, port


def get_existing_configs() -> Iterator[Path]:
    return CONFIG_PATH.glob('lighthouse-*.yaml')


def get_config_path(lighthouse_index: int) -> Path:
    return CONFIG_PATH / f'lighthouse-{int(lighthouse_index)}.yaml'
