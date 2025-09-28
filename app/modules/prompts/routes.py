"""
Prompt Management Routes

This module provides routes for viewing, managing, and analyzing
tracked prompts in the JobHunter Flask application.
"""

from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime, timedelta
from app.models import MyPrompts, PromptCategory, PromptComplexity, DevelopmentStage
from app import db
from app.middleware import track_manual_prompt

# Create blueprint
prompts_bp = Blueprint('prompts', __name__)

@prompts_bp.route('/')
def dashboard():
    """Prompt tracking dashboard"""
    return f"<h1>Prompt Tracking Dashboard</h1><p><b>Route:</b> dashboard</p><p><b>Path:</b> /prompts/</p>"

@prompts_bp.route('/list')
def list_prompts():
    """List all tracked prompts"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    complexity = request.args.get('complexity', '')
    
    # Base query
    query = MyPrompts.query
    
    # Apply filters
    if category:
        try:
            category_enum = PromptCategory(category)
            query = query.filter(MyPrompts.prompt_category == category_enum)
        except ValueError:
            pass  # Invalid category
    
    if complexity:
        try:
            complexity_enum = PromptComplexity(complexity)
            query = query.filter(MyPrompts.prompt_complexity == complexity_enum)
        except ValueError:
            pass  # Invalid complexity
    
    # Paginate results
    prompts = query.order_by(MyPrompts.created_at.desc())\
                   .paginate(page=page, per_page=20, error_out=False)
    
    # Simple HTML response showing prompts
    html = "<h1>Tracked Prompts</h1>"
    html += f"<p>Total prompts: {prompts.total}</p>"
    html += f"<p>Page {prompts.page} of {prompts.pages}</p>"
    
    for prompt in prompts.items:
        html += f"""
        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
            <h3>Prompt #{prompt.id}</h3>
            <p><b>Date:</b> {prompt.created_at}</p>
            <p><b>Category:</b> {prompt.prompt_category.value if prompt.prompt_category else 'N/A'}</p>
            <p><b>Complexity:</b> {prompt.prompt_complexity.value if prompt.prompt_complexity else 'N/A'}</p>
            <p><b>Text:</b> {prompt.prompt_text[:200]}{'...' if len(prompt.prompt_text) > 200 else ''}</p>
        </div>
        """
    
    return html

@prompts_bp.route('/stats')
def stats():
    """Prompt statistics"""
    try:
        # Get basic stats
        total_prompts = MyPrompts.query.count()
        
        # Category stats
        category_stats = db.session.query(
            MyPrompts.prompt_category,
            db.func.count(MyPrompts.id)
        ).group_by(MyPrompts.prompt_category).all()
        
        # Complexity stats
        complexity_stats = db.session.query(
            MyPrompts.prompt_complexity,
            db.func.count(MyPrompts.id)
        ).group_by(MyPrompts.prompt_complexity).all()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_prompts = MyPrompts.query.filter(
            MyPrompts.created_at >= week_ago
        ).count()
        
        stats_data = {
            'total_prompts': total_prompts,
            'recent_prompts': recent_prompts,
            'categories': {str(cat): count for cat, count in category_stats if cat},
            'complexity': {str(comp): count for comp, count in complexity_stats if comp}
        }
        
        return jsonify(stats_data)
        
    except Exception as e:
        current_app.logger.error(f"Error getting prompt stats: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500

@prompts_bp.route('/track', methods=['POST'])
def track_prompt():
    """Manually track a prompt"""
    try:
        data = request.get_json()
        
        if not data or 'prompt_text' not in data:
            return jsonify({'error': 'prompt_text is required'}), 400
        
        # Track the prompt using our service
        track_manual_prompt(
            prompt_text=data['prompt_text'],
            current_file=data.get('current_file'),
            response_summary=data.get('response_summary'),
            success_rating=data.get('success_rating')
        )
        
        return jsonify({'message': 'Prompt tracked successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error tracking prompt: {e}")
        return jsonify({'error': 'Failed to track prompt'}), 500

@prompts_bp.route('/search')
def search_prompts():
    """Search prompts by text"""
    query_text = request.args.get('q', '')
    if not query_text:
        return jsonify([])
    
    try:
        # Simple text search
        prompts = MyPrompts.query.filter(
            MyPrompts.prompt_text.contains(query_text)
        ).order_by(MyPrompts.created_at.desc()).limit(10).all()
        
        results = []
        for prompt in prompts:
            results.append({
                'id': prompt.id,
                'text': prompt.prompt_text[:100] + '...' if len(prompt.prompt_text) > 100 else prompt.prompt_text,
                'category': prompt.prompt_category.value if prompt.prompt_category else None,
                'date': prompt.created_at.isoformat()
            })
        
        return jsonify(results)
        
    except Exception as e:
        current_app.logger.error(f"Error searching prompts: {e}")
        return jsonify({'error': 'Search failed'}), 500

@prompts_bp.route('/export')
def export_prompts():
    """Export prompts as JSON"""
    try:
        # Get date range
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        prompts = MyPrompts.query.filter(
            MyPrompts.created_at >= start_date
        ).order_by(MyPrompts.created_at.desc()).all()
        
        export_data = []
        for prompt in prompts:
            export_data.append(prompt.to_dict())
        
        return jsonify({
            'total': len(export_data),
            'date_range': f"Last {days} days",
            'exported_at': datetime.utcnow().isoformat(),
            'prompts': export_data
        })
        
    except Exception as e:
        current_app.logger.error(f"Error exporting prompts: {e}")
        return jsonify({'error': 'Export failed'}), 500

@prompts_bp.route('/<int:prompt_id>')
def get_prompt(prompt_id):
    """Get details of a specific prompt"""
    try:
        prompt = MyPrompts.query.get_or_404(prompt_id)
        
        # Simple HTML display
        html = f"""
        <h1>Prompt Details #{prompt.id}</h1>
        <p><b>Date:</b> {prompt.created_at}</p>
        <p><b>Session:</b> {prompt.session_id}</p>
        <p><b>Category:</b> {prompt.prompt_category.value if prompt.prompt_category else 'N/A'}</p>
        <p><b>Complexity:</b> {prompt.prompt_complexity.value if prompt.prompt_complexity else 'N/A'}</p>
        <p><b>Development Stage:</b> {prompt.development_stage.value if prompt.development_stage else 'N/A'}</p>
        <p><b>Success Rating:</b> {prompt.success_rating or 'N/A'}</p>
        <p><b>Follow-up Needed:</b> {'Yes' if prompt.follow_up_needed else 'No'}</p>
        <p><b>Current File:</b> {prompt.current_file or 'N/A'}</p>
        <p><b>Project Phase:</b> {prompt.project_phase or 'N/A'}</p>
        <p><b>Keywords:</b> {prompt.keywords or 'N/A'}</p>
        <p><b>Tags:</b> {prompt.tags or 'N/A'}</p>
        <hr>
        <h3>Prompt Text:</h3>
        <pre style="white-space: pre-wrap;">{prompt.prompt_text}</pre>
        <hr>
        <h3>Response Summary:</h3>
        <pre style="white-space: pre-wrap;">{prompt.response_summary or 'N/A'}</pre>
        <hr>
        <p><b>Files Created:</b> {prompt.files_created or 'None'}</p>
        <p><b>Files Modified:</b> {prompt.files_modified or 'None'}</p>
        <p><b>Commands Executed:</b> {prompt.commands_executed or 'None'}</p>
        """
        
        return html
        
    except Exception as e:
        current_app.logger.error(f"Error getting prompt {prompt_id}: {e}")
        return f"<h1>Error</h1><p>Prompt not found or error occurred: {e}</p>", 404


@prompts_bp.route('/auto-capture', methods=['POST'])
def auto_capture():
    """Auto-capture endpoint for tracking prompts automatically"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'No prompt provided'}), 400
            
        prompt_text = data['prompt'].strip()
        if len(prompt_text) < 5:
            return jsonify({'error': 'Prompt too short'}), 400
            
        # Check if already exists
        existing = MyPrompts.query.filter_by(prompt_text=prompt_text).first()
        if existing:
            return jsonify({'message': 'Prompt already tracked', 'id': existing.id}), 200
            
        # Track the prompt automatically
        from app.services.conversation_tracker import track_user_prompt
        success = track_user_prompt(prompt_text)
        
        if success:
            return jsonify({'message': 'Prompt tracked successfully'}), 201
        else:
            return jsonify({'error': 'Failed to track prompt'}), 500
            
    except Exception as e:
        current_app.logger.error(f"Error in auto-capture: {e}")
        return jsonify({'error': str(e)}), 500


@prompts_bp.route('/track-current', methods=['POST'])  
def track_current():
    """Track current user prompt - for easy testing"""
    try:
        prompt_text = request.form.get('prompt') or request.json.get('prompt', '') if request.is_json else ''
        
        if not prompt_text or len(prompt_text.strip()) < 5:
            return jsonify({'error': 'Please provide a valid prompt'}), 400
            
        # Track using the conversation tracker
        from app.services.conversation_tracker import track_user_prompt  
        success = track_user_prompt(prompt_text)
        
        if success:
            # Get the tracked prompt details
            tracked_prompt = MyPrompts.query.filter_by(prompt_text=prompt_text).first()
            return jsonify({
                'message': 'Prompt tracked successfully!',
                'id': tracked_prompt.id if tracked_prompt else None,
                'prompt_preview': prompt_text[:100] + '...' if len(prompt_text) > 100 else prompt_text
            }), 201
        else:
            return jsonify({'error': 'Failed to track prompt'}), 500
            
    except Exception as e:
        current_app.logger.error(f"Error tracking current prompt: {e}")
        return jsonify({'error': str(e)}), 500