# #!/usr/bin/env python
#
# """Create Testflight."""
#
# import argparse
# import sys
# import jwt
# import json
# import time
# import requests
# from datetime import datetime, timedelta
#
# # Declare command-line flags.
# argparser = argparse.ArgumentParser(add_help=False)
# argparser.add_argument('apple_store_key_id',
#                        help='The Apple Store Key ID.')
# argparser.add_argument('key_path',
#                        nargs='?',
#                        default='test.apk',
#                        help='The iTunes Connect Private Key File.')
# argparser.add_argument('issue_id',
#                        help='The isuee id.')
#
# def main(argv):
#
#     args = argparser.parse_args()
#
#     ALGORITHM = 'ES256'
#
#     APP_STORE_KEY_ID = args.apple_store_key_id
#     ISSUER_ID = args.issue_id
#     KEY_PATH = args.key_path
#
#     secret = ""
#     with open(KEY_PATH,'r') as f:
#         secret = f.read()
#     exp = int(time.mktime((datetime.now() + timedelta(minutes=20)).timetuple()))
#     token = jwt.encode(
#         {
#             'iss': ISSUER_ID,
#             "exp": exp,
#             "aud": "appstoreconnect-v1"
#         },
#         secret,
#         algorithm=ALGORITHM,
#         headers={
#             'alg': ALGORITHM,
#             'kid': APP_STORE_KEY_ID,
#             "typ": "JWT"
#         }
#     )
#
#     url = 'https://api.appstoreconnect.apple.com/v1/users'
#     hed = {'Authorization': 'Bearer {}'.format(token.decode('ascii'))}
#     data = {}
#     response = requests.get(url, headers=hed)
#     data = response.json()
#     print(response.status_code)
#     print(json.dumps(data, ensure_ascii=False, indent=4))
#     # # Authenticate and construct service.
#     # service, flags = sample_tools.init(
#     #     argv,
#     #     'androidpublisher',
#     #     'v3',
#     #     __doc__,
#     #     __file__, parents=[argparser],
#     #     scope='https://www.googleapis.com/auth/androidpublisher')
#     #
#     # # Process flags and read their values.
#     # package_name = flags.package_name
#     # apk_file = flags.apk_file
#     # version_name = flags.version_name
#     #
#     # try:
#     #     edit_request = service.edits().insert(body={}, packageName=package_name)
#     #     result = edit_request.execute()
#     #     edit_id = result['id']
#     #
#     #     apk_response = service.edits().apks().upload(
#     #         editId=edit_id,
#     #         packageName=package_name,
#     #         media_body=apk_file).execute()
#     #
#     #     print 'Version code %d has been uploaded' % apk_response['versionCode']
#     #
#     #     track_response = service.edits().tracks().update(
#     #         editId=edit_id,
#     #         track=TRACK,
#     #         packageName=package_name,
#     #         body={u'releases': [{
#     #             u'name': version_name,
#     #             u'versionCodes': [str(apk_response['versionCode'])],
#     #             u'status': u'completed',
#     #         }]}).execute()
#     #
#     #     print 'Track %s is set with releases: %s' % (
#     #         track_response['track'], str(track_response['releases']))
#     #
#     #     commit_request = service.edits().commit(
#     #         editId=edit_id, packageName=package_name).execute()
#     #
#     #     print 'Edit "%s" has been committed' % (commit_request['id'])
#     #
#     # except client.AccessTokenRefreshError:
#     #     print ('The credentials have been revoked or expired, please re-run the '
#     #            'application to re-authorize')
#
# if __name__ == '__main__':
#     main(sys.argv)
