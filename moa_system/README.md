# MOA & Legal Opinion Tracking System

A desktop application built with Python and PyQt5 for tracking Memorandum of Agreement (MOA) and Legal Opinion (LO) documents for schools and universities.

## Features

- **Dashboard**: View summary statistics including total records, ongoing records, completed records, and missing documents
- **Add Records**: Create new MOA/LO records with comprehensive form
- **Records Management**: View, edit, and delete records with search and filtering capabilities
- **File Management**: Upload and manage PDF documents for MOA and Legal Opinion
- **Status Tracking**: Track workflow stages and document status with color indicators
- **SQLite Database**: Persistent data storage with automatic backup

## Technology Stack

- **Language**: Python 3.8+
- **GUI Framework**: PyQt5
- **Database**: SQLite3
- **File Management**: OS-level file handling

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone or download the project to your desired location

2. Navigate to the project directory:
```bash
cd moa_system
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Execute the main script:
```bash
python main.py
```

## Project Structure

```
moa_system/
├── main.py                      # Application entry point
├── database.py                  # Database operations
├── models.py                    # Data models
├── requirements.txt             # Python dependencies
│
├── ui/                          # User interface modules
│   ├── __init__.py
│   ├── dashboard.py             # Dashboard window with statistics
│   ├── add_record.py            # Form for adding new records
│   ├── records_table.py         # Records table with search/filter
│   └── edit_record.py           # Form for editing records
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── control_number_generator.py  # Auto-generate control numbers
│   └── file_handler.py          # File upload/download operations
│
├── uploads/                     # Document storage
│   ├── lo/                      # Legal Opinion PDFs
│   └── moa/                     # MOA PDFs
│
└── moa_tracking.db             # SQLite database (created at first run)
```

## Usage Guide

### Dashboard
- View key statistics at a glance
- Click "Refresh" to update statistics

### Adding a Record
1. Navigate to "Add Record" tab
2. Fill in basic information (school name, course, hours, date)
3. Optionally upload Legal Opinion PDF
4. Optionally upload MOA PDF
5. Set workflow stage and status
6. Click "Save Record"

### Managing Records
1. Navigate to "Records" tab
2. Use search bar to find records by control number, school name, or course
3. Use filter dropdown to view specific categories
4. Select a record and click:
   - **View**: See complete record details
   - **Edit**: Modify record information and files
   - **Delete**: Remove record (with confirmation)

### File Management
- Files are automatically organized in the uploads folder
- Control Number is used as the file identifier
- You can upload, view, or delete files from any record

## Database Schema

The application uses a single SQLite table `records` with the following fields:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key (auto-increment) |
| control_number | TEXT | Unique identifier (format: MOA-YYYY-###) |
| school_name | TEXT | Name of school/university |
| course | TEXT | Course name |
| number_of_hours | INTEGER | Course hours |
| date_received | DATE | Date record was received |
| date_lo | DATE | Legal Opinion date |
| legal_opinion | BOOLEAN | Whether LO is available |
| lo_scanned | BOOLEAN | Whether LO is scanned |
| lo_file | TEXT | Path to LO PDF file |
| date_moa | DATE | MOA date |
| moa_available | BOOLEAN | Whether MOA is available |
| moa_scanned | BOOLEAN | Whether MOA is scanned |
| moa_file | TEXT | Path to MOA PDF file |
| workflow_stage | TEXT | Current workflow stage |
| status | TEXT | Record status (Ongoing/Completed) |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

## Control Number Format

Control numbers are auto-generated in the format: `MOA-YYYY-###`

- MOA: Fixed prefix
- YYYY: Current year
- ###: Sequence number (001-999)

Example: `MOA-2026-001`

## Status & Workflow

### Workflow Stages
- Received
- For Legal Review
- Legal Opinion Issued
- MOA Preparation
- For Signing
- Completed

### Record Status
- Ongoing: Currently being processed
- Completed: Finished with all requirements met

## Color Indicators

- **Green**: Completed or Available
- **Yellow**: Ongoing
- **Orange**: Missing Legal Opinion
- **Red**: Missing MOA

## Tips & Best Practices

1. **Regular Backups**: The database is stored in `moa_tracking.db`. Back it up regularly.
2. **File Organization**: Keep uploaded PDFs in the designated folders (automatically handled)
3. **Search Tips**: Use partial names or control numbers for flexible searching
4. **Filtering**: Use filters to quickly identify documents that need attention
5. **Workflow Tracking**: Update workflow stages as documents progress through approval process

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Database errors
- Check that the application has write permissions in the directory
- The database file will be created automatically on first run

### File upload issues
- Ensure only PDF files are uploaded
- Check that upload directories have proper permissions
- Verify disk space is available

### Missing records after restart
- Check that `moa_tracking.db` file exists in the moa_system directory
- Ensure the database file hasn't been moved or deleted

## Future Enhancements

Potential features for future versions:
- Export records to Excel/CSV
- Email notifications for pending documents
- User authentication and role-based access
- Advanced reporting and analytics
- Document versioning and history tracking
- Batch operations for multiple records

## License

This project is provided as-is for organizational use.

## Support

For issues or questions, please refer to the project documentation or contact your system administrator.
