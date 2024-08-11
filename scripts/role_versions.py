#!/usr/bin/env python3

"""
    Check role versions.

"""

from ast import literal_eval as eval_literal
import sys
import subprocess
import json

def get_role_version(role_name: str) -> str:
    """Use ansible-galaxy to discover version of a role"""
    cmd_args = ['ansible-galaxy', 'role', 'list', role_name]
    result = subprocess.run(cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise Exception("ansible-galaxy command failed")

    lines = result.stdout.splitlines()
    if lines == []:
        return None

    assert len(lines) == 2, f"Wrong output: {lines!r}"

    last_line = lines[-1]

    ret_name, _, ret_version = last_line.partition(', ')

    return ret_version

def get_roles_versions(roles: 'list[str]') -> 'dict[str, str]':
    """Map list of roles into versions"""
    return {role: get_role_version(role) for role in roles}

def main():
    """Main()"""
    roles_stdin = sys.stdin.read()
    roles = eval_literal(roles_stdin)

    assert isinstance(roles, list), f"Incorrect input: {roles_stdin}"
    assert all(isinstance(r, str) for r in roles), f"Incorrect input: {roles_stdin}"

    roles_versions = get_roles_versions(roles)

    print(json.dumps(roles_versions))

if __name__ == '__main__':
    main()


