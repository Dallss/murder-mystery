import pytest
from backend.agents.models.template_models import MysteryTemplate, Suspect, Clue
from backend.agents.models.player_models import PlayerProfile
from backend.agents.template_agent import TemplateAgent

@pytest.fixture
def sample_template():
    return MysteryTemplate(
        id="template1",
        title="The Locked Room Mystery",
        victim="{{victim_name}}",
        murder_method="Blunt force trauma",
        location="Private study, locked from the inside",
        suspects=[
            Suspect(id="s1", name="{{suspect_1}}", motive="{{motive_1}}", alibi="{{alibi_1}}", guilty=True),
            Suspect(id="s2", name="{{suspect_2}}", motive="{{motive_2}}", alibi="{{alibi_2}}", guilty=False),
        ],
        clues=[
            Clue(id="c1", type="physical", description="A bloodied candlestick", found_at="bookshelf", relevance="murder weapon", related_suspects=["s1"]),
            Clue(id="c2", type="logical", description="The window was unlocked from the outside", found_at=None, relevance="explains the locked-room trick", related_suspects=[]),
        ],
        red_herrings=["A torn photo suggesting an affair (unrelated)"]
    )

@pytest.fixture
def sample_player_profile():
    return PlayerProfile(
        psychological_traits={"logic": 0.8, "intuition": 0.6},
        preferences={"setting": "classic", "difficulty": "medium"},
        play_history={}
    )

def test_extract_template_variables(sample_template):
    agent = TemplateAgent(use_mem0=False)
    variables = agent.extract_template_variables(sample_template)
    assert set(variables) == {"victim_name", "suspect_1", "motive_1", "alibi_1", "suspect_2", "motive_2", "alibi_2"}

def test_validate_template(sample_template):
    agent = TemplateAgent(use_mem0=False)
    errors = agent.validate_template(sample_template)
    assert errors == []

    # Remove all suspects to trigger error
    template_no_suspects = sample_template.copy(update={"suspects": []})
    errors = agent.validate_template(template_no_suspects)
    assert "Template must have at least one suspect" in errors

    # Remove all clues to trigger error
    template_no_clues = sample_template.copy(update={"clues": []})
    errors = agent.validate_template(template_no_clues)
    assert "Template must have at least one clue" in errors

    # Remove guilty flag
    suspects = [s.copy(update={"guilty": False}) for s in sample_template.suspects]
    template_no_guilty = sample_template.copy(update={"suspects": suspects})
    errors = agent.validate_template(template_no_guilty)
    assert "Template must have at least one guilty suspect" in errors

# The following test is for expected use and will only work if LLM API keys are set up and the agent is functional.
# Uncomment to run in a fully configured environment.
# import os
# import pytest
# @pytest.mark.asyncio
# async def test_populate_template(sample_template, sample_player_profile):
#     agent = TemplateAgent(use_mem0=False)
#     populated = agent.populate_template(sample_template, sample_player_profile)
#     assert "{{" not in populated.victim
#     for suspect in populated.suspects:
#         assert "{{" not in suspect.name
#         assert "{{" not in suspect.motive
#         assert "{{" not in suspect.alibi
