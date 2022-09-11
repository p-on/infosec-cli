from __main__ import *
import httpx
from datetime import datetime

# credit to xueledoc

try:
    doc_id = ''.join([x for x in margs[0].split("?")[0].split("/") if len(x) in (33, 44)])
    if doc_id:
        headers = {"X-Origin": "https://drive.google.com"}
        client = httpx.Client(headers=headers)

        url = f"https://clients6.google.com/drive/v2beta/files/{doc_id}?fields=alternateLink%2CcopyRequiresWriterPermission%2CcreatedDate%2Cdescription%2CdriveId%2CfileSize%2CiconLink%2Cid%2Clabels(starred%2C%20trashed)%2ClastViewedByMeDate%2CmodifiedDate%2Cshared%2CteamDriveId%2CuserPermission(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cpermissions(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cparents(id)%2Ccapabilities(canMoveItemWithinDrive%2CcanMoveItemOutOfDrive%2CcanMoveItemOutOfTeamDrive%2CcanAddChildren%2CcanEdit%2CcanDownload%2CcanComment%2CcanMoveChildrenWithinDrive%2CcanRename%2CcanRemoveChildren%2CcanMoveItemIntoTeamDrive)%2Ckind&supportsTeamDrives=true&enforceSingleParent=true&key=AIzaSyC1eQ1xj69IdTMeii5r7brs3R90eck-m7k"

        retries, failed = 100, False
        for retry in range(retries):
            req = client.get(url)
            if "File not found" in req.text:
                failed = True
            elif "rateLimitExceeded" in req.text:
                continue
            else:
                break
        else:
            failed = True

        if not failed:
            data = json.loads(req.text)

            created_date = datetime.strptime(data["createdDate"], '%Y-%m-%dT%H:%M:%S.%fz')
            modified_date = datetime.strptime(data["modifiedDate"], '%Y-%m-%dT%H:%M:%S.%fz')

            results.append(f"\033[0mCreated — \033[32m{created_date.strftime('%Y/%m/%d %H:%M:%S')}")
            results.append(f"\033[0mLast Updated — \033[32m{modified_date.strftime('%Y/%m/%d %H:%M:%S')}")

            user_permissions = []
            if data["userPermission"]:
                if data["userPermission"]["id"] == "me":
                    user_permissions.append(data["userPermission"]["role"])
                    if "additionalRoles" in data["userPermission"]:
                        user_permissions += data["userPermission"]["additionalRoles"]

            public_permissions = []
            owner = None
            for permission in data["permissions"]:
                if permission["id"] in ["anyoneWithLink", "anyone"]:
                    public_permissions.append(permission["role"])
                    if "additionalRoles" in data["permissions"]:
                        public_permissions += permission["additionalRoles"]
                elif permission["role"] == "owner":
                    owner = permission

            for permission in public_permissions:
                results.append(f"\033[0mPermission — \033[32m{permission}")

            if public_permissions != user_permissions:
                for permission in user_permissions:
                    results.append(f"\033[0mSpecial Permission — \033[32m{permission}")

            if owner:
                results.append(f"\033[0mOwner Name — \033[32m{owner['name']}")
                results.append(f"\033[0mOwner Email — \033[32m{owner['emailAddress']}")
                results.append(f"\033[0mOwner GAID — \033[32m{owner['id']}")
        else:
            results.append(f"\033[31mRatelimited or non-existant document")
    else:
        results.append(f"\033[31mInvalid document ID")
except Exception as e:
    results.append(f"\033[31m{e}")