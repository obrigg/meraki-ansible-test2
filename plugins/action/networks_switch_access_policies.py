#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
        AnsibleArgSpecValidator,
    )
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible.errors import AnsibleActionFail
from ansible_collections.cisco.meraki.plugins.plugin_utils.meraki import (
    MERAKI,
    meraki_argument_spec,
    meraki_compare_equality,
    get_dict_result,
)
from ansible_collections.cisco.meraki.plugins.plugin_utils.exceptions import (
    InconsistentParameters,
)

# Get common arguments specification
argument_spec = meraki_argument_spec()
# Add arguments specific for this module
argument_spec.update(dict(
    state=dict(type="str", default="present", choices=["present", "absent"]),
    name=dict(type="str"),
    radiusServers=dict(type="list"),
    radius=dict(type="dict"),
    guestPortBouncing=dict(type="bool"),
    radiusTestingEnabled=dict(type="bool"),
    radiusCoaSupportEnabled=dict(type="bool"),
    radiusAccountingEnabled=dict(type="bool"),
    radiusAccountingServers=dict(type="list"),
    radiusGroupAttribute=dict(type="str"),
    hostMode=dict(type="str"),
    accessPolicyType=dict(type="str"),
    increaseAccessSpeed=dict(type="bool"),
    guestVlanId=dict(type="int"),
    dot1x=dict(type="dict"),
    voiceVlanClients=dict(type="bool"),
    urlRedirectWalledGardenEnabled=dict(type="bool"),
    urlRedirectWalledGardenRanges=dict(type="list"),
    networkId=dict(type="str"),
    accessPolicyNumber=dict(type="str"),
))

required_if = [
    ("state", "present", ["accessPolicyNumber", "name", "networkId"], True),
    ("state", "absent", ["accessPolicyNumber", "name", "networkId"], True),
]
required_one_of = []
mutually_exclusive = []
required_together = []


