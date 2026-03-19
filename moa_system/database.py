"""
Database module for MOA and Legal Opinion Tracking System
Handles SQLite database initialization and operations
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Tuple, Optional

from app_paths import get_db_path, migrate_legacy_db_if_needed

DB_PATH = str(get_db_path())

class Database:
    """Database handler for MOA tracking system"""
    
    def __init__(self, db_path: str = DB_PATH):
        migrate_legacy_db_if_needed()
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                control_number TEXT UNIQUE NOT NULL,
                school_name TEXT NOT NULL,
                course TEXT NOT NULL,
                number_of_hours INTEGER NOT NULL,
                date_received DATE NOT NULL,
                date_lo DATE,
                legal_opinion BOOLEAN DEFAULT 0,
                lo_scanned BOOLEAN DEFAULT 0,
                lo_file TEXT,
                date_moa DATE,
                moa_available BOOLEAN DEFAULT 0,
                moa_scanned BOOLEAN DEFAULT 0,
                moa_file TEXT,
                pinned BOOLEAN DEFAULT 0,
                workflow_stage TEXT DEFAULT 'Received',
                status TEXT DEFAULT 'Ongoing',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Lightweight migration: add missing columns for older DBs
        try:
            cursor.execute("PRAGMA table_info(records)")
            existing_cols = {row[1] for row in cursor.fetchall()}
            if "pinned" not in existing_cols:
                cursor.execute("ALTER TABLE records ADD COLUMN pinned BOOLEAN DEFAULT 0")
        except Exception as e:
            print(f"[WARNING] DB migration check failed: {e}")
        
        conn.commit()
        conn.close()
    
    def add_record(self, data: Dict) -> int:
        """Add a new record to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO records (
                    control_number, school_name, course, number_of_hours,
                    date_received, date_lo, legal_opinion, lo_scanned, lo_file,
                    date_moa, moa_available, moa_scanned, moa_file,
                    workflow_stage, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('control_number'),
                data.get('school_name'),
                data.get('course'),
                data.get('number_of_hours'),
                data.get('date_received'),
                data.get('date_lo'),
                data.get('legal_opinion', False),
                data.get('lo_scanned', False),
                data.get('lo_file'),
                data.get('date_moa'),
                data.get('moa_available', False),
                data.get('moa_scanned', False),
                data.get('moa_file'),
                data.get('workflow_stage', 'Received'),
                data.get('status', 'Ongoing')
            ))
            
            record_id = cursor.lastrowid
            conn.commit()
            return record_id
        finally:
            conn.close()
    
    def update_record(self, record_id: int, data: Dict) -> bool:
        """Update an existing record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            updates = []
            values = []
            for key, value in data.items():
                if key != 'id':
                    updates.append(f'{key} = ?')
                    values.append(value)
            
            values.append(record_id)
            query = f'UPDATE records SET {", ".join(updates)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
            
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False
        finally:
            conn.close()
    
    def delete_record(self, record_id: int) -> bool:
        """Delete a record from database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
        finally:
            conn.close()

    def delete_records(self, record_ids: List[int]) -> bool:
        """Delete multiple records by IDs"""
        if not record_ids:
            return True
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            placeholders = ",".join(["?"] * len(record_ids))
            cursor.execute(f"DELETE FROM records WHERE id IN ({placeholders})", record_ids)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting records: {e}")
            return False
        finally:
            conn.close()

    def set_pinned(self, record_ids: List[int], pinned: bool) -> bool:
        """Pin or unpin multiple records"""
        if not record_ids:
            return True
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            placeholders = ",".join(["?"] * len(record_ids))
            value = 1 if pinned else 0
            cursor.execute(
                f"UPDATE records SET pinned = ?, updated_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})",
                [value, *record_ids],
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error pinning records: {e}")
            return False
        finally:
            conn.close()
    
    def get_record(self, record_id: int) -> Optional[Dict]:
        """Get a single record by ID"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        finally:
            conn.close()
    
    def get_all_records(self, filters: Dict = None) -> List[Dict]:
        """Get all records with optional filters"""
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            query = 'SELECT * FROM records WHERE 1=1'
            params = []
            
            if filters:
                if filters.get('search'):
                    search_term = f'%{filters["search"]}%'
                    query += ' AND (control_number LIKE ? OR school_name LIKE ? OR course LIKE ?)'
                    params.extend([search_term, search_term, search_term])
                
                if filters.get('status'):
                    query += ' AND status = ?'
                    params.append(filters['status'])
                
                if filters.get('filter_type'):
                    filter_type = filters['filter_type']
                    if filter_type == 'Missing LO':
                        query += ' AND legal_opinion = 0'
                    elif filter_type == 'Missing MOA':
                        query += ' AND moa_available = 0'
            
            # Pinned records first, then newest
            query += ' ORDER BY pinned DESC, created_at DESC'
            cursor.execute(query, params)
            
            records = []
            for row in cursor.fetchall():
                records.append(dict(row))
            return records
        finally:
            conn.close()
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Total records
            cursor.execute('SELECT COUNT(*) as count FROM records')
            total = cursor.fetchone()[0]
            
            # Ongoing records
            cursor.execute('SELECT COUNT(*) as count FROM records WHERE status = "Ongoing"')
            ongoing = cursor.fetchone()[0]
            
            # Completed records
            cursor.execute('SELECT COUNT(*) as count FROM records WHERE status = "Completed"')
            completed = cursor.fetchone()[0]
            
            # Missing Legal Opinion
            cursor.execute('SELECT COUNT(*) as count FROM records WHERE legal_opinion = 0')
            missing_lo = cursor.fetchone()[0]
            
            # Missing MOA
            cursor.execute('SELECT COUNT(*) as count FROM records WHERE moa_available = 0')
            missing_moa = cursor.fetchone()[0]
            
            return {
                'total': total,
                'ongoing': ongoing,
                'completed': completed,
                'missing_lo': missing_lo,
                'missing_moa': missing_moa
            }
        finally:
            conn.close()
    
    def record_exists(self, control_number: str) -> bool:
        """Check if a control number already exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM records WHERE control_number = ?', (control_number,))
            return cursor.fetchone()[0] > 0
        finally:
            conn.close()
    
    def get_next_control_number(self, year: int = None) -> str:
        """Get the next control number for a given year"""
        if year is None:
            year = datetime.now().year
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT COUNT(*) FROM records WHERE control_number LIKE ?',
                (f'MOA-{year}-%',)
            )
            count = cursor.fetchone()[0]
            return f'MOA-{year}-{count + 1:03d}'
        finally:
            conn.close()
