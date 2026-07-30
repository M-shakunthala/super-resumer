import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime


class ProfileMemory:
    """Manage user profile data and preferences for job applications."""
    
    def __init__(self, profile_path: str = "memory/user_profile.json"):
        self.profile_path = Path(profile_path)
        self.profile: Dict[str, Any] = self._load_profile()
    
    def _load_profile(self) -> Dict[str, Any]:
        """Load user profile from file or create default."""
        if self.profile_path.exists():
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_profile()
    
    def _create_default_profile(self) -> Dict[str, Any]:
        """Create default user profile structure."""
        default_profile = {
            "personal_info": {
                "name": "",
                "email": "",
                "phone": "",
                "location": "",
                "linkedin_url": "",
                "github_url": ""
            },
            "skills": [],
            "experience": [],
            "education": [],
            "preferences": {
                "target_roles": [],
                "industries": [],
                "company_sizes": [],
                "remote_preference": "hybrid",
                "salary_range": {"min": 0, "max": 0, "currency": "USD"},
                "locations": []
            },
            "application_history": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
        }
        self._save_profile(default_profile)
        return default_profile
    
    def _save_profile(self, profile: Dict[str, Any]) -> None:
        """Save profile to file."""
        profile["metadata"]["last_updated"] = datetime.now().isoformat()
        self.profile_path.parent.mkdir(exist_ok=True)
        with open(self.profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
    
    def get_personal_info(self) -> Dict[str, str]:
        """Get personal information."""
        return self.profile.get("personal_info", {})
    
    def update_personal_info(self, info: Dict[str, str]) -> None:
        """Update personal information."""
        self.profile["personal_info"].update(info)
        self._save_profile(self.profile)
    
    def get_skills(self) -> List[str]:
        """Get user skills."""
        return self.profile.get("skills", [])
    
    def add_skill(self, skill: str) -> None:
        """Add a skill to the profile."""
        if skill not in self.profile["skills"]:
            self.profile["skills"].append(skill)
            self._save_profile(self.profile)
    
    def get_experience(self) -> List[Dict[str, Any]]:
        """Get work experience."""
        return self.profile.get("experience", [])
    
    def add_experience(self, experience: Dict[str, Any]) -> None:
        """Add work experience."""
        self.profile["experience"].append(experience)
        self._save_profile(self.profile)
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get job preferences."""
        return self.profile.get("preferences", {})
    
    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update job preferences."""
        self.profile["preferences"].update(preferences)
        self._save_profile(self.profile)
    
    def add_application_record(self, job_data: Dict[str, Any]) -> None:
        """Record a job application."""
        application_record = {
            "job_id": job_data.get("job_id"),
            "company": job_data.get("company"),
            "role": job_data.get("role"),
            "applied_at": datetime.now().isoformat(),
            "status": "submitted",
            "platform": job_data.get("platform", "unknown")
        }
        self.profile["application_history"].append(application_record)
        self._save_profile(self.profile)
    
    def get_application_history(self) -> List[Dict[str, Any]]:
        """Get application history."""
        return self.profile.get("application_history", [])
    
    def get_profile_summary(self) -> Dict[str, Any]:
        """Get a summary of the profile."""
        return {
            "name": self.profile["personal_info"].get("name"),
            "skills_count": len(self.profile["skills"]),
            "experience_count": len(self.profile["experience"]),
            "applications_count": len(self.profile["application_history"]),
            "last_updated": self.profile["metadata"]["last_updated"]
        }


# Example usage
if __name__ == "__main__":
    profile_memory = ProfileMemory()
    print("Profile Summary:", profile_memory.get_profile_summary())
