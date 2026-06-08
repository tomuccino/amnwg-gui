from vpn_controller import VPNController
from config_manager import ConfigManager

def main():
    config_manager = ConfigManager()
    controller = VPNController(config_manager)