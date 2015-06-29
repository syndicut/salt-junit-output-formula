# -*- coding: utf-8 -*-

import logging
import yaml
from salt.utils.yamldumper import OrderedDumper
import xml.etree.ElementTree as xml
log = logging.getLogger(__name__)

def _format_host(host):
    return host.replace('.','_')

def _text_node(name, text):
    element = xml.Element(name)
    element.text = text
    return element

def _test_case(classname, name, time=False):
    element = xml.Element("testcase")
    element.attrib["name"] = name
    element.attrib["classname"] = classname
    if time is not False:
        element.attrib["time"] = time
    return element

def output(data):
    root = xml.Element("testsuite")
    root.attrib["name"] = 'state.highstate'
    for host, hostdata in data.iteritems():
        if type(hostdata) != type({}):
                log.debug('data is not iterable %s', hostdata)
                classname = _format_host(host)
                name = 'junit_check'
                test_case_element = _test_case(classname, name)
                failure_element = _text_node("failure", str(hostdata))
                test_case_element.append(failure_element)
                root.append(test_case_element)
                return xml.tostring(root)

        for key, state in hostdata.iteritems():
                classname = _format_host(host)
                name = state['name']
                time = str(round(state['duration']/1000,3))
                test_case_element = _test_case(classname, name, time)
                sysout_element = _text_node("system-out", state['comment'])
                test_case_element.append(sysout_element)
                if len(state['changes']) == 0:
                    test_case_element.append(xml.Element("skipped"))
                elif not state['result']:
                    failure_element = _text_node("failure", state['comment'])
                    test_case_element.append(failure_element)
                else:
                    params = dict(Dumper=OrderedDumper)
                    params.update(default_flow_style=False)
                    text = yaml.dump(state['changes'], **params)
                    syserr_element = _text_node("system-err", text)
                    test_case_element.append(syserr_element)

                root.append(test_case_element)
        return xml.tostring(root)
