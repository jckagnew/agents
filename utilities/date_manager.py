#!/usr/bin/env python3
"""
Date Manager for AI-Generated Documents
Ensures consistent and accurate date handling across all generated content
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

class DateManager:
    """Manages current date and time for AI-generated documents"""
    
    def __init__(self, env_file_path=".env"):
        self.env_file_path = env_file_path
        self.current_date = None
        self.current_datetime = None
        self.load_or_create_date()
    
    def load_or_create_date(self):
        """Load current date from .env or create if not exists"""
        env_path = Path(self.env_file_path)
        
        if env_path.exists():
            # Load existing .env file
            with open(env_path, 'r') as f:
                lines = f.readlines()
            
            # Check if date is already set
            for line in lines:
                if line.startswith('CURRENT_DATE='):
                    self.current_date = line.split('=', 1)[1].strip()
                    break
                elif line.startswith('CURRENT_DATETIME='):
                    self.current_datetime = line.split('=', 1)[1].strip()
                    break
        else:
            # Create new .env file
            lines = []
        
        # Update with current system date if not set or outdated
        now = datetime.now(timezone.utc)
        current_date_str = now.strftime('%B %d, %Y')
        current_datetime_str = now.strftime('%Y-%m-%d %H:%M:%S UTC')
        
        if not self.current_date or self.is_date_outdated():
            self.current_date = current_date_str
            self.current_datetime = current_datetime_str
            self.update_env_file(lines, current_date_str, current_datetime_str)
    
    def is_date_outdated(self):
        """Check if the stored date is more than 1 day old"""
        if not self.current_date:
            return True
        
        try:
            # Parse stored date
            stored_date = datetime.strptime(self.current_date, '%B %d, %Y')
            current_date = datetime.now()
            
            # Check if more than 1 day old
            days_diff = (current_date - stored_date).days
            return days_diff > 1
        except:
            return True
    
    def update_env_file(self, existing_lines, date_str, datetime_str):
        """Update .env file with current date information"""
        # Remove old date entries
        updated_lines = []
        for line in existing_lines:
            if not (line.startswith('CURRENT_DATE=') or line.startswith('CURRENT_DATETIME=')):
                updated_lines.append(line)
        
        # Add new date entries
        updated_lines.append(f'CURRENT_DATE={date_str}\n')
        updated_lines.append(f'CURRENT_DATETIME={datetime_str}\n')
        updated_lines.append(f'# Date last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        
        # Write updated .env file
        with open(self.env_file_path, 'w') as f:
            f.writelines(updated_lines)
    
    def get_current_date(self, format='%B %d, %Y'):
        """Get current date in specified format"""
        if not self.current_date:
            self.load_or_create_date()
        
        if format == '%B %d, %Y':
            return self.current_date
        
        # Convert to requested format
        try:
            date_obj = datetime.strptime(self.current_date, '%B %d, %Y')
            return date_obj.strftime(format)
        except:
            return self.current_date
    
    def get_current_datetime(self, format='%Y-%m-%d %H:%M:%S UTC'):
        """Get current datetime in specified format"""
        if not self.current_datetime:
            self.load_or_create_date()
        
        if format == '%Y-%m-%d %H:%M:%S UTC':
            return self.current_datetime
        
        # Convert to requested format
        try:
            datetime_obj = datetime.strptime(self.current_datetime, '%Y-%m-%d %H:%M:%S UTC')
            return datetime_obj.strftime(format)
        except:
            return self.current_datetime
    
    def get_formatted_date(self, format_name='standard'):
        """Get date in common formats"""
        formats = {
            'standard': '%B %d, %Y',           # September 24, 2025
            'short': '%b %d, %Y',              # Sep 24, 2025
            'iso': '%Y-%m-%d',                 # 2025-09-24
            'us': '%m/%d/%Y',                  # 09/24/2025
            'european': '%d/%m/%Y',            # 24/09/2025
            'timestamp': '%Y-%m-%d %H:%M:%S',  # 2025-09-24 12:53:22
            'readable': '%A, %B %d, %Y',       # Wednesday, September 24, 2025
        }
        
        format_str = formats.get(format_name, formats['standard'])
        return self.get_current_date(format_str)
    
    def update_date(self):
        """Force update to current system date"""
        now = datetime.now(timezone.utc)
        current_date_str = now.strftime('%B %d, %Y')
        current_datetime_str = now.strftime('%Y-%m-%d %H:%M:%S UTC')
        
        self.current_date = current_date_str
        self.current_datetime = current_datetime_str
        
        # Update .env file
        env_path = Path(self.env_file_path)
        if env_path.exists():
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        self.update_env_file(lines, current_date_str, current_datetime_str)
        print(f"✅ Date updated to: {current_date_str}")

def get_current_date(format='%B %d, %Y'):
    """Convenience function to get current date"""
    dm = DateManager()
    return dm.get_current_date(format)

def get_current_datetime(format='%Y-%m-%d %H:%M:%S UTC'):
    """Convenience function to get current datetime"""
    dm = DateManager()
    return dm.get_current_datetime(format)

def get_formatted_date(format_name='standard'):
    """Convenience function to get formatted date"""
    dm = DateManager()
    return dm.get_formatted_date(format_name)

# Example usage and testing
if __name__ == "__main__":
    print("🗓️  Date Manager Test")
    print("=" * 50)
    
    dm = DateManager()
    
    print(f"Current Date (standard): {dm.get_formatted_date('standard')}")
    print(f"Current Date (short): {dm.get_formatted_date('short')}")
    print(f"Current Date (ISO): {dm.get_formatted_date('iso')}")
    print(f"Current Date (readable): {dm.get_formatted_date('readable')}")
    print(f"Current DateTime: {dm.get_formatted_date('timestamp')}")
    
    print(f"\n📁 .env file location: {os.path.abspath('.env')}")
    print(f"📅 Date will auto-update daily")
