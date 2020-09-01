#!/usr/bin/env python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Uploads an apk to the alpha track."""

import argparse
import sys
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2
import re
from googleapiclient.http import MediaFileUpload
from pprint import pprint

TRACK = 'internal'  # Can be 'alpha', beta', 'production' or 'rollout'

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('service_account_email',
                       help='The service account email. Example: 567180731153-compute@developer.gserviceaccount.com')
argparser.add_argument('key_file',
                       help='The p12 or json file.')
argparser.add_argument('package_name',
                       help='The package name. Example: com.android.sample')
argparser.add_argument('apk_file',
                       nargs='?',
                       default='test.apk',
                       help='The path to the APK file to upload.')
argparser.add_argument('version_name',
                       help='The Version name. Example: API Release')

def main(argv):

    args = argparser.parse_args()
    # Process flags and read their values.
    service_account_email = args.service_account_email
    key_file = args.key_file
    package_name = args.package_name
    apk_file = args.apk_file
    version_name = args.version_name

    # Load the key in PKCS 12 format that you downloaded from the Google APIs
    # Console when you created your Service account.
    # f = file(key_file, 'rb')
    # key = f.read()
    # f.close()

    # Authenticate and construct service.
    if re.match(r".+\.p12", key_file):
        credentials = ServiceAccountCredentials.from_p12_keyfile(
            service_account_email,
            key_file,
            scopes=['https://www.googleapis.com/auth/androidpublisher'])
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file,
            scopes=['https://www.googleapis.com/auth/androidpublisher'])
    http = httplib2.Http()
    http = credentials.authorize(http)

    service = build('androidpublisher', 'v3', http=http)


    try:
        edit_request = service.edits().insert(body={}, packageName=package_name)
        result = edit_request.execute()
        edit_id = result['id']

        # apk support
        apk_response = None
        if re.match(r".+\.aab", apk_file):
            media = MediaFileUpload(apk_file, mimetype='application/octet-stream', resumable=True)
            apk_response = service.edits().bundles().upload(
                editId=edit_id,
                packageName=package_name,
                media_body=media).execute()
        else:
            apk_response = service.edits().apks().upload(
                editId=edit_id,
                packageName=package_name,
                media_body=apk_file).execute()

        print('Version code %d has been uploaded' % apk_response['versionCode'])

        track_response = service.edits().tracks().update(
            editId=edit_id,
            track=TRACK,
            packageName=package_name,
            body={u'releases': [{
                u'name': version_name,
                u'versionCodes': [str(apk_response['versionCode'])],
                u'status': u'completed',
            }]}).execute()

        print('Track %s is set with releases: %s' % (
            track_response['track'], str(track_response['releases']))
        )

        commit_request = service.edits().commit(
            editId=edit_id, packageName=package_name).execute()

        print('Edit "%s" has been committed' % (commit_request['id']))

    except Exception as e:
        print ('The credentials have been revoked or expired, please re-run the '
               'application to re-authorize')
        raise Exception(e)

if __name__ == '__main__':
    main(sys.argv)
