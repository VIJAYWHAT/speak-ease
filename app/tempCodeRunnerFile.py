app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.secret_key = "secure_secret_key"
db = firestore.client()
