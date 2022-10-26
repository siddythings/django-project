import firebase_admin, requests
from firebase_admin import messaging, credentials, db, initialize_app, storage
from application.settings import FIREBASE_NOTIFICATION_KEY, NOTIFICATION_STORAGE_BUKET

class BookingServicesClass:
    def update_report(self, file):
        cred = credentials.Certificate(FIREBASE_NOTIFICATION_KEY)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {'storageBucket': NOTIFICATION_STORAGE_BUKET})
        
        # responce = requests.get(url, allow_redirects=True)
        fileName = file.read()    
        bucket = storage.bucket()
        blob = bucket.blob("files2.pdf")
        # blob.upload_from_filename(fileName)
        blob.upload_from_string(
            fileName,
            content_type=file.content_type
            )
        blob.make_public()
        firebase_admin.delete_app(firebase_admin.get_app()) 
        pdf_url = blob.public_url
        return True

BookingServices = BookingServicesClass()