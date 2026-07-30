from unittest.mock import patch

from ui.super_resumer_dashboard import SuperResumerDashboard


def test_render_jobs_table_uses_plain_text_rendering():
    dashboard = SuperResumerDashboard()
    jobs = [
        {
            "title": "Senior C# Developer",
            "company": "Microsoft",
            "location": "Bangalore",
            "salary": "15-20 LPA",
            "match_score": 98,
            "source": "linkedin",
            "status": "pending",
            "match_analysis": {"resume_type": "C# Developer"},
        }
    ]

    with patch("ui.super_resumer_dashboard.st.info") as mock_info, patch(
        "ui.super_resumer_dashboard.st.markdown"
    ) as mock_markdown, patch("ui.super_resumer_dashboard.st.write") as mock_write:
        result = dashboard.render_jobs_table(jobs)

    assert result == jobs
    assert mock_info.call_count == 0
    assert any("Senior C# Developer" in str(call.args[0]) for call in mock_markdown.call_args_list)
    assert any("Microsoft" in str(call.args[0]) for call in mock_markdown.call_args_list)


def test_build_july_record_creates_current_month_entry():
    dashboard = SuperResumerDashboard()
    jobs = [
        {
            "title": "Python AI Engineer",
            "company": "Google",
            "location": "Bangalore",
            "salary": "18-25 LPA",
            "match_score": 99,
            "source": "linkedin",
            "status": "pending",
            "match_analysis": {"resume_type": "Python AI Developer"},
        }
    ]

    record = dashboard._build_july_record(jobs)

    assert record["month"] == "July 2026"
    assert record["title"] == "Python AI Engineer"
    assert record["status"] == "applied"
    assert record["applied_date"].startswith("2026-07")


def test_render_jobs_table_sorts_applied_jobs_by_latest_date():
    dashboard = SuperResumerDashboard()
    jobs = [
        {
            "title": "Older Applied Job",
            "company": "OldCo",
            "location": "Bangalore",
            "salary": "10-15 LPA",
            "match_score": 80,
            "source": "linkedin",
            "status": "applied",
            "applied_date": "2026-07-01T10:00:00",
            "match_analysis": {"resume_type": "C# Developer"},
        },
        {
            "title": "Newest Applied Job",
            "company": "NewCo",
            "location": "Hyderabad",
            "salary": "12-18 LPA",
            "match_score": 90,
            "source": "indeed",
            "status": "applied",
            "applied_date": "2026-07-20T10:00:00",
            "match_analysis": {"resume_type": "Python AI Developer"},
        },
    ]

    with patch("ui.super_resumer_dashboard.st.markdown") as mock_markdown:
        dashboard.render_jobs_table(jobs, "applied")

    rendered = "\n".join(str(call.args[0]) for call in mock_markdown.call_args_list)
    assert "Newest Applied Job" in rendered
    assert rendered.index("Newest Applied Job") < rendered.index("Older Applied Job")


def test_render_jobs_table_sorts_all_jobs_by_latest_date():
    dashboard = SuperResumerDashboard()
    jobs = [
        {
            "title": "Older Job",
            "company": "OldCo",
            "location": "Bangalore",
            "salary": "10-15 LPA",
            "match_score": 80,
            "source": "linkedin",
            "status": "pending",
            "applied_date": "2026-07-01T10:00:00",
            "match_analysis": {"resume_type": "C# Developer"},
        },
        {
            "title": "Newest Job",
            "company": "NewCo",
            "location": "Hyderabad",
            "salary": "12-18 LPA",
            "match_score": 90,
            "source": "indeed",
            "status": "pending",
            "applied_date": "2026-07-20T10:00:00",
            "match_analysis": {"resume_type": "Python AI Developer"},
        },
    ]

    with patch("ui.super_resumer_dashboard.st.markdown") as mock_markdown:
        dashboard.render_jobs_table(jobs, "all")

    rendered = "\n".join(str(call.args[0]) for call in mock_markdown.call_args_list)
    assert "Newest Job" in rendered
    assert rendered.index("Newest Job") < rendered.index("Older Job")
