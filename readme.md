# ovos-PHAL-plugin - system

handle bus events to interact with the OS

```python
self.bus.on("system.ntp.sync", self.handle_ntp_sync_request)
self.bus.on("system.ssh.enable", self.handle_ssh_enable_request)
self.bus.on("system.ssh.disable", self.handle_ssh_disable_request)
self.bus.on("system.reboot", self.handle_reboot_request)
self.bus.on("system.shutdown", self.handle_shutdown_request)
```