from ovos_plugin_manager.phal import PHALPlugin
from ovos_utils.system import system_shutdown, system_reboot, ssh_enable, ssh_disable, ntp_sync, restart_mycroft_service


class SystemEventsValidator:
    @staticmethod
    def validate(config=None):
        """ this method is called before loading the plugin.
        If it returns False the plugin is not loaded.
        This allows a plugin to run platform checks"""
        return True


class SystemEvents(PHALPlugin):
    validator = SystemEventsValidator

    def __init__(self, bus=None, config=None):
        super().__init__(bus=bus, name="ovos-PHAL-plugin-system", config=config)
        self.bus.on("system.ntp.sync", self.handle_ntp_sync_request)
        self.bus.on("system.ssh.enable", self.handle_ssh_enable_request)
        self.bus.on("system.ssh.disable", self.handle_ssh_disable_request)
        self.bus.on("system.reboot", self.handle_reboot_request)
        self.bus.on("system.shutdown", self.handle_shutdown_request)
        self.bus.on("system.mycroft.service.restart",
                    self.handle_mycroft_restart_request)

    def handle_ssh_enable_request(self, message):
        ssh_enable()

    def handle_ssh_disable_request(self, message):
        ssh_disable()

    def handle_ntp_sync_request(self, message):
        ntp_sync()
        self.bus.emit(message.reply('system.ntp.sync.complete'))

    def handle_reboot_request(self, message):
        system_reboot()

    def handle_shutdown_request(self, message):
        system_shutdown()

    def handle_mycroft_restart_request(self, message):
        restart_mycroft_service()

    def shutdown(self):
        self.bus.remove("system.ntp.sync", self.handle_ntp_sync_request)
        self.bus.remove("system.ssh.enable", self.handle_ssh_enable_request)
        self.bus.remove("system.ssh.disable", self.handle_ssh_disable_request)
        self.bus.remove("system.reboot", self.handle_reboot_request)
        self.bus.remove("system.shutdown", self.handle_shutdown_request)
        super().shutdown()