class NetworksSwitchAccessPolicies(object):
    def __init__(self, params, meraki):
        self.meraki = meraki
        self.new_object = dict(
            name=params.get("name"),
            radiusServers=params.get("radiusServers"),
            radius=params.get("radius"),
            guestPortBouncing=params.get("guestPortBouncing"),
            radiusTestingEnabled=params.get("radiusTestingEnabled"),
            radiusCoaSupportEnabled=params.get("radiusCoaSupportEnabled"),
            radiusAccountingEnabled=params.get("radiusAccountingEnabled"),
            radiusAccountingServers=params.get("radiusAccountingServers"),
            radiusGroupAttribute=params.get("radiusGroupAttribute"),
            hostMode=params.get("hostMode"),
            accessPolicyType=params.get("accessPolicyType"),
            increaseAccessSpeed=params.get("increaseAccessSpeed"),
            guestVlanId=params.get("guestVlanId"),
            dot1x=params.get("dot1x"),
            voiceVlanClients=params.get("voiceVlanClients"),
            urlRedirectWalledGardenEnabled=params.get("urlRedirectWalledGardenEnabled"),
            urlRedirectWalledGardenRanges=params.get("urlRedirectWalledGardenRanges"),
            networkId=params.get("networkId"),
            accessPolicyNumber=params.get("accessPolicyNumber"),
        )

    def get_all_params(self, name=None, id=None):
        new_object_params = {}
        if self.new_object.get('networkId') is not None or self.new_object.get('network_id') is not None:
            new_object_params['networkId'] = self.new_object.get('networkId') or \
                self.new_object.get('network_id')
        return new_object_params

    def get_params_by_id(self, name=None, id=None):
        new_object_params = {}
        if self.new_object.get('networkId') is not None or self.new_object.get('network_id') is not None:
            new_object_params['networkId'] = self.new_object.get('networkId') or \
                self.new_object.get('network_id')
        if self.new_object.get('accessPolicyNumber') is not None or self.new_object.get('access_policy_number') is not None:
            new_object_params['accessPolicyNumber'] = self.new_object.get('accessPolicyNumber') or \
                self.new_object.get('access_policy_number')
        return new_object_params

    def create_params(self):
        new_object_params = {}
        #REVIEW {'name': {'type': 'str', 'description': 'Name of the access policy.'}, 'radiusServers': {'type': 'list', 'description': 'List of RADIUS servers to require connecting devices to authenticate against before granting network access.', 'elements': 'dict', 'suboptions': {'host': {'type': 'str', 'description': 'Public IP address of the RADIUS server.'}, 'port': {'type': 'int', 'description': 'UDP port that the RADIUS server listens on for access requests.'}, 'secret': {'type': 'str', 'description': 'RADIUS client shared secret.'}}}, 'radius': {'type': 'dict', 'suboptions': {'criticalAuth': {'type': 'dict', 'suboptions': {'dataVlanId': {'type': 'int', 'description': 'VLAN that clients who use data will be placed on when RADIUS authentication fails. Will be null if hostMode is Multi-Auth.'}, 'voiceVlanId': {'type': 'int', 'description': 'VLAN that clients who use voice will be placed on when RADIUS authentication fails. Will be null if hostMode is Multi-Auth.'}, 'suspendPortBounce': {'type': 'bool', 'description': 'Enable to suspend port bounce when RADIUS servers are unreachable.'}}, 'description': 'Critical auth settings for when authentication is rejected by the RADIUS server.'}, 'failedAuthVlanId': {'type': 'int', 'description': 'VLAN that clients will be placed on when RADIUS authentication fails. Will be null if hostMode is Multi-Auth.'}, 'reAuthenticationInterval': {'type': 'int', 'description': 'Re-authentication period in seconds. Will be null if hostMode is Multi-Auth.'}}, 'description': 'Object for RADIUS Settings.'}, 'guestPortBouncing': {'type': 'bool', 'description': 'If enabled, Meraki devices will periodically send access-request messages to these RADIUS servers.'}, 'radiusTestingEnabled': {'type': 'bool', 'description': 'If enabled, Meraki devices will periodically send access-request messages to these RADIUS servers.'}, 'radiusCoaSupportEnabled': {'type': 'bool', 'description': 'Change of authentication for RADIUS re-authentication and disconnection.'}, 'radiusAccountingEnabled': {'type': 'bool', 'description': 'Enable to send start, interim-update and stop messages to a configured RADIUS accounting server for tracking connected clients.'}, 'radiusAccountingServers': {'type': 'list', 'description': 'List of RADIUS accounting servers to require connecting devices to authenticate against before granting network access.', 'elements': 'dict', 'suboptions': {'host': {'type': 'str', 'description': 'Public IP address of the RADIUS accounting server.'}, 'port': {'type': 'int', 'description': 'UDP port that the RADIUS Accounting server listens on for access requests.'}, 'secret': {'type': 'str', 'description': 'RADIUS client shared secret.'}}}, 'radiusGroupAttribute': {'type': 'str', 'description': 'Acceptable values are `""` for None, or `"11"` for Group Policies ACL.'}, 'hostMode': {'type': 'str', 'description': 'Choose the Host Mode for the access policy.'}, 'accessPolicyType': {'type': 'str', 'description': "Access Type of the policy. Automatically 'Hybrid authentication' when hostMode is 'Multi-Domain'."}, 'increaseAccessSpeed': {'type': 'bool', 'description': "Enabling this option will make switches execute 802.1X and MAC-bypass authentication simultaneously so that clients authenticate faster. Only required when accessPolicyType is 'Hybrid Authentication."}, 'guestVlanId': {'type': 'int', 'description': 'ID for the guest VLAN allow unauthorized devices access to limited network resources.'}, 'dot1x': {'type': 'dict', 'suboptions': {'controlDirection': {'type': 'str', 'description': "Supports either 'both' or 'inbound'. Set to 'inbound' to allow unauthorized egress on the switchport. Set to 'both' to control both traffic directions with authorization. Defaults to 'both'."}}, 'description': '802.1x Settings.'}, 'voiceVlanClients': {'type': 'bool', 'description': "CDP/LLDP capable voice clients will be able to use this VLAN. Automatically true when hostMode is 'Multi-Domain'."}, 'urlRedirectWalledGardenEnabled': {'type': 'bool', 'description': 'Enable to restrict access for clients to a specific set of IP addresses or hostnames prior to authentication.'}, 'urlRedirectWalledGardenRanges': {'type': 'list', 'description': 'IP address ranges, in CIDR notation, to restrict access for clients to a specific set of IP addresses or hostnames prior to authentication.', 'elements': 'str'}, 'networkId': {'type': 'str', 'description': 'NetworkId path parameter. Network ID.'}}
        if self.new_object.get('name') is not None or self.new_object.get('name') is not None:
            new_object_params['name'] = self.new_object.get('name') or \
                self.new_object.get('name')
        if self.new_object.get('radiusServers') is not None or self.new_object.get('radius_servers') is not None:
            new_object_params['radiusServers'] = self.new_object.get('radiusServers') or \
                self.new_object.get('radius_servers')
        if self.new_object.get('radius') is not None or self.new_object.get('radius') is not None:
            new_object_params['radius'] = self.new_object.get('radius') or \
                self.new_object.get('radius')
        if self.new_object.get('guestPortBouncing') is not None or self.new_object.get('guest_port_bouncing') is not None:
            new_object_params['guestPortBouncing'] = self.new_object.get('guestPortBouncing')
        if self.new_object.get('radiusTestingEnabled') is not None or self.new_object.get('radius_testing_enabled') is not None:
            new_object_params['radiusTestingEnabled'] = self.new_object.get('radiusTestingEnabled')
        if self.new_object.get('radiusCoaSupportEnabled') is not None or self.new_object.get('radius_coa_support_enabled') is not None:
            new_object_params['radiusCoaSupportEnabled'] = self.new_object.get('radiusCoaSupportEnabled')
        if self.new_object.get('radiusAccountingEnabled') is not None or self.new_object.get('radius_accounting_enabled') is not None:
            new_object_params['radiusAccountingEnabled'] = self.new_object.get('radiusAccountingEnabled')
        if self.new_object.get('radiusAccountingServers') is not None or self.new_object.get('radius_accounting_servers') is not None:
            new_object_params['radiusAccountingServers'] = self.new_object.get('radiusAccountingServers') or \
                self.new_object.get('radius_accounting_servers')
        if self.new_object.get('radiusGroupAttribute') is not None or self.new_object.get('radius_group_attribute') is not None:
            new_object_params['radiusGroupAttribute'] = self.new_object.get('radiusGroupAttribute') or \
                self.new_object.get('radius_group_attribute')
        if self.new_object.get('hostMode') is not None or self.new_object.get('host_mode') is not None:
            new_object_params['hostMode'] = self.new_object.get('hostMode') or \
                self.new_object.get('host_mode')
        if self.new_object.get('accessPolicyType') is not None or self.new_object.get('access_policy_type') is not None:
            new_object_params['accessPolicyType'] = self.new_object.get('accessPolicyType') or \
                self.new_object.get('access_policy_type')
        if self.new_object.get('increaseAccessSpeed') is not None or self.new_object.get('increase_access_speed') is not None:
            new_object_params['increaseAccessSpeed'] = self.new_object.get('increaseAccessSpeed')
        if self.new_object.get('guestVlanId') is not None or self.new_object.get('guest_vlan_id') is not None:
            new_object_params['guestVlanId'] = self.new_object.get('guestVlanId') or \
                self.new_object.get('guest_vlan_id')
        if self.new_object.get('dot1x') is not None or self.new_object.get('dot1x') is not None:
            new_object_params['dot1x'] = self.new_object.get('dot1x') or \
                self.new_object.get('dot1x')
        if self.new_object.get('voiceVlanClients') is not None or self.new_object.get('voice_vlan_clients') is not None:
            new_object_params['voiceVlanClients'] = self.new_object.get('voiceVlanClients')
        if self.new_object.get('urlRedirectWalledGardenEnabled') is not None or self.new_object.get('url_redirect_walled_garden_enabled') is not None:
            new_object_params['urlRedirectWalledGardenEnabled'] = self.new_object.get('urlRedirectWalledGardenEnabled')
        if self.new_object.get('urlRedirectWalledGardenRanges') is not None or self.new_object.get('url_redirect_walled_garden_ranges') is not None:
            new_object_params['urlRedirectWalledGardenRanges'] = self.new_object.get('urlRedirectWalledGardenRanges') or \
                self.new_object.get('url_redirect_walled_garden_ranges')
        if self.new_object.get('networkId') is not None or self.new_object.get('network_id') is not None:
            new_object_params['networkId'] = self.new_object.get('networkId') or \
                self.new_object.get('network_id')
        return new_object_params

    def delete_by_id_params(self):
        new_object_params = {}
        if self.new_object.get('networkId') is not None or self.new_object.get('network_id') is not None:
            new_object_params['networkId'] = self.new_object.get('networkId') or \
                self.new_object.get('network_id')
        if self.new_object.get('accessPolicyNumber') is not None or self.new_object.get('access_policy_number') is not None:
            new_object_params['accessPolicyNumber'] = self.new_object.get('accessPolicyNumber') or \
                self.new_object.get('access_policy_number')
        return new_object_params

    def update_by_id_params(self):
        new_object_params = {}
        if self.new_object.get('name') is not None or self.new_object.get('name') is not None:
            new_object_params['name'] = self.new_object.get('name') or \
                self.new_object.get('name')
        if self.new_object.get('radiusServers') is not None or self.new_object.get('radius_servers') is not None:
            new_object_params['radiusServers'] = self.new_object.get('radiusServers') or \
                self.new_object.get('radius_servers')
        if self.new_object.get('radius') is not None or self.new_object.get('radius') is not None:
            new_object_params['radius'] = self.new_object.get('radius') or \
                self.new_object.get('radius')
        if self.new_object.get('guestPortBouncing') is not None or self.new_object.get('guest_port_bouncing') is not None:
            new_object_params['guestPortBouncing'] = self.new_object.get('guestPortBouncing')
        if self.new_object.get('radiusTestingEnabled') is not None or self.new_object.get('radius_testing_enabled') is not None:
            new_object_params['radiusTestingEnabled'] = self.new_object.get('radiusTestingEnabled')
        if self.new_object.get('radiusCoaSupportEnabled') is not None or self.new_object.get('radius_coa_support_enabled') is not None:
            new_object_params['radiusCoaSupportEnabled'] = self.new_object.get('radiusCoaSupportEnabled')
        if self.new_object.get('radiusAccountingEnabled') is not None or self.new_object.get('radius_accounting_enabled') is not None:
            new_object_params['radiusAccountingEnabled'] = self.new_object.get('radiusAccountingEnabled')
        if self.new_object.get('radiusAccountingServers') is not None or self.new_object.get('radius_accounting_servers') is not None:
            new_object_params['radiusAccountingServers'] = self.new_object.get('radiusAccountingServers') or \
                self.new_object.get('radius_accounting_servers')
        if self.new_object.get('radiusGroupAttribute') is not None or self.new_object.get('radius_group_attribute') is not None:
            new_object_params['radiusGroupAttribute'] = self.new_object.get('radiusGroupAttribute') or \
                self.new_object.get('radius_group_attribute')
        if self.new_object.get('hostMode') is not None or self.new_object.get('host_mode') is not None:
            new_object_params['hostMode'] = self.new_object.get('hostMode') or \
                self.new_object.get('host_mode')
        if self.new_object.get('accessPolicyType') is not None or self.new_object.get('access_policy_type') is not None:
            new_object_params['accessPolicyType'] = self.new_object.get('accessPolicyType') or \
                self.new_object.get('access_policy_type')
        if self.new_object.get('increaseAccessSpeed') is not None or self.new_object.get('increase_access_speed') is not None:
            new_object_params['increaseAccessSpeed'] = self.new_object.get('increaseAccessSpeed')
        if self.new_object.get('guestVlanId') is not None or self.new_object.get('guest_vlan_id') is not None:
            new_object_params['guestVlanId'] = self.new_object.get('guestVlanId') or \
                self.new_object.get('guest_vlan_id')
        if self.new_object.get('dot1x') is not None or self.new_object.get('dot1x') is not None:
            new_object_params['dot1x'] = self.new_object.get('dot1x') or \
                self.new_object.get('dot1x')
        if self.new_object.get('voiceVlanClients') is not None or self.new_object.get('voice_vlan_clients') is not None:
            new_object_params['voiceVlanClients'] = self.new_object.get('voiceVlanClients')
        if self.new_object.get('urlRedirectWalledGardenEnabled') is not None or self.new_object.get('url_redirect_walled_garden_enabled') is not None:
            new_object_params['urlRedirectWalledGardenEnabled'] = self.new_object.get('urlRedirectWalledGardenEnabled')
        if self.new_object.get('urlRedirectWalledGardenRanges') is not None or self.new_object.get('url_redirect_walled_garden_ranges') is not None:
            new_object_params['urlRedirectWalledGardenRanges'] = self.new_object.get('urlRedirectWalledGardenRanges') or \
                self.new_object.get('url_redirect_walled_garden_ranges')
        if self.new_object.get('networkId') is not None or self.new_object.get('network_id') is not None:
            new_object_params['networkId'] = self.new_object.get('networkId') or \
                self.new_object.get('network_id')
        if self.new_object.get('accessPolicyNumber') is not None or self.new_object.get('access_policy_number') is not None:
            new_object_params['accessPolicyNumber'] = self.new_object.get('accessPolicyNumber') or \
                self.new_object.get('access_policy_number')
        return new_object_params

    def get_object_by_name(self, name):
        result = None
        # NOTE: Does not have a get by name method or it is in another action
        try:
            items = self.meraki.exec_meraki(
                family="switch",
                function="getNetworkSwitchAccessPolicies",
                params=self.get_all_params(name=name),
            )
            if isinstance(items, dict):
                if 'response' in items:
                    items = items.get('response')
            result = get_dict_result(items, 'name', name)
            if result == None:
                result = items
        except Exception as e:
            print("Error: ", e)
            result = None
        return result

    def get_object_by_id(self, id):
        result = None
        try:
            items = self.meraki.exec_meraki(
                family="switch",
                function="getNetworkSwitchAccessPolicy",
                params=self.get_params_by_id()
            )
            if isinstance(items, dict):
                if 'response' in items:
                    items = items.get('response')
            result = get_dict_result(items, 'accessPolicyNumber', id)
        except Exception as e:
            print("Error: ", e)
            result = None
        return result

    def exists(self):
        id_exists = False
        name_exists = False
        prev_obj = None
        o_id = self.new_object.get("id")
        o_id = o_id or self.new_object.get(
            "access_policy_number") or self.new_object.get("accessPolicyNumber")
        name = self.new_object.get("name")
        if o_id:
            prev_obj = self.get_object_by_id(o_id)
            id_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if not id_exists and name:
            prev_obj = self.get_object_by_name(name)
            name_exists = prev_obj is not None and isinstance(prev_obj, dict)
        if name_exists:
            _id = prev_obj.get("id")
            _id = _id or prev_obj.get("accessPolicyNumber")
            if id_exists and name_exists and o_id != _id:
                raise InconsistentParameters(
                    "The 'id' and 'name' params don't refer to the same object")
            if _id:
                self.new_object.update(dict(id=_id))
                self.new_object.update(dict(accessPolicyNumber=_id))
            if _id:
                prev_obj = self.get_object_by_id(_id)
        it_exists = prev_obj is not None and isinstance(prev_obj, dict)
        return (it_exists, prev_obj)

    def requires_update(self, current_obj):
        requested_obj = self.new_object

        obj_params = [
            ("name", "name"),
            ("radiusServers", "radiusServers"),
            ("radius", "radius"),
            ("guestPortBouncing", "guestPortBouncing"),
            ("radiusTestingEnabled", "radiusTestingEnabled"),
            ("radiusCoaSupportEnabled", "radiusCoaSupportEnabled"),
            ("radiusAccountingEnabled", "radiusAccountingEnabled"),
            ("radiusAccountingServers", "radiusAccountingServers"),
            ("radiusGroupAttribute", "radiusGroupAttribute"),
            ("hostMode", "hostMode"),
            ("accessPolicyType", "accessPolicyType"),
            ("increaseAccessSpeed", "increaseAccessSpeed"),
            ("guestVlanId", "guestVlanId"),
            ("dot1x", "dot1x"),
            ("voiceVlanClients", "voiceVlanClients"),
            ("urlRedirectWalledGardenEnabled", "urlRedirectWalledGardenEnabled"),
            ("urlRedirectWalledGardenRanges", "urlRedirectWalledGardenRanges"),
            ("networkId", "networkId"),
            ("accessPolicyNumber", "accessPolicyNumber"),
        ]
        # Method 1. Params present in request (Ansible) obj are the same as the current (DNAC) params
        # If any does not have eq params, it requires update
        return any(not meraki_compare_equality(current_obj.get(meraki_param),
                                               requested_obj.get(ansible_param))
                   for (meraki_param, ansible_param) in obj_params)

    def create(self):
        result = self.meraki.exec_meraki(
            family="switch",
            function="createNetworkSwitchAccessPolicy",
            params=self.create_params(),
            op_modifies=True,
        )
        return result

    def update(self):
        id = self.new_object.get("id")
        id = id or self.new_object.get("accessPolicyNumber")
        name = self.new_object.get("name")
        result = None
        if not id:
            prev_obj_name = self.get_object_by_name(name)
            id_ = None
            if prev_obj_name:
                id_ = prev_obj_name.get("id")
                id_ = id_ or prev_obj_name.get("accessPolicyNumber")
            if id_:
                self.new_object.update(dict(accessPolicyNumber=id_))
        result = self.meraki.exec_meraki(
            family="switch",
            function="updateNetworkSwitchAccessPolicy",
            params=self.update_by_id_params(),
            op_modifies=True,
        )
        return result

    def delete(self):
        id = self.new_object.get("id")
        id = id or self.new_object.get("accessPolicyNumber")
        name = self.new_object.get("name")
        result = None
        if not id:
            prev_obj_name = self.get_object_by_name(name)
            id_ = None
            if prev_obj_name:
                id_ = prev_obj_name.get("id")
                id_ = id_ or prev_obj_name.get("accessPolicyNumber")
            if id_:
                self.new_object.update(dict(accessPolicyNumber=id_))
        result = self.meraki.exec_meraki(
            family="switch",
            function="deleteNetworkSwitchAccessPolicy",
            params=self.delete_by_id_params(),
        )
        return result


