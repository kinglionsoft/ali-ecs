#!/usr/bin/env python
#coding=utf-8

import json
import requests

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupAttributeRequest import DescribeSecurityGroupAttributeRequest
from aliyunsdkecs.request.v20140526.RevokeSecurityGroupRequest import RevokeSecurityGroupRequest
from aliyunsdkecs.request.v20140526.AuthorizeSecurityGroupRequest import AuthorizeSecurityGroupRequest

class SecruityGroup:

    def __init__(self, AccessKey, AccessSecret, RegionId):
        self.AccessKey = AccessKey
        self.AccessSecret = AccessSecret
        self.RegionId = RegionId

    def client(self):
        """用于创建AcsClient实例
        """
        client = AcsClient(self.AccessKey, self.AccessSecret, self.RegionId)
        return client

    def getRules(self, groupId):
        """
        获取安全组的规则
        """
        request = DescribeSecurityGroupAttributeRequest()
        request.set_accept_format('json')

        request.set_SecurityGroupId(groupId)

        client = self.client()

        response = client.do_action_with_exception(request)

        data = json.loads(response)

        return (data['Permissions']['Permission'])

    def changeSourceCidr(self, groupId, descPrefix, newCidr = None):
        """
        修改源地址
        """
        if newCidr is None:
            newCidr = self.getCidr()
        print('new SourceCidrIp: ' + newCidr)
        rules = self.getRules(groupId)

        targetRules = [x for x in rules if x['Description'].startswith(descPrefix)]

        index = 1

        for r in targetRules:
            print('\n%d: %s' % (index, r))
            index = index + 1
            cidr = r['SourceCidrIp']

            if cidr == newCidr:
                print('samve CIDR, ignore')
                continue

            portRange = r['PortRange']
            inProtocol = r['IpProtocol']
            desc = r['Description']

            self.revokeRule(groupId, portRange, inProtocol, cidr)
            print('revoked')

            self.createRule(groupId, portRange, inProtocol, newCidr, desc)
            print('created')


    def revokeRule(self, groupId, portRange, inProtocol, cidr):
        """
        撤销规则
        """
        request = RevokeSecurityGroupRequest()
        request.set_accept_format('json')
        request.set_SecurityGroupId(groupId)
        request.set_PortRange(portRange)
        request.set_IpProtocol(inProtocol)
        request.set_SourceCidrIp(cidr)

        client = self.client()

        response = client.do_action_with_exception(request)

        data = str(response, encoding='utf-8')

        if ('"Code"' in data):
            raise Exception(str(response))


    def createRule(self, groupId, portRange, inProtocol, cidr, desc):
        """
        创建规则
        """
        request = AuthorizeSecurityGroupRequest()
        request.set_accept_format('json')

        request.set_SecurityGroupId(groupId)
        request.set_PortRange(portRange)
        request.set_IpProtocol(inProtocol)
        request.set_SourceCidrIp(cidr)
        request.set_Description(desc)

        client = self.client()

        response = client.do_action_with_exception(request)

        data = str(response, encoding='utf-8')

        if ('"Code"' in data):
                raise Exception(str(response))

    def getCidr(self, url = 'http://140.246.36.49:40080'):
        response = requests.get(url)
        return response.text.replace('\n', '').replace('\r', '')

if __name__ == '__main__':
    group = SecruityGroup('<accessKeyId>', '<accessSecret>', '<region>')
    group.changeSourceCidr('<group id>', '<comment>')

