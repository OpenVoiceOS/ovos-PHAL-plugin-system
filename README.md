# ovos-PHAL-plugin-system

This PHAL plugin gives OpenVoiceOS commands to control the host system. It handles NTP sync, SSH, reboot, shutdown, factory reset, and language configuration through bus events. The plugin does not yet define a dbus interface.

## Install

```bash
pip install ovos-PHAL-plugin-system
```

## Config

This plugin can run as an admin plugin. An admin plugin runs as root. To enable it, add this to `mycroft.conf`:

```javascript
{
"PHAL": {
    "admin": {
        "ovos-PHAL-plugin-system": {"enabled": true}
    }
}
}
```

If you omit this config, the plugin runs as the regular user. In that case, you need a polkit policy that allows `systemctl` without `sudo`. This policy is not yet implemented.

## Usage

The plugin listens for these bus events and reacts to each one:

```python
self.bus.on("system.ntp.sync", self.handle_ntp_sync_request)
self.bus.on("system.ssh.status", self.handle_ssh_status)
self.bus.on("system.ssh.enable", self.handle_ssh_enable_request)
self.bus.on("system.ssh.disable", self.handle_ssh_disable_request)
self.bus.on("system.reboot", self.handle_reboot_request)
self.bus.on("system.shutdown", self.handle_shutdown_request)
self.bus.on("system.factory.reset", self.handle_factory_reset_request)
self.bus.on("system.factory.reset.register", self.handle_reset_register)
self.bus.on("system.configure.language", self.handle_configure_language_request)
self.bus.on("system.mycroft.service.restart", self.handle_mycroft_restart_request)
```

## Related projects

- [OpenVoiceOS/ovos-PHAL](https://github.com/OpenVoiceOS/ovos-PHAL): the hardware abstraction layer that loads this plugin
- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager): plugin loader and admin plugin support

## License

Apache-2.0
