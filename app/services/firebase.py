import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings

# Initialize Firebase
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

db = firestore.client()

class FirebaseService:
    @staticmethod
    def get_models(filters: dict = None):
        query = db.collection("models")
        
        if filters:
            if "status" in filters and filters["status"] != "all":
                query = query.where("status", "==", filters["status"])
            if "task" in filters:
                query = query.where("task", "==", filters["task"])
        
        query = query.order_by("created_at", direction=firestore.Query.DESCENDING)
        
        return [{"id": doc.id, **doc.to_dict()} for doc in query.stream()]
    
    @staticmethod
    def add_model(model_data: dict) -> str:
        doc_ref = db.collection("models").document()
        doc_ref.set(model_data)
        return doc_ref.id
    
    @staticmethod
    def get_model(model_id: str) -> dict:
        doc = db.collection("models").document(model_id).get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None
    
    @staticmethod
    def update_model(model_id: str, updates: dict):
        db.collection("models").document(model_id).update(updates)
    
    @staticmethod
    def delete_model(model_id: str):
        db.collection("models").document(model_id).delete()
    
    @staticmethod
    def create_test(test_data: dict) -> str:
        doc_ref = db.collection("tests").document()
        doc_ref.set(test_data)
        return doc_ref.id
    
    @staticmethod
    def get_test(test_id: str) -> dict:
        doc = db.collection("tests").document(test_id).get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None
    
    @staticmethod
    def update_test(test_id: str, updates: dict):
        db.collection("tests").document(test_id).update(updates)

firebase_service = FirebaseService()
