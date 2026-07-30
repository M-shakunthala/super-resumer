"""
Job tracking database for application history and analytics
"""
import sqlite3


class JobMemory:
    """Manages job application state with comprehensive tracking"""

    def __init__(self):

        self.conn = sqlite3.connect(
            "jobs.db",
            check_same_thread=False
        )

        self.create()

    def create(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs(
            url TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            platform TEXT,
            status TEXT,
            score REAL,
            interview INTEGER DEFAULT 0,
            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.conn.commit()

    def save(
        self,
        job
    ):

        self.conn.execute(
            """
            INSERT OR REPLACE INTO jobs
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (
                job["url"],
                job["title"],
                job["company"],
                job["platform"],
                job["status"],
                job["score"],
                job.get("interview", 0)
            )
        )

        self.conn.commit()

    def exists(self, url):
        """
        Check if job URL exists in database
        
        Args:
            url: Job URL to check
            
        Returns:
            True if job exists, False otherwise
        """
        cur = self.conn.execute("SELECT 1 FROM jobs WHERE url=?", (url,))
        return cur.fetchone() is not None

    def get_all_jobs(self):
        """
        Get all jobs from database
        
        Returns:
            List of job dictionaries
        """
        cur = self.conn.execute("""
            SELECT url, title, company, platform, status, score, interview, created_at 
            FROM jobs 
            ORDER BY created_at DESC
        """)
        
        jobs = []
        for row in cur.fetchall():
            jobs.append({
                "url": row[0],
                "title": row[1],
                "company": row[2],
                "platform": row[3],
                "status": row[4],
                "score": row[5],
                "interview": row[6],
                "created_at": row[7]
            })
        
        return jobs

    def get_jobs_by_status(self, status):
        """
        Get jobs filtered by status
        
        Args:
            status: Status to filter by
            
        Returns:
            List of job dictionaries
        """
        cur = self.conn.execute("""
            SELECT url, title, company, platform, status, score, interview, created_at 
            FROM jobs 
            WHERE status = ?
            ORDER BY created_at DESC
        """, (status,))
        
        jobs = []
        for row in cur.fetchall():
            jobs.append({
                "url": row[0],
                "title": row[1],
                "company": row[2],
                "platform": row[3],
                "status": row[4],
                "score": row[5],
                "interview": row[6],
                "created_at": row[7]
            })
        
        return jobs

    def update_status(self, url, status):
        """
        Update job status
        
        Args:
            url: Job URL
            status: New status
        """
        self.conn.execute(
            "UPDATE jobs SET status = ? WHERE url = ?",
            (status, url)
        )
        self.conn.commit()

    def set_interview(self, url, interview=1):
        """
        Update interview status
        
        Args:
            url: Job URL
            interview: Interview status (1 = got interview, 0 = no interview)
        """
        self.conn.execute(
            "UPDATE jobs SET interview = ? WHERE url = ?",
            (interview, url)
        )
        self.conn.commit()

    def get_stats(self):
        """
        Get database statistics
        
        Returns:
            Dictionary with job statistics
        """
        stats = {}
        
        # Total jobs
        cur = self.conn.execute("SELECT COUNT(*) as count FROM jobs")
        stats['total'] = cur.fetchone()[0]
        
        # Count by status
        cur = self.conn.execute("SELECT status, COUNT(*) as count FROM jobs GROUP BY status")
        for row in cur.fetchall():
            stats[row[0]] = row[1]
        
        # Count by platform
        cur = self.conn.execute("SELECT platform, COUNT(*) as count FROM jobs GROUP BY platform")
        for row in cur.fetchall():
            stats['platform_' + str(row[0])] = row[1]
        
        # Interview count
        cur = self.conn.execute("SELECT COUNT(*) as count FROM jobs WHERE interview = 1")
        stats['interviews'] = cur.fetchone()[0]
        
        # Interview rate
        cur = self.conn.execute("SELECT COUNT(*) as total FROM jobs WHERE status = 'applied'")
        total_applied = cur.fetchone()[0]
        if total_applied > 0:
            cur = self.conn.execute("SELECT COUNT(*) as count FROM jobs WHERE interview = 1 AND status = 'applied'")
            interviews = cur.fetchone()[0]
            stats['interview_rate'] = round((interviews / total_applied) * 100, 1)
        
        # Average score
        cur = self.conn.execute("SELECT AVG(score) as avg_score FROM jobs WHERE score IS NOT NULL")
        avg_score = cur.fetchone()[0]
        if avg_score:
            stats['avg_score'] = round(avg_score, 2)
        
        return stats

    def close(self):
        """Close database connection"""
        self.conn.close()