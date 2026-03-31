from toolsmith.policy import harness_policy, load_policy, render_policy_summary, render_policy_text


def test_policy_canonical_values():
    data = load_policy()
    policy = harness_policy()

    assert data["cliRequired"] is True
    assert data["cliVersion"] == "1.3.2"
    assert data["validationWorkflowShape"] == "minimal-xml-skeleton"
    assert data["smokeTestEnabled"] is True
    assert policy.cli_required is True
    assert policy.cli_version == "1.3.2"
    assert policy.validation_workflow_shape == "minimal-xml-skeleton"
    assert policy.smoke_test_enabled is True


def test_policy_renderers():
    summary = render_policy_summary()
    text = render_policy_text()

    assert summary["cli"]["required"] is True
    assert summary["cli"]["version"] == "1.3.2"
    assert "CLI required: yes" in text
    assert "Validation: minimal XML workflow skeleton by default" in text
