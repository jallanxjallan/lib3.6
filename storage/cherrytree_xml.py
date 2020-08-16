    #!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cherrytree.py
#

import sys
import os
import re
from pathlib import Path
import logging
import attr
import time
from lxml import etree
from lxml.etree import XPathEvalError
import base64
import urllib

note_pat = re.compile(r'~+')

@attr.s
class Codebox():
    element = attr.ib()
    def __attrs_post_init__(self):
        self.content = self.element.text
        self.language = self.element.attrib['language']

@attr.s
class Anchor():
    element = attr.ib()
    def __attrs_post_init__(self):
        self.name = self.element.attrib['anchor']

@attr.s
class Link():
    element = attr.ib()
    def __attrs_post_init__(self):
        self.text = self.element.text
        args = self.element.attrib['link'].split()
        self.type = args[0]
        if self.type == 'file':
            self.href = base64.b64decode(args[1]).decode()
        else:
            self.href = args[1]

class Node():
    def __init__(self, element):
        self.element = element
        self.id = element.attrib['unique_id']
        self.name = element.attrib['name']

    @property
    def level(self):
        ans = [a for a in self.element.iterancestors()]
        return len(ans)

    @property
    def parent(self):
        try:
            return Node(self.element.getparent())
        except Exception as e:
            return None

    def insert_element(self, element):
        try:
            self.element.append(element)
        except Exception as e:
            print ('Insert failed because of', e)
            return False
        return True

    @property
    def children(self):
        return (Node(c) for c in self.element.iterchildren('node'))

    @property
    def descendants(self):
        return (Node(c) for c in self.element.iterdescendants('node'))


    @property
    def texts(self):
        return (e.text for e in self.element.iterchildren('rich_text') if e.text)

    @property
    def notes(self):
        try:
            return note_pat.split('\n'.join(list(self.texts)))[1]
        except IndexError:
            return None

    @property
    def links(self):
        return (Link(l) for l in self.element.findall('rich_text[@link]'))

    @property
    def filepath(self):
        links = self.links
        return next((l.href for l in links if l.type == 'file'), None)

    @property
    def codeboxes(self):
        return (Codebox(c) for c in self.element.xpath('codebox'))

    @property
    def anchors(self):
        return (Anchor(a) for a in self.element.xpath('encoded_png'))

    def insert_link(self, href, text, parent=None):
        element = etree.Element('rich_text')
        href = base64.b64encode(str(href).encode("utf-8")).decode()
        element.attrib['link'] = f'file {href}'
        element.text = text
        return Link(element) if self.insert_element(element) else None


    def insert_codebox(self, content, language='yaml', parent=None):
        atts = dict(
            language=language,
            char_offset="10",
            frame_height="200",
            frame_width="700",
            highlight_brackets="True",
            show_line_numbers="False",
            syntax_highlighting='yaml',
        )
        element = etree.Element('codebox', atts)
        element.text = content
        return Codebox(element) if self.insert_element(element) else None


    def insert_text(self, content, parent=None):
        element = etree.Element('rich_text')
        element.text = content
        return content if self.insert_element(element) else None

    def insert_anchor(self, name, parent=None):
        element = etree.Element('encoded_png',
                                char_offset="0",
                                anchor=name)
        return Anchor(element) if self.insert_element(element) else None

class CherryTree():
    def __init__(self, filepath):
        if type(filepath) is str:
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError
        self.tree = etree.parse(str(filepath))
        self.root = self.tree.getroot()
        self.filepath = filepath

    def save(self, *arg):
        if arg:
            filepath = Path(arg[0])
        else:
            filepath = self.filepath
        with filepath.open('wb') as outfile:
            outfile.write(etree.tostring(self.tree))

    def nodes(self, base_arg=None):
        if base_arg:
            try:
                base_node = base_arg.element
            except AttributeError:
                try:
                    base_node = self.find_node_by_name(base_arg).element
                except Exception as e:
                    print(e)
                    return None
        else:
            base_node = self.root

        for element in [e for e in base_node.iter() if e.tag == 'node']:
            yield Node(element)

    def find_node_by_xpath(self, xpath):
        try:
            m = self.tree.xpath(xpath)
        except XPathEvalError:
            print(f'bad xpath {xpath}')
            return False
        if not m:
            return False

        if m[0].tag == 'node':
            return Node(m[0])
        elif len(m) == 1:
            return Node(m[0].getparent())
        else:
            return next((Node(n) for n in reversed(m) if n.tag == 'node'), None)

    def find_node_by_id(self, id):
        return self.find_node_by_xpath(f'//node[@unique_id={id}]')

    def find_node_by_name(self, name):
        return self.find_node_by_xpath(f'//node[@name="{name}"]')

    def find_node_by_text(self, text):
        return self.find_node_by_xpath(f'//*[contains(., "{text}")]')

    def find_node_by_attribute(self, attr, value):
        return self.find_node_by_xpath(f'//*[@{attr}="{value}"]')

    def find_node_by_pattern(self, pat):
        try:
            m = self.tree.xpath(f"//a[re:match(text(), {pat})]",
                namespaces={"re": "http://exslt.org/regular-expressions"})
        except XPathEvalError:
            print(f'bad xpath {pat}')
            return False
        return m

    def create_node(self, name):
        unique_id = max([int(id.attrib['unique_id']) for id in self.tree.xpath('//node[@unique_id]')])
        timestamp = str(time.time())
        return Node(etree.Element('node',
                name=name,
                unique_id=str(unique_id + 1),
                custom_icon_id="0",
                foreground="",
                is_bold="False",
                prog_lang="custom-colors",
                readonly="False",
                ts_creation=timestamp,
                ts_lastsave=timestamp
            ))

    def insert_node(self, element, parent=None, sibling=None):
        element = element.element if hasattr(element, 'element') else element
        parent = parent.element if hasattr(parent, 'element') else parent
        sibling = sibling.element if hasattr(sibling, 'element') else sibling
        try:
            if parent:
                parent.append(element)
            elif sibling:
                sibling.addnext(element)
            else:
                self.root.append(element)
        except Exception as e:
            print(e)
            raise e
        return Node(element)
