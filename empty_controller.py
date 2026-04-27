#!/usr/bin/env python
"""
Empty Ryu controller for Phase 2.

Logs OpenFlow handshake from switches but installs no flows.
"""
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3


class EmptyController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(EmptyController, self).__init__(*args, **kwargs)
        self.logger.info('EmptyController started - waiting for switches')

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        dpid = datapath.id
        self.logger.info('Switch connected (dpid=%s) - OpenFlow handshake ok', dpid)
        # Do not install any flow entries

    @set_ev_cls(ofp_event.EventOFPStateChange, MAIN_DISPATCHER)
    def state_change_handler(self, ev):
        # Keep for future use
        pass
