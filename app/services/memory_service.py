from app.services.firebase_service import db


def get_student_memory(dni):

    doc = (
        db.collection("ai_memory")
        .document(dni)
        .get()
    )

    if doc.exists:

        return doc.to_dict()

    return {}


def update_student_memory(
    dni,
    data
):

    db.collection("ai_memory") \
        .document(dni) \
        .set(
            data,
            merge=True
        )