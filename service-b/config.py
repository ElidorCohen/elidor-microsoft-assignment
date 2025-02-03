from dataclasses import dataclass


@dataclass
class Config:
    base_url: str = '0.0.0.0'
    base_port: int = 80
