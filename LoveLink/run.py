from app import create_app, db
from app.models import LovePage
import os
app = create_app()

# 🔥 Create database tables automatically
with app.app_context():
    db.create_all()

if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
    #app.run(debug=True)
     app.run(host="0.0.0.0", port=port, debug=False)
