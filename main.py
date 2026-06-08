from vpn_controller import VPNController
from config_manager import ConfigManager
from vpn_gui import VPNGUI
from pprint import pprint

def main():
    config_manager = ConfigManager()
    controller = VPNController(config_manager)
    app = VPNGUI()
    app.run()



if __name__ == '__main__':
    main()