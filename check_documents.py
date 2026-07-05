from app import app

from models.document import ComplaintDocument

with app.app_context():

    docs = ComplaintDocument.query.all()

    print("Total Documents:", len(docs))

    for doc in docs:

        print(
            "ID:", doc.id,
            "Complaint:", doc.complaint_id,
            "File:", doc.file_name
        )