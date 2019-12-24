#!/home/jeremy/ProjectPython/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#

import sys
import os
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive


class GDrive():
    def __init__(self, credentials_filepath):
        gauth = GoogleAuth()
        scope = ['https://www.googleapis.com/auth/drive']
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_filepath, scope)
        self.drive = GoogleDrive(gauth)

    def upload_google_doc(self, title, content):
        fileobj = self.drive.CreateFile({'title':title, 'mimetype':'application/vnd.google-apps.document'})
        fileobj.SetContentString(content)
        fileobj.Upload()
        return fileobj['id']

    def download_google_doc(self, file_id, filepath):
        fileobj = self.drive.CreateFile({'id':file_id})
        return fileobj.GetContentFile(filepath)
    
    #~ def share_google_doc(self, file_id):
        #~ fileobj = self.drive.CreateFile({'id':file_id})
        #~ perm = fileobj.InsertPermission(
                #~ {
                    #~ "kind": "drive#permissionId",
                    #~ "id": "16783462743074028936"
                #~ }
            #~ )
            
        #~ return fileobj, perm
    
    



