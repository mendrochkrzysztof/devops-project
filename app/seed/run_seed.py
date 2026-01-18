#!/usr/bin/env python3
"""
Database seeder script
Generates initial data and exports to seed_output volume
"""
import os
import sys
import json
import csv
import logging
from datetime import datetime
from pathlib import Path

# Add app to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.src import create_app
from app.src.models import db, User, Task

def setup_logging(output_dir):
    """Configure logging to file and stdout"""
    log_file = output_dir / 'seed.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def create_sample_data():
    """Create sample users and tasks"""
    users = [
        User(username='john_doe', email='john@example.com'),
        User(username='jane_smith', email='jane@example.com'),
        User(username='bob_wilson', email='bob@example.com'),
        User(username='alice_jones', email='alice@example.com'),
        User(username='charlie_brown', email='charlie@example.com')
    ]
    
    tasks = [
        Task(title='Complete project', description='Finish DevOps project', user_id=1),
        Task(title='Write tests', description='Implement unit tests', user_id=1),
        Task(title='Setup CI/CD', description='Configure GitHub Actions', user_id=2),
        Task(title='Dockerize app', description='Create Docker images', user_id=3),
        Task(title='Deploy to Azure', description='Setup Azure resources', user_id=4),
        Task(title='Documentation', description='Write project docs', user_id=5),
        Task(title='Code review', description='Review team code', user_id=2),
        Task(title='Performance test', description='Run load tests', user_id=3)
    ]
    
    return users, tasks

def export_to_csv(output_dir, users, tasks):
    """Export data to CSV files"""
    # Export users
    users_file = output_dir / 'users.csv'
    with open(users_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'username', 'email', 'created_at'])
        for user in users:
            writer.writerow([user.id, user.username, user.email, user.created_at])
    
    # Export tasks
    tasks_file = output_dir / 'tasks.csv'
    with open(tasks_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'description', 'status', 'user_id', 'created_at'])
        for task in tasks:
            writer.writerow([task.id, task.title, task.description, task.status, task.user_id, task.created_at])

def export_to_json(output_dir, users, tasks):
    """Export data to JSON file"""
    data = {
        'seed_timestamp': datetime.utcnow().isoformat(),
        'users_count': len(users),
        'tasks_count': len(tasks),
        'users': [user.to_dict() for user in users],
        'tasks': [task.to_dict() for task in tasks]
    }
    
    json_file = output_dir / 'data.json'
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def main():
    """Main seeding function"""
    # Get output directory from environment or use default
    output_dir = Path(os.environ.get('SEED_OUTPUT_DIR', '/app/seed_output'))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger = setup_logging(output_dir)
    logger.info("Starting database seeder...")
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            # Create sample data
            logger.info("Creating sample data...")
            users, tasks = create_sample_data()
            
            # Save to database
            db.session.add_all(users)
            db.session.add_all(tasks)
            db.session.commit()
            
            # Export data
            logger.info("Exporting data to files...")
            export_to_csv(output_dir, users, tasks)
            export_to_json(output_dir, users, tasks)
            
            # Create summary file
            summary = {
                'status': 'success',
                'timestamp': datetime.utcnow().isoformat(),
                'users_created': len(users),
                'tasks_created': len(tasks),
                'output_files': [
                    str(output_dir / 'seed.log'),
                    str(output_dir / 'users.csv'),
                    str(output_dir / 'tasks.csv'),
                    str(output_dir / 'data.json')
                ]
            }
            
            summary_file = output_dir / 'summary.json'
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info(f"Seeding completed successfully. Created {len(users)} users and {len(tasks)} tasks.")
            logger.info(f"Output files saved to: {output_dir}")
            
        except Exception as e:
            logger.error(f"Seeding failed: {str(e)}")
            sys.exit(1)

if __name__ == '__main__':
    main()