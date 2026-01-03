"""Main application module"""
from service import create_app
from flask import jsonify
import click

app = create_app()

# Add root endpoint with required response
@app.route('/')
def index():
    """Root endpoint with service info"""
    return jsonify({
        "name": "Account REST API Service",
        "version": "1.0"
    })

# Add health check endpoint
@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

# Add error handler for bad JSON requests
@app.errorhandler(400)
def handle_bad_request(e):
    """Handle bad requests including invalid JSON"""
    if hasattr(e, 'description') and 'Failed to decode JSON object' in str(e.description):
        return jsonify({'error': 'Invalid JSON format'}), 400
    return jsonify({'error': str(e.description) if hasattr(e, 'description') else 'Bad request'}), 400

@app.errorhandler(500)
def handle_internal_error(e):
    """Handle internal server errors"""
    app.logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# Add custom Flask command for db-create
@app.cli.command("db-create")
def db_create():
    """Create database tables"""
    from service import db
    with app.app_context():
        db.create_all()
        click.echo('Database tables created successfully!')

def run_app():
    """Function to run the app (makes it testable)"""
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_app()
