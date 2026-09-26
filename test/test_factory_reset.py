"""Tests for the factory-reset config wipe path.

These tests require an `ovos-config` release that ships `ASSISTANT_CONFIG`
(ovos-config#194). Against an older `ovos-config` the whole module fails to
import, so the module is skipped rather than failing.
"""
import importlib
import os
import unittest
from unittest.mock import MagicMock

XDG_ENV_VARS = ("XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME")


def _point_xdg_at_scratch(scratch_dir):
    for var, sub in zip(XDG_ENV_VARS, ("config", "data", "state", "cache")):
        path = os.path.join(scratch_dir, sub)
        os.makedirs(path, exist_ok=True)
        os.environ[var] = path
    # OLD_USER_CONFIG (pre-XDG layout) is derived from expanduser('~'), not
    # from the XDG_* vars, so HOME must also be redirected into the scratch
    # tree - never let this test touch the real home directory.
    home = os.path.join(scratch_dir, "home")
    os.makedirs(home, exist_ok=True)
    os.environ["HOME"] = home


class FakeBus:
    """Minimal bus double - no real connection, no real IO."""

    def on(self, *args, **kwargs):
        pass

    def once(self, *args, **kwargs):
        pass

    def remove(self, *args, **kwargs):
        pass

    def emit(self, *args, **kwargs):
        pass


def _load_plugin_module():
    """Import the plugin module against a scratch XDG tree.

    Returns None (and the test using it should skip) if the installed
    ovos-config predates ASSISTANT_CONFIG (ovos-config#194).
    """
    import tempfile
    scratch = tempfile.mkdtemp(prefix="phal-system-reset-test-")
    _point_xdg_at_scratch(scratch)
    try:
        import ovos_PHAL_plugin_system as mod
        importlib.reload(mod)
        return mod, scratch
    except ImportError:
        return None, scratch


class TestFactoryResetConfigWipe(unittest.TestCase):
    def setUp(self):
        self._saved_env = {v: os.environ.get(v) for v in (*XDG_ENV_VARS, "HOME")}
        self.mod, self.scratch = _load_plugin_module()
        if self.mod is None:
            self.skipTest("installed ovos-config lacks ASSISTANT_CONFIG "
                          "(requires ovos-config#194+)")

    def tearDown(self):
        for var, value in self._saved_env.items():
            if value is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = value

    def _make_plugin(self):
        plugin = self.mod.SystemEventsPlugin.__new__(self.mod.SystemEventsPlugin)
        plugin.bus = FakeBus()
        plugin.config = {}
        plugin.factory_reset_plugs = []
        return plugin

    def _touch(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("{}")

    def _reset_message(self):
        from ovos_bus_client.message import Message
        return Message("system.factory.reset", {
            "wipe_cache": False,
            "wipe_data": False,
            "wipe_logs": False,
            "wipe_configs": True,
            "reset_hardware": False,
            "script": False,
            "reboot": False,
        })

    def test_removes_all_config_paths_when_present(self):
        from os.path import join, expanduser
        mod = self.mod
        old_user_config = join(expanduser('~'), '.' + mod.get_xdg_base(),
                               mod.get_config_filename())
        for p in (old_user_config, mod.USER_CONFIG, mod.ASSISTANT_CONFIG,
                 mod.WEB_CONFIG_CACHE):
            self._touch(p)

        plugin = self._make_plugin()
        plugin.handle_factory_reset_request(self._reset_message())

        for p in (old_user_config, mod.USER_CONFIG, mod.ASSISTANT_CONFIG,
                 mod.WEB_CONFIG_CACHE):
            self.assertFalse(os.path.isfile(p), f"expected {p} to be removed")

    def test_missing_config_paths_are_skipped_without_error(self):
        mod = self.mod
        # nothing created on disk - none of the paths exist
        plugin = self._make_plugin()
        # should not raise
        plugin.handle_factory_reset_request(self._reset_message())

    def test_wipe_configs_false_leaves_files_untouched(self):
        from os.path import join, expanduser
        mod = self.mod
        old_user_config = join(expanduser('~'), '.' + mod.get_xdg_base(),
                               mod.get_config_filename())
        for p in (old_user_config, mod.USER_CONFIG, mod.ASSISTANT_CONFIG,
                 mod.WEB_CONFIG_CACHE):
            self._touch(p)

        from ovos_bus_client.message import Message
        message = Message("system.factory.reset", {
            "wipe_cache": False,
            "wipe_data": False,
            "wipe_logs": False,
            "wipe_configs": False,
            "reset_hardware": False,
            "script": False,
            "reboot": False,
        })

        plugin = self._make_plugin()
        plugin.handle_factory_reset_request(message)

        for p in (old_user_config, mod.USER_CONFIG, mod.ASSISTANT_CONFIG,
                 mod.WEB_CONFIG_CACHE):
            self.assertTrue(os.path.isfile(p), f"expected {p} to survive")


if __name__ == "__main__":
    unittest.main()
