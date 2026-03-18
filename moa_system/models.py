"""
Models for MOA and Legal Opinion Tracking System
Dataclass definitions for domain objects
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Record:
    """Record model for MOA and Legal Opinion tracking"""
    control_number: str
    school_name: str
    course: str
    number_of_hours: int
    date_received: str
    date_lo: Optional[str] = None
    legal_opinion: bool = False
    lo_scanned: bool = False
    lo_file: Optional[str] = None
    date_moa: Optional[str] = None
    moa_available: bool = False
    moa_scanned: bool = False
    moa_file: Optional[str] = None
    workflow_stage: str = 'Received'
    status: str = 'Ongoing'
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            'id': self.id,
            'control_number': self.control_number,
            'school_name': self.school_name,
            'course': self.course,
            'number_of_hours': self.number_of_hours,
            'date_received': self.date_received,
            'date_lo': self.date_lo,
            'legal_opinion': self.legal_opinion,
            'lo_scanned': self.lo_scanned,
            'lo_file': self.lo_file,
            'date_moa': self.date_moa,
            'moa_available': self.moa_available,
            'moa_scanned': self.moa_scanned,
            'moa_file': self.moa_file,
            'workflow_stage': self.workflow_stage,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Create record from dictionary"""
        return Record(
            id=data.get('id'),
            control_number=data.get('control_number'),
            school_name=data.get('school_name'),
            course=data.get('course'),
            number_of_hours=data.get('number_of_hours'),
            date_received=data.get('date_received'),
            date_lo=data.get('date_lo'),
            legal_opinion=data.get('legal_opinion', False),
            lo_scanned=data.get('lo_scanned', False),
            lo_file=data.get('lo_file'),
            date_moa=data.get('date_moa'),
            moa_available=data.get('moa_available', False),
            moa_scanned=data.get('moa_scanned', False),
            moa_file=data.get('moa_file'),
            workflow_stage=data.get('workflow_stage', 'Received'),
            status=data.get('status', 'Ongoing'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

@dataclass
class DashboardStats:
    """Dashboard statistics model"""
    total_records: int = 0
    ongoing_records: int = 0
    completed_records: int = 0
    missing_lo: int = 0
    missing_moa: int = 0
    
    @staticmethod
    def from_dict(data: dict):
        """Create stats from dictionary"""
        return DashboardStats(
            total_records=data.get('total', 0),
            ongoing_records=data.get('ongoing', 0),
            completed_records=data.get('completed', 0),
            missing_lo=data.get('missing_lo', 0),
            missing_moa=data.get('missing_moa', 0)
        )
