from pyzotero import zotero
import os

class ZoteroDownloader:
    def __init__(self, user_id, api_key, base_path="data/zotero_papers"):
        self.user_id = user_id
        self.api_key = api_key
        self.zot = zotero.Zotero(self.user_id, 'user', self.api_key)
        self.base_path = base_path

    def download_pdfs(self, group_limit=None):
        if group_limit is None:
            # Download from personal library
            self._download_attachments(self.zot, self.base_path)
        else:
            # Download from groups, respecting the group_limit
            groups = self.zot.groups()
            for group in groups[:group_limit]:
                group_id = group['id']
                group_name = group['data']['name'].replace(' ', '_').replace('/', '_')  # Sanitize for filesystem
                group_path = os.path.join(self.base_path, f"user_{self.user_id}", f"group_{group_id}_{group_name}")
                zot_group = zotero.Zotero(group_id, 'group', self.api_key)
                self._download_attachments(zot_group, group_path)

    def _download_attachments(self, zot_instance, path):
        # Ensure the download directory exists
        if not os.path.exists(path):
            os.makedirs(path)
        # Fetch all PDF attachments
        attachments = zot_instance.everything(zot_instance.items(itemType='attachment', linkMode='imported_file'))
        for attachment in attachments:
            # Check if the attachment is a PDF
            if 'application/pdf' in attachment['data'].get('contentType', ''):
                filename = attachment['data'].get('filename', 'unnamed.pdf')
                pdf_path = os.path.join(path, filename)
                # Skip download if file already exists
                if not os.path.exists(pdf_path):
                    try:
                        # Download the PDF file content
                        pdf_content = zot_instance.file(attachment['key'])
                        # Save the PDF file to the specified path
                        with open(pdf_path, 'wb') as pdf_file:
                            pdf_file.write(pdf_content)
                        print(f"Successfully downloaded: {filename}")
                    except Exception as e:
                        print(f"Error downloading {filename}: {e}")
                else:
                    print(f"File already exists. Skipping: {filename}")
