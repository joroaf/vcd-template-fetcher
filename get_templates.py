#!/usr/bin/env python

import csv
import argparse
import requests
from pyvcloud.vcd.utils import to_dict
from pyvcloud.vcd.client import BasicLoginCredentials, Client, ResourceType, QueryResultFormat
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warnings from urllib3
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def fetch_vapp_templates_with_metadata(
        vcd_host,
        username,
        password,
        api_version='37.0', verify_ssl_certs=False, metadata_key=None, metadata_value=None):

    # Create a vCD client with admin credentials
    client = Client(vcd_host, api_version=api_version, verify_ssl_certs=verify_ssl_certs,
                    log_headers=True, log_requests=True, log_file="./log")
    client.set_credentials(BasicLoginCredentials(username, 'System', password))  # Use 'System' for the admin org.

    query = client.get_typed_query(
        ResourceType.ADMIN_CATALOG_ITEM.value,
        query_result_format=QueryResultFormat.RECORDS
    )
    marked_templates = []
    for template in query.execute():
        t = to_dict(template)
        res = requests.get(url=f"{t['entity']}/metadata", headers={
            "x-vcloud-authorization": client._vcloud_auth_token,
            "Accept": f"application/*+json;version={api_version}"
        }, verify=verify_ssl_certs).json()
        for m in res["metadataEntry"]:
            if m["key"] == metadata_key and m["typedValue"]["value"] == metadata_value:
                marked_templates.append(t)

    if len(marked_templates) < 1:
        print(f"No templates marked with meta property {metadata_key}=={metadata_value} found!")

    csv_file = 'output.csv'

    # Specify the field names (column headers)
    field_names = [
        "entity",
        "entityName",
        "entityType",
        "catalog",
        "catalogName",
        "ownerName",
        "owner",
        "isPublished",
        "vdc",
        "vdcName",
        "isVdcEnabled",
        "org",
        "creationDate",
        "isExpired",
        "status",
        "name",
        "storageKB"
    ]

    # Write the list of dictionaries to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)

        # Write the header
        writer.writeheader()

        # Write the data
        for row in marked_templates:
            writer.writerow(row)
        
        print(f"CSV file {csv_file} was created/updated.")

    # Disconnect from the vCD
    client.logout()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch vApp templates with specific metadata from vCloud Director using admin credentials.")
    parser.add_argument("--vcd-host", required=True, help="The URL of the vCD instance.")
    parser.add_argument("--username", required=True, help="The administrator's username for vCD authentication.")
    parser.add_argument("--password", required=True, help="The administrator's password for vCD authentication.")
    parser.add_argument("--api-version", default='37.0', help="The vCD API version (default is '37.0')")
    parser.add_argument("--no-verify-ssl", action='store_true',
                        help="Disable SSL certificate verification (default is False)")
    parser.add_argument("--metadata-key", default="your.meta.data.key",
                        help="The key of the metadata property to filter on.")
    parser.add_argument("--metadata-value", default=True, help="The value of the metadata property to filter on")

    args = parser.parse_args()

    fetch_vapp_templates_with_metadata(
        args.vcd_host,
        args.username,
        args.password,
        args.api_version,
        not args.no_verify_ssl,
        args.metadata_key,
        args.metadata_value
    )
