from .server import Client, CLIENT_AUTHORIZED
from .extension import Extension
import json


def client_function(data: dict, client: Client,
                    extension: dict[str, Extension]) -> None:
    """Client function."""
    if data["version"] in CLIENT_AUTHORIZED:
        variable = {}
        for key, value in extension.items():
            for var in value.variables:
                variable[f"{key}.{var}"] = value.variables[var]
        client.send(json.dumps({"ok": True,
                                "variables": variable}).encode())
    else:
        client.send(
            json.dumps({"ok": False,
                        "error": "Client version not supported"}).encode())
        client.close()
        return


def variable_function(data: dict, client: Client) -> None:
    """Variable function."""
    client.variables = data["variables"]
    client.send(json.dumps({"ok": True}).encode())
