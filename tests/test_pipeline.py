from unittest.mock import MagicMock

from app.workflow.lead_pipeline import LeadPipeline


def test_pipeline():
    pipeline = LeadPipeline()

    pipeline.extractor.analyze = MagicMock(...)
    pipeline.qualifier.evaluate = MagicMock(...)
    pipeline.sheets.append = MagicMock()
    pipeline.slack.notify = MagicMock()
    pipeline.email.generate = MagicMock(return_value="Reply")

    result = pipeline.run("email")

    assert result["reply_email"] == "Reply"

    pipeline.sheets.append.assert_called_once()
    pipeline.slack.notify.assert_called_once()