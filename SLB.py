# -*- coding: utf-8 -*-
import sys

from typing import List
import requests

from alibabacloud_slb20140515.client import Client as Slb20140515Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_slb20140515 import models as slb_20140515_models


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def getCidr(url = 'http://140.246.36.49:40080'):
        response = requests.get(url)
        return response.text.replace('\n', '').replace('\r', '')

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str
    ) -> Slb20140515Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'slb.aliyuncs.com'
        return Slb20140515Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        region_id = args[2]
        acl_id = args[3]
        client = Sample.create_client(args[0], args[1])
        describe_access_control_list_attribute_request = slb_20140515_models.DescribeAccessControlListAttributeRequest(
            region_id= region_id,
            acl_id=acl_id
        )

        acl = client.describe_access_control_list_attribute(describe_access_control_list_attribute_request)
        print(acl.body)

        public_ip = '{0}/32'.format(Sample.getCidr())
        print('public ip: ' + public_ip)

        if acl.body.acl_entrys is not None:
            public_entry = next((el for el in acl.body.acl_entrys.acl_entry if el.acl_entry_ip == public_ip), None)
            if public_entry is not None:
                print('public ip is already exists.')
                return 0
            to_be_removing = acl.AclEntrys.AclEntry[:]
        else:
            to_be_removing = None

        add_access_control_list_entry_request = slb_20140515_models.AddAccessControlListEntryRequest(
            acl_entrys='[{"entry":"'+ public_ip +'","comment":"dev"}]',
            region_id= region_id,
            acl_id=acl_id
        )
        client.add_access_control_list_entry(add_access_control_list_entry_request)
        print('added ' + public_ip)

        if to_be_removing is None:
            return 0

        for entry in to_be_removing:
            remove_access_control_list_entry_request = slb_20140515_models.RemoveAccessControlListEntryRequest(
                region_id= region_id,
                acl_id=acl_id,
                acl_entrys='[{"entry":"{0}","comment":"dev"}]'.format(entry.AclEntryIP)
            )
            client.remove_access_control_list_entry(remove_access_control_list_entry_request)
            print('removed '+ entry.AclEntryIP)


if __name__ == '__main__':
    Sample.main(['<accessKeyId>', '<accessSecret>', '<region>', 'acl-id'])