class ActionModule(ActionBase):
    def __init__(self, *args, **kwargs):
        if not ANSIBLE_UTILS_IS_INSTALLED:
            raise AnsibleActionFail(
                "ansible.utils is not installed. Execute 'ansible-galaxy collection install ansible.utils'")
        super(ActionModule, self).__init__(*args, **kwargs)
        self._supports_async = False
        self._supports_check_mode = False
        self._result = None

    # Checks the supplied parameters against the argument spec for this module
    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=dict(argument_spec=argument_spec),
            schema_format="argspec",
            schema_conditionals=dict(
                required_if=required_if,
                required_one_of=required_one_of,
                mutually_exclusive=mutually_exclusive,
                required_together=required_together,
            ),
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)

    def run(self, tmp=None, task_vars=None):
        self._task.diff = False
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._result["changed"] = False
        self._check_argspec()

        meraki = MERAKI(self._task.args)
        obj = NetworksSwitchAccessPolicies(self._task.args, meraki)

        state = self._task.args.get("state")

        response = None

        if state == "present":
            (obj_exists, prev_obj) = obj.exists()
            if obj_exists:
                if obj.requires_update(prev_obj):
                    response = obj.update()
                    meraki.object_updated()
                else:
                    response = prev_obj
                    meraki.object_already_present()
            else:
                response = obj.create()
                meraki.object_created()

        elif state == "absent":
            (obj_exists, prev_obj) = obj.exists()
            if obj_exists:
                response = obj.delete()
                meraki.object_deleted()
            else:
                meraki.object_already_absent()

        self._result.update(dict(meraki_response=response))
        self._result.update(meraki.exit_json())
        return self._result
