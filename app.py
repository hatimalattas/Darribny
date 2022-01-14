import os
from darribny import app

port = int(os.environ.get("PORT", 4000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
